#!/usr/bin/env python3
"""Love Singing — find lyrics instantly for your sing-along sessions!"""

import os
import sys
import argparse
import requests

# ── ANSI colours ────────────────────────────────────────────────────────────
R   = "\033[0m"
B   = "\033[1m"
DIM = "\033[2m"
CYN = "\033[96m"
YLW = "\033[93m"
GRN = "\033[92m"
MGT = "\033[95m"
RED = "\033[91m"
WHT = "\033[97m"

LYRICS_API = "https://api.lyrics.ovh/v1"

# Built-in offline library — used as fallback when the network is unavailable
OFFLINE_LIBRARY = {
    ("rihanna", "we found love"): (
        "Yellow diamonds in the light\n"
        "And we're standing side by side\n"
        "As your shadow crosses mine\n"
        "What it takes to come alive\n\n"
        "It's the way I'm feeling\n"
        "I just can't deny\n"
        "But I've gotta let it go\n\n"
        "We found love in a hopeless place\n"
        "We found love in a hopeless place\n"
        "We found love in a hopeless place\n"
        "We found love in a hopeless place"
    ),
    ("coldplay", "yellow"): (
        "Look at the stars\n"
        "Look how they shine for you\n"
        "And everything you do\n"
        "Yeah, they were all yellow\n\n"
        "I came along\n"
        "I wrote a song for you\n"
        "And all the things you do\n"
        "And it was called Yellow\n\n"
        "So then I took my turn\n"
        "Oh, what a thing to have done\n"
        "And it was all yellow\n\n"
        "Your skin, oh yeah, your skin and bones\n"
        "Turn into something beautiful\n"
        "You know, you know I love you so\n"
        "You know I love you so"
    ),
    ("queen", "bohemian rhapsody"): (
        "Is this the real life?\n"
        "Is this just fantasy?\n"
        "Caught in a landslide\n"
        "No escape from reality\n\n"
        "Open your eyes\n"
        "Look up to the skies and see\n"
        "I'm just a poor boy, I need no sympathy\n"
        "Because it's easy come, easy go\n"
        "Little high, little low\n"
        "Anyway the wind blows\n"
        "Doesn't really matter to me, to me\n\n"
        "Mama, just killed a man\n"
        "Put a gun against his head\n"
        "Pulled my trigger, now he's dead\n"
        "Mama, life had just begun\n"
        "But now I've gone and thrown it all away"
    ),
    ("journey", "don't stop believin'"): (
        "Just a small town girl\n"
        "Livin' in a lonely world\n"
        "She took the midnight train goin' anywhere\n\n"
        "Just a city boy\n"
        "Born and raised in South Detroit\n"
        "He took the midnight train goin' anywhere\n\n"
        "A singer in a smoky room\n"
        "The smell of wine and cheap perfume\n"
        "For a smile they can share the night\n"
        "It goes on and on and on and on\n\n"
        "Don't stop believin'\n"
        "Hold on to the feelin'\n"
        "Streetlight, people\n"
        "Don't stop believin'\n"
        "Hold on!"
    ),
    ("bon jovi", "livin' on a prayer"): (
        "Tommy used to work on the docks\n"
        "Union's been on strike\n"
        "He's down on his luck, it's tough\n"
        "So tough\n\n"
        "Gina works the diner all day\n"
        "Working for her man\n"
        "She brings home her pay\n"
        "For love, mm, for love\n\n"
        "She says, we've gotta hold on to what we've got\n"
        "'Cause it doesn't make a difference\n"
        "If we make it or not\n"
        "We've got each other and that's a lot\n"
        "For love, we'll give it a shot\n\n"
        "Whoa, we're half way there\n"
        "Whoa, livin' on a prayer\n"
        "Take my hand, we'll make it I swear\n"
        "Whoa, livin' on a prayer"
    ),
}

BANNER = f"""
{MGT}{B}
   ♪ ♫   L O V E - S I N G I N G   ♫ ♪
   ──────────────────────────────────────
     Find lyrics. Sing along. Have fun!
{R}"""


# ── Lyrics fetching ──────────────────────────────────────────────────────────

def fetch_lyrics(artist: str, title: str) -> str | None:
    """Return lyrics from lyrics.ovh, falling back to the offline library."""
    try:
        url = f"{LYRICS_API}/{requests.utils.quote(artist)}/{requests.utils.quote(title)}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("lyrics")
    except requests.RequestException:
        pass

    # Offline fallback
    key = (artist.strip().lower(), title.strip().lower())
    result = OFFLINE_LIBRARY.get(key)
    if result:
        print(f"{DIM}  (showing offline lyrics — no internet connection){R}")
    return result


# ── Display ──────────────────────────────────────────────────────────────────

def print_banner():
    print(BANNER)


def print_lyrics(artist: str, title: str, lyrics: str):
    sep = f"{CYN}{B}{'─' * 54}{R}"
    print(f"\n{sep}")
    print(f"  {YLW}{B}{title.title()}{R}  {DIM}by{R}  {GRN}{B}{artist.title()}{R}")
    print(f"{sep}\n")

    for line in lyrics.strip().split("\n"):
        print(f"  {WHT}{line}{R}" if line.strip() else "")

    print(f"\n{sep}")


# ── Save ─────────────────────────────────────────────────────────────────────

def save_lyrics(artist: str, title: str, lyrics: str):
    folder = "saved_lyrics"
    os.makedirs(folder, exist_ok=True)
    safe = lambda s: s.lower().replace(" ", "_")
    path = os.path.join(folder, f"{safe(artist)}-{safe(title)}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{title.title()}  —  {artist.title()}\n")
        f.write("=" * 54 + "\n\n")
        f.write(lyrics.strip() + "\n")

    print(f"\n{GRN}Saved → {path}{R}")


# ── Interactive mode ─────────────────────────────────────────────────────────

def interactive():
    print_banner()

    while True:
        print(f"\n{YLW}Search for a song  (or type  quit  to exit){R}")

        artist = input(f"  {CYN}Artist : {R}").strip()
        if artist.lower() in ("quit", "q", "exit"):
            break

        title = input(f"  {CYN}Song   : {R}").strip()
        if title.lower() in ("quit", "q", "exit"):
            break

        if not artist or not title:
            print(f"{RED}Both artist and song title are required.{R}")
            continue

        print(f"\n  {DIM}Fetching lyrics…{R}")
        lyrics = fetch_lyrics(artist, title)

        if lyrics:
            print_lyrics(artist, title, lyrics)

            ans = input(f"\n{YLW}Save to file? (y/n): {R}").strip().lower()
            if ans == "y":
                save_lyrics(artist, title, lyrics)
        else:
            print(f"\n{RED}Couldn't find lyrics for '{title}' by '{artist}'.{R}")
            print(f"{DIM}Tip: check spelling, or try a slightly different artist/title.{R}")

        ans = input(f"\n{YLW}Search another song? (y/n): {R}").strip().lower()
        if ans != "y":
            break

    print(f"\n{MGT}Keep singing! See you next time ♪{R}\n")


# ── One-shot CLI mode ─────────────────────────────────────────────────────────

def cli_search(artist: str, title: str, save: bool):
    print(f"\n{DIM}Fetching lyrics…{R}")
    lyrics = fetch_lyrics(artist, title)

    if not lyrics:
        print(f"{RED}Lyrics not found for '{title}' by '{artist}'.{R}")
        sys.exit(1)

    print_lyrics(artist, title, lyrics)
    if save:
        save_lyrics(artist, title, lyrics)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="lyrics",
        description="Love-Singing — instant lyrics for sing-along sessions",
    )
    parser.add_argument("artist", nargs="?", help="Artist name")
    parser.add_argument("title",  nargs="?", help="Song title")
    parser.add_argument("-s", "--save", action="store_true",
                        help="Save lyrics to saved_lyrics/<artist>-<title>.txt")
    parser.add_argument("--demo", action="store_true",
                        help="Show a sample output without hitting the network")

    args = parser.parse_args()

    if args.demo:
        sample = (
            "We found love in a hopeless place\n"
            "We found love in a hopeless place\n\n"
            "Yellow diamonds in the light\n"
            "And we're standing side by side\n"
            "As your shadow crosses mine\n"
            "What it takes to come alive\n\n"
            "It's the way I'm feeling\n"
            "I just can't deny\n"
            "But I've gotta let it go\n\n"
            "We found love in a hopeless place\n"
            "We found love in a hopeless place"
        )
        print_banner()
        print_lyrics("Rihanna", "We Found Love", sample)
    elif args.artist and args.title:
        cli_search(args.artist, args.title, args.save)
    else:
        interactive()


if __name__ == "__main__":
    main()
