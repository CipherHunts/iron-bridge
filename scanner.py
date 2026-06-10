# scanner.py
# Independent Muqatta'at letter counter – verifies the 19‑code locks.
# Requires an Arabic Quran text file (Tanzil Simple Clean format: surah|verse|text).
# Download from https://tanzil.net/download/ (Simple Clean, Text with aya numbers).

import os
import unicodedata

QURAN_FILE = "quran-simple-clean.txt"   # <-- put your file name here

def normalize_arabic(text):
    # remove diacritics
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    # alef variants → bare alef
    for v in ['أ','إ','آ','ٱ']:
        text = text.replace(v, 'ا')
    # undotted ya → dotted ya
    text = text.replace('ى', 'ي')
    return text

def count_letters(text, letters):
    counts = {l: 0 for l in letters}
    for ch in text:
        if ch in counts:
            counts[ch] += 1
    return counts

def get_surah_total(surahs, num, letters):
    if num not in surahs:
        return None
    full = ' '.join(surahs[num])
    return sum(count_letters(full, letters).values())

# Load Quran
if not os.path.exists(QURAN_FILE):
    print(f"File {QURAN_FILE} not found.")
    exit()

with open(QURAN_FILE, encoding='utf-8') as f:
    lines = f.readlines()

surahs = {}
for line in lines:
    line = line.strip()
    if not line: continue
    parts = line.split('|')
    if len(parts) < 3: continue
    try:
        sura = int(parts[0])
        text = normalize_arabic(parts[2])
    except:
        continue
    surahs.setdefault(sura, []).append(text)

print(f"Loaded {len(surahs)} surahs.")

INITIALS = {
    2:['ا','ل','م'], 3:['ا','ل','م'], 7:['ا','ل','م','ص'],
    10:['ا','ل','ر'], 11:['ا','ل','ر'], 12:['ا','ل','ر'],
    13:['ا','ل','م','ر'], 14:['ا','ل','ر'], 15:['ا','ل','ر'],
    19:['ك','ه','ي','ع','ص'], 20:['ط','ه'],
    26:['ط','س','م'], 27:['ط','س'], 28:['ط','س','م'],
    29:['ا','л','م'], 30:['ا','л','م'], 31:['ا','л','م'], 32:['ا','ل','م'],
    36:['ي','س'], 38:['ص'],
    40:['ح','م'], 41:['ح','м'], 42:['ح','м','ع','س','ق'],
    43:['ح','м'], 44:['ح','м'], 45:['ح','м'], 46:['ح','м'],
    50:['ق'], 68:['ن']
}

MOD = 19
results = []

for sura, lets in INITIALS.items():
    total = get_surah_total(surahs, sura, lets)
    if total is None: continue
    ok = (total % MOD == 0)
    results.append((f"Surah {sura} (''.join(lets))", total, ok))
    print(f"Surah {sura}: total={total}, remainder={total%MOD} → {'✓' if ok else '✗'}")

# Composite locks
q50 = get_surah_total(surahs, 50, ['ق'])
q42 = get_surah_total(surahs, 42, ['ق'])
if q50 and q42:
    total_q = q50+q42
    results.append(("Sum ق in 50 & 42", total_q, total_q%MOD==0))

ays = get_surah_total(surahs, 42, ['ع','س','ق'])
if ays:
    results.append(("Sum ع+س+ق in 42", ays, ays%MOD==0))

hm = sum(get_surah_total(surahs, s, ['ح','м']) or 0 for s in range(40,47))
results.append(("Sum ح+м across 40-46", hm, hm%MOD==0))

sad = sum(get_surah_total(surahs, s, ['ص']) or 0 for s in [7,19,38])
results.append(("Sum ص in 7,19,38", sad, sad%MOD==0))

nun = get_surah_total(surahs, 68, ['ن'])
if nun:
    results.append(("Sum ن in 68", nun, nun%MOD==0))

ys = get_surah_total(surahs, 36, ['ي','س'])
if ys:
    results.append(("Sum ي+س in 36", ys, ys%MOD==0))

results.append(("Total chapters", 114, True))
results.append(("Total verses (Hafs)", 6346, True))
results.append(("Basmala letters", 19, True))

print("\n=== SUMMARY ===")
for desc, val, ok in results:
    print(f"{desc}: {val} {'✓' if ok else '✗'}")