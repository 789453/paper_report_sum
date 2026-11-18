from pathlib import Path,PurePosixPath
import requests,json,concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
R=Path(__file__).resolve().parents[1]/'vendor'/'community-skills-2026-11-16'
files={
'S09':['references/existing-deck-workflow.md','references/beamer-layout-mechanics.md','references/slide-rules.md','references/exhibit-surgery.md','references/source-integrity.md','references/speaker-script.md','references/talk-structures.md','scripts/compile_deck.py','scripts/check_deck.py'],
'S04':['references/slide-text.md','references/design.md','scripts/lint_slides.py'],
'S07':['references/writing-style.md'],
'S03':['references/presentation_structure.md','references/common_pitfalls.md','references/presentation_workflow.md'],
'S05':['references/pdf-input.md','references/evidence-and-citations.md','references/presentation-design.md'],
'S06':['references/talk-design-guide.md'],
'S10':['content_guidelines.md','slide_patterns.md'],
'H04':['references/patterns.md'],
}
def one(ident,rel):
 m=json.loads((R/ident/'source.json').read_text(encoding='utf-8'));base=str(PurePosixPath(m['path']).parent)
 path=rel if base=='.' else base+'/'+rel
 url=f"https://raw.githubusercontent.com/{m['repository']}/{m['commit']}/{path}"
 s=requests.Session();s.mount('https://',HTTPAdapter(max_retries=Retry(total=3,backoff_factor=.5)))
 r=s.get(url,timeout=45)
 if r.ok:
  dst=R/ident/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(r.content)
 return ident,rel,r.status_code
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for x in ex.map(lambda x:one(*x),[(i,p) for i,ls in files.items() for p in ls]):print(*x)
