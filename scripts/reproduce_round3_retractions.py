import json,csv,sys
from pathlib import Path
def distance(a,b):
 d=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  e=[i]
  for j,y in enumerate(b,1):e.append(min(e[-1]+1,d[j]+1,d[j-1]+(x!=y)))
  d=e
 return d[-1]
FIRST='アカサタナハマヤラワイキシチニヒミリヰウクスツヌフムユルエケセテネヘメレヱオコソトノホモヨロ'
SECOND='アイウエオカキクケコ';THIRD='ホヘフヒハノネヌニナトテツチタソセスシサ'
def kana(n):
 x=n-1;return FIRST[x//200]+SECOND[x%10]+THIRD[(x%200)//10]
assert kana(7300)=='ヱコナ' and kana(5700)=='エコナ'
roman={'ヱ':'e','エ':'e','コ':'ko','ナ':'na'}
assert ''.join(roman[c] for c in kana(7300))==''.join(roman[c] for c in kana(5700))=='ekona'
b=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
literal=''.join(r['source_group'] for r in csv.DictReader((b/'data/reading_order.tsv').open(),delimiter='\t'))
raw=literal.replace('[','').replace(']','')
assert len(raw)==1265 and raw[896:913]=='kaesomikanuteashi'
pattern='kaesomikanuteasu'
tests=[dict(stripped_start=896,stripped_end=e,target=raw[896:e],edit_distance=distance(pattern,raw[896:e]),complete_last_codeword=e==913,literal_start=898,literal_end=e+2) for e in [911,912,913]]
assert [r['edit_distance'] for r in tests]==[1,1,2]
print(json.dumps({'formula':'200*FIRST.index(k1)+10*THIRD.index(k3)+SECOND.index(k2)+1','distinct_kana':{'韶7300':kana(7300),'蘿5700':kana(5700)},'collapsed_roman':'ekona','pattern':pattern,'boundary_tests':tests},ensure_ascii=False,indent=2))
