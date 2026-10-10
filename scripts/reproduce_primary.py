"""Portable adapters of project primary_print_alignment/verify_primary_signature.
Pinned glyph/code assignments are inputs; formula and comparison are recomputed.
No source images, remote tables, or meaning-based repair are consulted.
"""
import csv,sys,bisect,random,json
from pathlib import Path
from three_kana_formula import code_to_triple, triple_to_code,S
R=Path(__file__).resolve().parent.parent
OUT=R/'outputs';OUT.mkdir(exist_ok=True)
def rows(name):
 with (R/'data'/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def save(name,data):
 with (OUT/name).open('w',encoding='utf8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t');w.writeheader();w.writerows(data)
gold=rows('primary107_vs_raw591.tsv')
text=''.join(x.strip()for x in (R/'data/primary_1916_welcome_telegram.txt').read_text().splitlines()if not x.startswith('#'))
assert len(text)==len(gold)==107
lookup={}
for x in gold:
 c=x['lookup_variant'] or x['printed_glyph'];n=int(x['code'])
 assert c not in lookup or lookup[c]==n
 lookup[c]=n
roman={}
for a,k in S.items():roman.setdefault(k,a)
roman.update({'シ':'shi','チ':'chi','ツ':'tsu','フ':'fu','ヱ':'e'})
raw=''.join(x['source_group']for x in rows('reading_order.tsv'))
expected='';ends=[];result=[]
for i,c in enumerate(text):
 key={'刪':'删'}.get(c,c);n=lookup[key];kana=code_to_triple(n);word=''.join(roman[k]for k in kana)
 result.append(dict(print_index=str(i+1),printed_glyph=c,lookup_variant=key if key!=c else '',code=f'{n:04d}',reencoded_kana=kana,reencoded_roman=word,expected_start=str(len(expected))))
 expected+=word;ends.append(len(expected))
a=raw[:591];m,n=len(expected),len(a);D=[[0]*(n+1)for _ in range(m+1)]
for i in range(m+1):D[i][0]=i
for j in range(n+1):D[0][j]=j
for i in range(1,m+1):
 for j in range(1,n+1):D[i][j]=min(D[i-1][j-1]+(expected[i-1]!=a[j-1]),D[i-1][j]+1,D[i][j-1]+1)
i,j=m,n;ops=[]
while i or j:
 if i and j and D[i][j]==D[i-1][j-1]+(expected[i-1]!=a[j-1]):ops.append((i-1,j-1,'match'if expected[i-1]==a[j-1]else'sub'));i-=1;j-=1
 elif i and D[i][j]==D[i-1][j]+1:ops.append((i-1,None,'missing_from_source'));i-=1
 else:ops.append((i,j-1,'extra_in_source'));j-=1
ops.reverse();slots=[[]for _ in result];changes=[[]for _ in result]
for x,y,op in ops:
 z=min(bisect.bisect_right(ends,x),len(result)-1)
 if y is not None:slots[z].append(y)
 if op!='match':changes[z].append(f'{op}:expected{x}:source{y}')
cursor=0
for x,pos,ch in zip(result,slots,changes):
 if pos:assert pos==list(range(cursor,cursor+len(pos)))
 end=cursor+len(pos)
 x.update(source_start=str(cursor),source_end=str(end),raw_source=a[cursor:end],raw_exact=str(a[cursor:end]==x['reencoded_roman']),edit_events=';'.join(ch),status='diagnostic_global_alignment_not_source_emendation');cursor=end
assert result==gold, 'Recomputed alignment differs from pinned prior output'
assert (m,n,D[m][n],sum(x['raw_exact']=='True'for x in result))==(593,591,63,73)
save('primary107_vs_raw591.tsv',result)
sig=rows('independent_primary_signature.tsv');codes={x['printed_glyph']:int(x['code'])for x in gold}
for x in sig:
 n=codes[x['independent_print_glyph']];kana=code_to_triple(n);word=''.join(roman[k]for k in kana)
 assert x['printed_glyph_code']==f'{n:04d}' and x['reencoded_kana']==kana and x['reencoded_roman']==word
 assert raw[int(x['start']):int(x['end'])]==x['raw_source']
 assert x['raw_exact']==str(x['raw_source']==word)
 assert x['worksheet_formula_exact']==str(x['prior_formula_code']==f'{n:04d}')
assert sum(x['raw_exact']=='True'for x in sig)==5
assert sum(x['worksheet_formula_exact']=='True'for x in sig)==6
rng=random.Random(20261007);expect=[x['reencoded_roman']for x in sig];source=[x['raw_source']for x in sig];controls=[]
for i in range(100):
 z=expect[:];rng.shuffle(z);controls.append(dict(permutation=str(i),exact_raw_slots=str(sum(x==y for x,y in zip(source,z)))))
assert controls==rows('primary_signature_negative_controls.tsv')
save('primary_signature_negative_controls.tsv',controls)
nums=[int(x['exact_raw_slots'])for x in controls]
summary=dict(printed_glyphs=107,expected_roman_letters=m,raw_prefix_positions=len(a),edit_distance=D[m][len(a)],exact_aligned_words=73,signature_raw_exact=5,signature_worksheet_exact=6,shuffle_count=100,shuffle_mean=sum(nums)/100,shuffle_max=max(nums),interpretation='diagnostic comparison, not plaintext accuracy or uniqueness')
assert summary['shuffle_mean']==.72 and summary['shuffle_max']==5
(OUT/'primary_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
