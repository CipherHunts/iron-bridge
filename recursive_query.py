# recursive_query.py
# Feeds a question into a loop using 57, 108, 19, and maps residues to Arabic letters.

abjad = {
    'ا':1,'ب':2,'ج':3,'د':4,'ه':5,'و':6,'ز':7,'ح':8,'ط':9,
    'ي':10,'ك':20,'ل':30,'م':40,'ن':50,'س':60,'ع':70,'ف':80,'ص':90,
    'ق':100,'ر':200,'ش':300,'ت':400,'ث':500,'خ':600,'ذ':700,'ض':800,'ظ':900,'غ':1000
}
res2char = {i: chr(ord('ا')+i-1) for i in range(1,19)}  # 1→ا .. 18→غ
res2char[0] = 'ق'  # 0 (19 mod) → ق

question = "ما العلاقة بين الكون والإنسان"
values = [abjad.get(ch,0) for ch in question if ch in abjad]
print("Initial values:", values)

for gen in range(20):
    residues = [( (v+57+108) % 19 ) for v in values]
    letters = ''.join(res2char[r] for r in residues)
    qcnt = letters.count('ق')
    print(f"Gen {gen:2d}: {letters[:30]}...  ق count={qcnt}")
    values = [abjad.get(ch,0) for ch in letters]