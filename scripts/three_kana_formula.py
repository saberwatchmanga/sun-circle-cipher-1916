"""Reproduce Tomokiyo's Sept 2026 published inverse formula for 3-kana code.

Reference: https://cryptiana.web.fc2.com/code/chinesecrypto_e2.htm
This is application of a published key, not a new key recovery. Source key
has uncertainties around period romanization and some worksheet readings.
"""
import csv,sys
from pathlib import Path
FIRST='アカサタナハマヤラワイキシチニヒミリヰウクスツヌフムユルエケセテネヘメレヱオコソトノホモヨロ'
SECOND='アイウエオカキクケコ'
THIRD='ホヘフヒハノネヌニナトテツチタソセスシサ'
assert len(FIRST)==46 and len(SECOND)==10 and len(THIRD)==20

def triple_to_code(t):
 a,b,c=t
 if a not in FIRST or b not in SECOND or c not in THIRD:return None
 return 200*FIRST.index(a)+10*THIRD.index(c)+SECOND.index(b)+1

def code_to_triple(n):
 if not 1 <= n <= 9200:raise ValueError(n)
 a=(n-1)//200;b=(n-1)%10;c=((n-1)//10)%20
 return FIRST[a]+SECOND[b]+THIRD[c]

def published_excel_code_to_triple(n):
 """Literal Sept. 2026 article formula; differs at exact multiples of 200.

 The article uses INT(code/200)+1 for the first kana. Its observed examples
 do not establish how boundary values were historically treated.
 """
 if not 1 <= n <= 9199:raise ValueError(n)
 a=n//200;b=(n-1)%10;c=((n-1)//10)%20
 return FIRST[a]+SECOND[b]+THIRD[c]

# Romanizations in original are an observed channel, not a 1:1 key.
S={}
for cons,kana in [('','ア'),('k','カ'),('s','サ'),('t','タ'),('n','ナ'),('h','ハ'),('m','マ'),('y','ヤ'),('r','ラ'),('w','ワ')]:
 for v,off in zip('aiueo',range(5)):
  ko='アイウエオ' if cons=='' else {'k':'カキクケコ','s':'サシスセソ','t':'タチツテト','n':'ナニヌネノ','h':'ハヒフヘホ','m':'マミムメモ','y':'ヤイユエヨ','r':'ラリルレロ','w':'ワヰウヱヲ'}[cons]
  if len(ko)==5:S[cons+v]=ko[off]
# Preserve period spelling variants in input parser but do not choose silently.
S.update({'shi':'シ','chi':'チ','tsu':'ツ','fu':'フ','wi':'ヰ','we':'ヱ','wo':'ヲ','si':'シ','ti':'チ','tu':'ツ','hu':'フ'})
# Match longest first; `n` is deliberately excluded because it is ambiguous.
TOK=sorted(S,key=len,reverse=True)

def parse_greedy(s):
 out=[];i=0
 while i<len(s):
  t=next((x for x in TOK if s.startswith(x,i)),None)
  if not t:return out,i
  out.append((S[t],t,i));i+=len(t)
 return out,i

