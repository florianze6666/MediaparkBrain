"""Text hinter einer Adresse holen — fuer das Feld "Link oder Text" im Drop-In.

Bewusst eng gehalten, weil hier der Server auf Zuruf des Browsers eine fremde
Adresse laedt:

* nur http und https,
* 10 Sekunden Zeitlimit,
* hoechstens 2 MB (der Rest wird abgeschnitten, nicht nachgeladen),
* keine Weiterleitung auf interne Adressen (localhost, private Netze) —
  sonst waere das Feld ein bequemer Weg, das interne Netz abzufragen,
* nur Text: HTML wird auf den lesbaren Inhalt reduziert, alles andere
  (PDF, Bilder, Downloads) wird abgelehnt statt geraten.

Fehler kommen als ValueError mit einem Satz, der direkt in der Statuszeile
stehen kann.
"""
from __future__ import annotations

import html
import ipaddress
import re
import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse

TIMEOUT = 10          # Sekunden
MAX_BYTES = 2 * 1024 * 1024
USER_AGENT = "Kompass/1.0 (+MediaparkBrain)"

URL_ONLY_RE = re.compile(r"^<?(https?://[^\s<>\"']+?)>?[.,;]?$", re.IGNORECASE)

_SCRIPT_RE = re.compile(r"(?is)<(script|style|noscript|template)\b.*?</\1\s*>")
_BREAK_RE = re.compile(r"(?i)<(br\s*/?|/p|/div|/li|/h[1-6]|/tr)\s*>")
_TAG_RE = re.compile(r"(?s)<[^>]+>")
_TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
_WS_RE = re.compile(r"[ \t\f\v]+")
_NL_RE = re.compile(r"\n{3,}")

TEXT_TYPES = ("text/", "application/xhtml", "application/xml", "application/json")


def find_url(text: str) -> str | None:
    """Die Adresse, wenn der Eingabetext *nur* aus einer Adresse besteht.

    Steht die Adresse mitten in einem Absatz, ist der Absatz gemeint und nicht
    die Seite dahinter — dann wird nichts geladen.
    """
    match = URL_ONLY_RE.match((text or "").strip())
    return match.group(1) if match else None


def _check_host(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Nur http- und https-Adressen werden geladen.")
    if not parsed.hostname:
        raise ValueError("Diese Adresse hat keinen Rechnernamen.")
    try:
        infos = socket.getaddrinfo(parsed.hostname, None)
    except OSError:
        raise ValueError(f"Adresse nicht erreichbar: {parsed.hostname}")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise ValueError("Adressen im internen Netz werden nicht geladen.")
    return parsed.hostname


def html_to_text(raw: str) -> str:
    """HTML auf lesbaren Text reduzieren. Kein Parser, keine neue Abhaengigkeit."""
    text = _SCRIPT_RE.sub(" ", raw)
    text = _BREAK_RE.sub("\n", text)
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = _WS_RE.sub(" ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    return _NL_RE.sub("\n\n", text).strip()


def fetch_text(url: str) -> tuple[str, str]:
    """(Text, Bezeichnung) hinter der Adresse. ValueError mit klarem Satz sonst."""
    host = _check_host(url)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310
            # Nach einer Weiterleitung kann eine ganz andere Adresse dastehen.
            final = response.geturl()
            if final != url:
                _check_host(final)
            ctype = (response.headers.get("Content-Type") or "").lower()
            if ctype and not any(ctype.startswith(t) for t in TEXT_TYPES):
                raise ValueError(f"Unter dieser Adresse steht kein Text ({ctype.split(';')[0]}).")
            raw = response.read(MAX_BYTES + 1)[:MAX_BYTES]
            charset = response.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as exc:
        raise ValueError(f"Die Seite antwortet mit Fehler {exc.code}.")
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as exc:
        raise ValueError(f"Seite nicht geladen ({getattr(exc, 'reason', exc)}).")

    body = raw.decode(charset, errors="replace")
    label = host
    if "<" in body:
        title = _TITLE_RE.search(body)
        if title:
            label = html.unescape(_TAG_RE.sub(" ", title.group(1))).strip() or host
        body = html_to_text(body)
    if not body.strip():
        raise ValueError("Unter dieser Adresse war kein lesbarer Text.")
    return body, label
