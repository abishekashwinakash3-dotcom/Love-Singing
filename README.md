# Love-Singing ♪

Instantly find the lyrics to any song — perfect for singing along with friends in class or anywhere.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Interactive mode (recommended for sing-alongs)
```bash
python lyrics.py
```
You'll be prompted to enter the artist and song title, and the lyrics will be printed in your terminal — ready to sing along!

### One-shot mode
```bash
python lyrics.py "Ed Sheeran" "Shape of You"
```

### Save lyrics to a file (great for offline use)
```bash
python lyrics.py "Coldplay" "Yellow" --save
# saved to saved_lyrics/coldplay-yellow.txt
```

## Features

- Free, no API key needed (uses [lyrics.ovh](https://lyricsovh.docs.apiary.io/))
- Clean, readable terminal output — easy to read while singing
- Save lyrics as `.txt` files for offline sing-alongs
- Works on Windows, Mac, and Linux
