#!/usr/bin/env python3
"""Refresh the videos block in a profile README from the public YouTube feed.

Any network or feed problem leaves the README untouched.
"""
import html
import pathlib
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCptfYZedOFByXavKtWzqIfA"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
LIMIT = 3
HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": "SOCS=CAI"}
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
ARABIC = re.compile(r"[؀-ۿ]")
GERMAN = re.compile(
    r"\b(ein|eine|einen|deine|deinen|dein|wie|für|und|funktioniert|registriert|sich)\b",
    re.IGNORECASE,
)
BLOCK = re.compile(
    r"(<!-- videos:start(?: style=(?P<style>cards|list))? -->\n).*?(\n<!-- videos:end -->)",
    re.DOTALL,
)


class FeedError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def parse_feed(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as error:
        raise FeedError(f"invalid feed: {error}") from error
    videos = []
    for entry in root.findall("atom:entry", NS):
        video_id = entry.findtext("yt:videoId", default="", namespaces=NS)
        title = entry.findtext("atom:title", default="", namespaces=NS).strip()
        if VIDEO_ID.match(video_id) and title:
            videos.append({"id": video_id, "title": title})
    return videos


def is_english(title):
    return not ARABIC.search(title) and not GERMAN.search(title)


def is_short(video_id):
    """YouTube serves Shorts at /shorts/<id> and redirects full videos away."""
    request = urllib.request.Request(
        f"https://www.youtube.com/shorts/{video_id}", headers=HEADERS
    )
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=15) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
    except urllib.error.URLError as error:
        raise FeedError(f"could not check {video_id}: {error}") from error
    if status == 200:
        return True
    if status == 303:
        return False
    raise FeedError(f"unexpected status {status} for {video_id}")


def pick_videos(videos, short_check, limit=LIMIT):
    picked = []
    for video in videos:
        if is_english(video["title"]) and not short_check(video["id"]):
            picked.append(video)
            if len(picked) == limit:
                return picked
    raise FeedError(f"found only {len(picked)} of {limit} full English videos")


def render(videos, style="cards"):
    items = []
    for video in videos:
        url = f"https://www.youtube.com/watch?v={video['id']}"
        title = html.escape(video["title"], quote=True)
        if style == "list":
            items.append(f'<li><a href="{url}">{title}</a></li>')
        else:
            thumb = f"https://i.ytimg.com/vi/{video['id']}/mqdefault.jpg"
            items.append(
                f'<td width="33%" valign="top"><a href="{url}"><img src="{thumb}" '
                f'alt="{title}" width="100%"></a><br><a href="{url}">{title}</a></td>'
            )
    if style == "list":
        return "<ul>\n" + "\n".join(items) + "\n</ul>"
    return "<table>\n<tr>\n" + "\n".join(items) + "\n</tr>\n</table>"


def replace_block(text, videos):
    match = BLOCK.search(text)
    if not match:
        raise ValueError("videos markers not found")
    block = render(videos, match.group("style") or "cards")
    return text[: match.start()] + match.group(1) + block + match.group(3) + text[match.end() :]


def fetch_feed():
    request = urllib.request.Request(FEED_URL, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as error:
        raise FeedError(f"could not fetch feed: {error}") from error


def main(argv):
    path = pathlib.Path(argv[1] if len(argv) > 1 else "README.md")
    text = path.read_text(encoding="utf-8")
    try:
        videos = pick_videos(parse_feed(fetch_feed()), is_short)
    except FeedError as error:
        print(f"::warning::Videos not updated: {error}")
        return 0
    updated = replace_block(text, videos)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print("Videos updated.")
    else:
        print("Videos already current.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
