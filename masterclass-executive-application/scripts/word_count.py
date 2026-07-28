import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python scripts/word_count.py <file>")
    sys.exit(1)

text = Path(sys.argv[1]).read_text(encoding="utf-8")
words = text.replace("—", " ").replace("/", " ").split()
print(f"Word count: {len(words)}")
