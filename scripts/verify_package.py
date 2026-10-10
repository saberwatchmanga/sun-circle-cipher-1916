"""Verify bounded release integrity and structural invariants; no network."""
import json,csv,hashlib
from pathlib import Path
from three_kana_formula import code_to_triple,triple_to_code
R=Path(__file__).resolve().parent.parent
manifest=json.loads((R/'provenance/PACKAGE_SHA256.json').read_text())
for name,sha in manifest.items():
 p=R/name;assert p.is_file() and not p.is_symlink()
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha, name
# Required files are pinned; ignored generated outputs are not release inputs.
def rows(name):
 with (R/name).open(newline='',encoding='utf8')as f:return list(csv.DictReader(f,delimiter='\t'))
raw=''.join(x['source_group']for x in rows('data/reading_order.tsv'))
assert len(raw)==1271 and len(raw.replace('[','').replace(']',''))==1265
ledger=rows('data/whole_source_alignment.tsv');cursor=0
for x in ledger:
 a,b=int(x['start']),int(x['end']);assert a==cursor and b>a and x['raw_source']==raw[a:b];cursor=b
assert cursor==len(raw)
for n in range(1,9201):assert triple_to_code(code_to_triple(n))==n
f=R/'data/hypotheses/PREDICTIONS_FROZEN_20261009.json'
assert hashlib.sha256(f.read_bytes()).hexdigest()=='ccdde0e8d13be171069529573fd6c49723d07ca13f73ebc49605b0d2914e3946'
coverage=rows('data/round4/PAGE_COVERAGE.tsv');assert len(coverage)==259
units=json.loads((R/'data/round4/UNIT_COVERAGE.json').read_text())
for u in units:
 subset=[x for x in coverage if x['archive_id']==u['archive_id']]
 assert len(subset)==u['pages']
 assert [int(x['pdf_page'])for x in subset]==list(range(1,u['pages']+1))
 assert [int(x['film_frame'])for x in subset]==list(range(u['film_start'],u['film_start']+u['pages']))
assert all(x['accepted_independent_evidence']=='no'for x in coverage)
print(json.dumps(dict(pinned_files_verified=len(manifest),literal_positions=len(raw),ledger_intervals=len(ledger),formula_round_trips=9200,round4_frames=len(coverage),frozen_predictions_unchanged=True),indent=2))
