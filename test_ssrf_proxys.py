"""SSRF des proxys d'images et des liens courts (audit sécurité du 2026-11-12, point S4).

Réseau et DNS simulés (httpx.MockTransport + résolveur factice) : aucun appel réel.
"""
from __future__ import annotations

import asyncio

import httpx

import safe_fetch

CDN = ("tiktokcdn.com", "byteimg.com")
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 64
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64

# DNS factice : tout est public sauf les noms « interne ».
async def dns(host: str) -> list[str]:
    return ["10.0.0.7"] if "interne" in host else ["151.101.1.1"]


def _run(coro):
    return asyncio.run(coro)


def _transport(routes: dict[str, httpx.Response]):
    vus: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        vus.append(url)
        return routes.get(url, httpx.Response(404))

    return httpx.MockTransport(handler), vus


def _fetch(url, routes):
    transport, vus = _transport(routes)
    return _run(safe_fetch.fetch_image(url, CDN, transport=transport, resolver=dns)), vus


def test_image_legitime_servie():
    img, _ = _fetch("https://p16.tiktokcdn.com/a.jpg",
                    {"https://p16.tiktokcdn.com/a.jpg": httpx.Response(200, content=JPEG,
                                                                       headers={"content-type": "image/jpeg"})})
    assert img and img.content == JPEG and img.content_type == "image/jpeg"


def test_redirection_vers_les_metadonnees_cloud_refusee():
    img, vus = _fetch("https://p16.tiktokcdn.com/a.jpg", {
        "https://p16.tiktokcdn.com/a.jpg": httpx.Response(302, headers={"location": "http://169.254.169.254/latest/meta-data/"}),
        "http://169.254.169.254/latest/meta-data/": httpx.Response(200, content=b"secret"),
    })
    assert img is None
    assert all("169.254" not in u for u in vus), "la cible interne ne doit jamais être contactée"


def test_redirection_vers_un_hote_hors_liste_refusee():
    img, vus = _fetch("https://p16.tiktokcdn.com/a.jpg", {
        "https://p16.tiktokcdn.com/a.jpg": httpx.Response(302, headers={"location": "https://evil.example/x.jpg"}),
        "https://evil.example/x.jpg": httpx.Response(200, content=JPEG, headers={"content-type": "image/jpeg"}),
    })
    assert img is None and "https://evil.example/x.jpg" not in vus


def test_hote_autorise_resolvant_vers_une_ip_privee_refuse():
    img, vus = _fetch("https://interne.tiktokcdn.com/a.jpg", {
        "https://interne.tiktokcdn.com/a.jpg": httpx.Response(200, content=JPEG, headers={"content-type": "image/jpeg"}),
    })
    assert img is None and not vus


def test_reponse_qui_n_est_pas_une_image_refusee():
    # Avant : re-servie étiquetée image/jpeg → lecture du contenu de la cible.
    img, _ = _fetch("https://p16.tiktokcdn.com/a.jpg", {
        "https://p16.tiktokcdn.com/a.jpg": httpx.Response(200, content=b'{"token":"x"}',
                                                          headers={"content-type": "image/jpeg"}),
    })
    assert img is None


def test_image_avec_type_generique_acceptee_par_signature():
    img, _ = _fetch("https://v.byteimg.com/a", {
        "https://v.byteimg.com/a": httpx.Response(200, content=PNG,
                                                  headers={"content-type": "application/octet-stream"}),
    })
    assert img and img.content == PNG


def test_redirection_legitime_entre_cdn_suivie():
    img, _ = _fetch("https://p16.tiktokcdn.com/a.jpg", {
        "https://p16.tiktokcdn.com/a.jpg": httpx.Response(302, headers={"location": "https://p19.byteimg.com/b.jpg"}),
        "https://p19.byteimg.com/b.jpg": httpx.Response(200, content=JPEG, headers={"content-type": "image/jpeg"}),
    })
    assert img and img.content == JPEG


def test_trop_de_redirections_refuse():
    routes = {f"https://p{i}.tiktokcdn.com/a.jpg":
              httpx.Response(302, headers={"location": f"https://p{i + 1}.tiktokcdn.com/a.jpg"}) for i in range(10)}
    img, _ = _fetch("https://p0.tiktokcdn.com/a.jpg", routes)
    assert img is None


def test_image_trop_lourde_refusee(monkeypatch):
    monkeypatch.setattr(safe_fetch, "MAX_IMAGE_BYTES", 32)
    img, _ = _fetch("https://p16.tiktokcdn.com/a.jpg", {
        "https://p16.tiktokcdn.com/a.jpg": httpx.Response(200, content=JPEG, headers={"content-type": "image/jpeg"}),
    })
    assert img is None


def test_ipv4_encapsulee_en_ipv6_non_publique():
    assert not safe_fetch.is_public_ip("::ffff:127.0.0.1")
    assert not safe_fetch.is_public_ip("169.254.169.254")
    assert safe_fetch.is_public_ip("151.101.1.1")


# ── Liens courts TikTok (market_creators._resolve_short_url) ─────────────────

def _resolve(url, routes):
    transport, vus = _transport(routes)
    return _run(safe_fetch.resolve_redirects(url, ("tiktok.com",), transport=transport, resolver=dns)), vus


def test_lien_court_tiktok_resolu():
    final, _ = _resolve("https://vm.tiktok.com/ZMabc/", {
        "https://vm.tiktok.com/ZMabc/": httpx.Response(301, headers={"location": "https://www.tiktok.com/view/product/1729"}),
        "https://www.tiktok.com/view/product/1729": httpx.Response(200),
    })
    assert final == "https://www.tiktok.com/view/product/1729"


def test_lien_court_redirigeant_vers_le_reseau_interne_refuse():
    final, vus = _resolve("https://vm.tiktok.com/ZMabc/", {
        "https://vm.tiktok.com/ZMabc/": httpx.Response(302, headers={"location": "http://127.0.0.1:10000/admin"}),
    })
    assert final is None and all("127.0.0.1" not in u for u in vus)


def test_url_non_tiktok_jamais_contactee():
    final, vus = _resolve("http://10.0.0.5/interne", {})
    assert final is None and not vus
