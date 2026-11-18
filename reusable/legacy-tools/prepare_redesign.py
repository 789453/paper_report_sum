from pathlib import Path
import json, shutil, hashlib
import pymupdf as fitz
R=Path(__file__).resolve().parents[1]
P=R/'paper/information-set-redesign-20261117'; A=P/'assets'; A.mkdir(exist_ok=True)
Q=R/'qa/information-set-redesign-20261117'; Q.mkdir(exist_ok=True)
for name in ['ruc-research.sty','RenminUniv.sty']:
    shutil.copy2(R/'paper/information-set'/name,P/name)
for f in (R/'paper/information-set/assets').glob('*'):
    if f.suffix in ['.png','.pdf']: shutil.copy2(f,A/f.name)
doc=fitz.open(R/'sources/information-set/paper.pdf')
clip=fitz.Rect(52,70,552,390)
out=fitz.open();out.new_page(width=clip.width,height=clip.height)
out[0].show_pdf_page(out[0].rect,doc,56,clip=clip)
out.save(A/'web_compare.pdf');out.close()
doc[56].get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,alpha=False).save(A/'web_compare.png')
assets=json.loads((R/'paper/information-set/assets_manifest.json').read_text(encoding='utf-8'))
assets['sell_paths']['pdf_clip_rect']=[405,134,665,311]
for name, meta in assets.items():
    pg=meta['paper_pdf_page']-1; rc=fitz.Rect(meta['pdf_clip_rect'])
    cropped=fitz.open();cropped.new_page(width=rc.width,height=rc.height)
    cropped[0].show_pdf_page(cropped[0].rect,doc,pg,clip=rc)
    target=A/(name+'.pdf')
    # Replace only this task's derived asset; the source PDF and old project stay untouched.
    tmp=A/(name+'.new.pdf');cropped.save(tmp);cropped.close();tmp.replace(target)
    doc[pg].get_pixmap(matrix=fitz.Matrix(3,3),clip=rc,alpha=False).save(A/(name+'.png'))
assets['web_compare']={'paper_pdf_page':57,'pdf_clip_rect':list(clip),'method':'original figure upper region; no inferred data'}
(P/'assets_manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
slides=json.loads((P/'slides.json').read_text(encoding='utf-8'))
snap=Q/'revisions';snap.mkdir(exist_ok=True)
if not (snap/'r0_content_draft.json').exists(): shutil.copy2(P/'slides.json',snap/'r0_content_draft.json')
count=sum(sum('\u4e00'<=c<='\u9fff' for c in s['speech']) for s in slides)
print(json.dumps({'slides':len(slides),'speech_chinese_chars':count,'planned_seconds':sum(s['seconds'] for s in slides)},ensure_ascii=False))
plan=['# 新版逐页论证设计','', '45页连续正文；封面计入物理页数。无讨论尾页及附录。','',
      '|页|页面|讲述任务|证据|秒|','|---:|---|---|---|---:|']
for s in slides:plan.append(f"|{s['page']}|{s['title'].replace(chr(10),' ')}|{s['purpose']}|{s['source']}|{s['seconds']}|")
(P/'逐页论证设计.md').write_text('\n'.join(plan),encoding='utf-8')
sources={'paper':{'path':'sources/information-set/paper.pdf','version':'2026-04-27','pages':70,
  'sha256':hashlib.sha256((R/'sources/information-set/paper.pdf').read_bytes()).hexdigest()},
  'reference':{'path':'raw_reference/chatgpt-export_论文深度讲解.md','role':'问题和解释思路；包含被后文纠正的2025旧稿数字，不作原始实证证据'},
  'web_checked_on':'2026-11-17','web':[
    {'url':'https://sites.google.com/view/toomaslaarits/research','supports':'Laarits为NYU Stern金融助理教授；本篇R&R，April 2026；未公开期刊'},
    {'url':'https://pages.stern.nyu.edu/jwurgler/main.htm','supports':'Wurgler为Nomura Professor；BW情绪及Comovement代表作'},
    {'url':'https://pages.stern.nyu.edu/~jwurgler/pdfs/cvshort8.pdf','supports':'历史CV列JFE与Management Science Associate Editor，历史任职而非当前职务'},
    {'url':'https://www.nber.org/papers/w33625','supports':'旧题名及NBER WP 33625；本轮全文打开403，题名同时由已归档原文与搜索记录核对'},
    {'url':'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5187645','supports':'SSRN记录标识；全文数字均来自用户本地完整稿，不依赖403页面'}],
  'native_skills':'保留vendor/community-skills-2026-11-16及固定commit/SHA清单；本地新增规范与原生文件分开。',
  'explicit_corrections':[
    'NTU应为NYU；Laarits是助理教授，Wurgler是Nomura讲席教授。',
    '本篇工作稿R&R，但未公开期刊，不推测投稿。',
    '5.7分钟为50户家庭内比率的横截面中位数。',
    '新闻归因用部分可见新闻标题与RavenPack匹配；讨论板才明确使用当代Reddit。',
    '理性预期不要求同质信息；讲解公式不是本文估计模型。',
    'PC2投机指标参与构造，C/D分组也使用PC2，不是独立因果检验。']}
(P/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
print('prepared sources, assets and content snapshot')
