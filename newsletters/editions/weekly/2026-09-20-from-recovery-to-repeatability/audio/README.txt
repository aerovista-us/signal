AeroVista Signal EOW 2026-09-20 — audio drop-in contract

The HTML player expects these MP3 masters:
  01-executive-brief.mp3
  02-operating-proof.mp3
  03-next-week-focus.mp3

Transcripts/scripts live one level up in ../bytecasts/.
The player probes each MP3 before enabling playback, so the edition remains functional while masters are absent or replaced.

When masters are added:
1. Update meta.json bytecast.audioStatus and runtimes.
2. Run: python scripts/registry_v2.py refresh
3. Run: python scripts/test_registry_v2.py
4. Commit the refreshed registry record/index/catalog outputs with the MP3s.
