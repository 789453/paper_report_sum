from pathlib import Path
import requests,json,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1];OUT=R/'vendor'/'community-skills-2026-11-16';OUT.mkdir(parents=True,exist_ok=True)
TARGETS=[
('S01','wenlzhang/beamer-skill','main','SKILL.md'),
('S02','Noi1r/beamer-skill','main','beamer/SKILL.md'),
('S03','K-Dense-AI/claude-scientific-writer','main','.claude/skills/scientific-slides/SKILL.md'),
('S04','aeghnnsw/cc-toolkit','master','creator-skills/skills/sci-slides/SKILL.md'),
('S05','DELONG-L/Research-Presentation-Skill','main','research-presentation/SKILL.md'),
('S06','Yash-Kavaiya/research-scholar-agent-skills','main','skills/paper-to-slides/SKILL.md'),
('S07','Faust-Donf/beamer-academic','main','SKILL.md'),
('S08','thanhlamauto/weekly-research-slides','main','SKILL.md'),
('S09','hanlulong/econ-slides-skill','main','skills/econ-slides/SKILL.md'),
('S10','nsinha00/academic-beamer-skill','main','SKILL.md'),
('H01','blader/humanizer','main','SKILL.md'),
('H02','op7418/Humanizer-zh','main','SKILL.md'),
('H03','neuromechanist/research-skills','main','plugins/manuscript/skills/humanizer/SKILL.md'),
('H04','ai-zixun/humanizer-zh','main','SKILL.md')]
def get_one(t):
 ident,repo,branch,path=t; folder=OUT/ident;folder.mkdir(exist_ok=True)
 sess=requests.Session();sess.headers['User-Agent']='Academic-slide-source-review/1.0'
 from requests.adapters import HTTPAdapter
 from urllib3.util.retry import Retry
 sess.mount('https://',HTTPAdapter(max_retries=Retry(total=3,backoff_factor=.5)))
 api=sess.get(f'https://api.github.com/repos/{repo}/commits/{branch}',timeout=40)
 sha=api.json().get('sha',branch) if api.ok else branch
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
 res=sess.get(url,timeout=50)
 if not res.ok:
  tree=sess.get(f'https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1',timeout=50)
  term='research-presentation' if ident=='S10' else 'research-presentations'
  matches=[x['path'] for x in tree.json().get('tree',[]) if x['path'].endswith('SKILL.md') and term in x['path']]
  if matches:path=matches[0];url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}';res=sess.get(url,timeout=50)
 res.raise_for_status();(folder/'SKILL.md').write_bytes(res.content)
 lic='not located';licpath=''
 for name in ['LICENSE','LICENSE.md','LICENSE.txt']:
  q=sess.get(f'https://raw.githubusercontent.com/{repo}/{sha}/{name}',timeout=30)
  if q.ok:(folder/name).write_bytes(q.content);licpath=name;lic=q.text[:120].strip();break
 meta={'id':ident,'category':'academic-slides' if ident[0]=='S' else 'anti-AI-prose','repository':repo,'commit':sha,'path':path,'url':f'https://github.com/{repo}/blob/{sha}/{path}','sha256':hashlib.sha256(res.content).hexdigest(),'bytes':len(res.content),'license_file':licpath,'license_preview':lic,'retrieved':'2026-11-16'}
 (folder/'source.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');return meta
if __name__=='__main__':
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  jobs={ex.submit(get_one,t):t[0] for t in TARGETS}
  for f in concurrent.futures.as_completed(jobs):
   try:r=f.result();results.append(r);print(r['id'],r['repository'],r['bytes'])
   except Exception as e:print('FAIL',jobs[f],str(e))
 (OUT/'manifest.json').write_text(json.dumps(sorted(results,key=lambda x:x['id']),ensure_ascii=False,indent=2),encoding='utf-8')
