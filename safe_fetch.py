"""Téléchargement d'images distantes sans SSRF (audit sécurité du 2026-11-12, point S4).

Les proxys d'images (/api/img-proxy, /api/tt-thumb, /api/feed-radar/{id}/thumb)
téléchargent côté serveur une URL venue de l'extérieur. Avant ce module :
  - seule la PREMIÈRE URL était vérifiée, puis httpx suivait les redirections sans
    revalider la destination : un hôte autorisé pouvait rebondir vers le réseau
    interne (169.254.169.254, 127.0.0.1, 10.x…) ;
  - /api/img-proxy renvoyait le corps même quand ce n'était pas une image (étiqueté
    image/jpeg), ce qui permettait de LIRE la réponse de la cible ;
  - les vignettes oEmbed n'étaient pas filtrées du tout.

Désormais, à CHAQUE saut (URL initiale et chaque redirection) :
  1. https obligatoire, pas d'IP littérale, hôte dans la liste blanche (`host_allowed`) ;
  2. le nom d'hôte doit résoudre uniquement vers des adresses publiques ;
  3. redirections suivies à la main, 3 au maximum ;
puis la réponse n'est rendue que si c'est vraiment une image (type ET signature),
avec une taille plafonnée.

Limite connue : entre notre résolution DNS et celle de httpx, un DNS malveillant
pourrait changer de réponse (rebinding). La liste blanche ne contient que des CDN
(ByteDance/TikTok, Akamai…), ce qui rend ce scénario très improbable.
"""
from __future__ import annotations

import asyncio
import ipaddress
import socket
from dataclasses import dataclass
from typing import Awaitable, Callable, Iterable, Optional
from urllib.parse import urljoin, urlparse

import httpx

MAX_REDIRECTS = 3
MAX_IMAGE_BYTES = 8_000_000
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"

Resolver = Callable[[str], Awaitable[list[str]]]


@dataclass
class FetchedImage:
    content: bytes
    content_type: str


def host_allowed(url: str, allowed: Iterable[str]) -> bool:
    """https + nom d'hôte (pas d'IP littérale) appartenant à un domaine autorisé."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower().rstrip(".")
    if not host:
        return False
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    return any(host == d or host.endswith("." + d) for d in allowed if d)


def is_public_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    # IPv4 encapsulée dans IPv6 (::ffff:127.0.0.1) : on juge l'IPv4 réelle.
    if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
        addr = addr.ipv4_mapped
    return addr.is_global and not addr.is_multicast


async def _system_resolver(host: str) -> list[str]:
    loop = asyncio.get_running_loop()
    infos = await loop.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    return [info[4][0] for info in infos]


def looks_like_image(head: bytes) -> bool:
    """Signature binaire des formats d'image servis par les CDN (JPEG, PNG, GIF, WebP, AVIF/HEIC)."""
    return (
        head.startswith(b"\xff\xd8\xff")
        or head.startswith(b"\x89PNG\r\n\x1a\n")
        or head.startswith((b"GIF87a", b"GIF89a"))
        or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")
        or head[4:8] == b"ftyp"
    )


async def resolve_redirects(
    url: str,
    allowed: Iterable[str],
    *,
    timeout: float = 12.0,
    max_redirects: int = 5,
    transport: Optional[httpx.AsyncBaseTransport] = None,
    resolver: Optional[Resolver] = None,
) -> Optional[str]:
    """Suit les redirections (liens courts) en restant dans `allowed` à chaque saut.

    Retourne l'URL finale, ou None si un saut sort de la liste blanche, vise une
    adresse non publique ou dépasse `max_redirects`. Le corps n'est jamais lu.
    """
    allowed = tuple(allowed)
    resolve = resolver or _system_resolver
    current = url
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False, transport=transport) as client:
        for _saut in range(max_redirects + 1):
            if not host_allowed(current, allowed):
                return None
            try:
                ips = await resolve(urlparse(current).hostname or "")
            except Exception:
                return None
            if not ips or not all(is_public_ip(ip) for ip in ips):
                return None
            async with client.stream("GET", current, headers={"User-Agent": "Mozilla/5.0"}) as r:
                if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("location"):
                    current = urljoin(current, r.headers["location"])
                    continue
                return current
    return None


async def fetch_image(
    url: str,
    allowed: Iterable[str],
    *,
    timeout: float = 6.0,
    transport: Optional[httpx.AsyncBaseTransport] = None,
    resolver: Optional[Resolver] = None,
    on_reject: Optional[Callable[[str, str], None]] = None,
) -> Optional[FetchedImage]:
    """Télécharge une image en revalidant chaque saut. None si refusé ou si ce n'est pas une image."""
    allowed = tuple(allowed)
    resolve = resolver or _system_resolver

    def reject(raison: str, cible: str) -> None:
        if on_reject:
            on_reject(raison, cible)
        return None

    current = url
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False, transport=transport) as client:
        for _saut in range(MAX_REDIRECTS + 1):
            if not host_allowed(current, allowed):
                return reject("hôte refusé", current)
            host = urlparse(current).hostname or ""
            try:
                ips = await resolve(host)
            except Exception:
                return reject("résolution DNS impossible", current)
            if not ips or not all(is_public_ip(ip) for ip in ips):
                return reject("adresse non publique", current)

            async with client.stream("GET", current, headers={"User-Agent": USER_AGENT, "Referer": ""}) as r:
                if r.status_code in (301, 302, 303, 307, 308):
                    location = r.headers.get("location")
                    if not location:
                        return reject("redirection sans destination", current)
                    current = urljoin(current, location)
                    continue
                if not r.is_success:
                    return reject(f"statut {r.status_code}", current)

                body = bytearray()
                async for chunk in r.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_IMAGE_BYTES:
                        return reject("image trop lourde", current)

                ct = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
                if not looks_like_image(bytes(body[:16])):
                    return reject(f"pas une image ({ct or 'type inconnu'})", current)
                if not ct.startswith("image/"):
                    ct = "image/jpeg"
                return FetchedImage(bytes(body), ct)
        return reject("trop de redirections", current)
