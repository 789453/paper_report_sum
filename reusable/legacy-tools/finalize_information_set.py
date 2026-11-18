from pathlib import Path
import re,json,shutil,zipfile,hashlib,ast
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';O=R/'output/information-set';O.mkdir(parents=True,exist_ok=True)
shutil.copy2(P/'build/main.pdf',O/'01_组会报告_40页.pdf')
# Final, rather than round-1, frame records.
tex=(P/'main.tex').read_text(encoding='utf-8');plan=json.loads((P/'slide_plan.json').read_text(encoding='utf-8'))
chunks=re.split(r'% Physical page \d+\n',tex)[1:]
manifest=[dict(physical_page=x['physical_page'],title=x['title'],main=x['main'],seconds=x['seconds'],tex=c.split('\\end{frame}')[0]+'\\end{frame}' if '\\end{frame}' in c else c.split('\\section')[0].strip()) for x,c in zip(plan,chunks)]
(P/'frame_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
prep=(R/'scripts/prepare_information_set.py').read_text(encoding='utf-8');crops=ast.literal_eval(re.search(r'crops=(\{.*?\})\nfor',prep,re.S)[1])
used=set(re.findall(r'assets/([A-Za-z_]+)\.pdf',tex))
(P/'assets_manifest.json').write_text(json.dumps({n:{'paper_pdf_page':crops[n][0],'pdf_clip_rect':crops[n][1],'method':'vector PDF crop; no inferred data'} for n in sorted(used)},ensure_ascii=False,indent=2),encoding='utf-8')
notice='''# 来源与使用说明

RenminUniv.sty来自RUC-Beamer-Theme，原仓库及许可保留。上游commit：cb04e44c9f66ba000a63615993d052ed389200ea。ruc-research.sty为本项目派生层，清空背景和封面校徽，保留原酒红色、楷体与4:3样式。

论文图形来自用户提供的Laarits与Wurgler（2026-04-27）70页工作稿。assets_manifest.json记录原图页码和裁剪坐标。图形版权不因主题的MIT许可而改变；本包用于本次学术阅读汇报。

完整工作流的10份slides skill及4份去AI味skill来源在项目docs/社区skills整合与执行规则.md，固定版本见vendor/community-skills-2026-11-16/manifest.json。未把许可未明的上游全文并入本源码包。
'''
(P/'NOTICE.md').write_text(notice,encoding='utf-8')
lic=R/'vendor/RUC-Beamer-Theme/LICENSE'
if lic.exists():shutil.copy2(lic,P/'LICENSE_RUC_TEMPLATE')
codezip=O/'05_LaTeX可编译工程.zip'
with zipfile.ZipFile(codezip,'w',zipfile.ZIP_DEFLATED) as z:
 for n in ['main.tex','ruc-research.sty','RenminUniv.sty','README.md','NOTICE.md','LICENSE_RUC_TEMPLATE','assets_manifest.json','source_version.json','evidence.csv','slide_plan.json','frame_manifest.json','讲稿正文.json','逐页讲稿.md','专业问答.md','研究分析.md']:
  if (P/n).exists():z.write(P/n,n)
 for n in sorted(used):z.write(P/'assets'/(n+'.pdf'),'assets/'+n+'.pdf')
with zipfile.ZipFile(codezip) as z:
 bad=z.testzip();assert bad is None
 test=(R/'qa/information-set/portable_compile').resolve();assert test.is_relative_to(R.resolve());test.mkdir(parents=True,exist_ok=True)
 for n in z.namelist():assert (test/n).resolve().is_relative_to(test)
 z.extractall(test)
shutil.copy2(R/'docs/社区skills整合与执行规则.md',O/'06_社区skill来源与执行规则.md')
shutil.copy2(R/'qa/information-set/revisions/五轮修订记录.md',O/'07_五轮修订记录.md')
shutil.copy2(R/'qa/information-set/验收记录.md',O/'08_验收记录.md')
for n in ['main.tex','main.pdf','main.log']:shutil.copy2(P/n if n.endswith('.tex') else P/'build'/n,R/'qa/information-set/revisions/r5_layout'/n)
metrics=json.loads((O/'delivery_metrics.json').read_text(encoding='utf-8'))
metrics['docx_pages']={'speech':11,'qa':9,'analysis':15}
metrics['files_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix in ['.docx','.pdf','.zip'] and '全部' not in p.name}
(O/'delivery_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
allzip=O/'全部汇报材料.zip'
with zipfile.ZipFile(allzip,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(O.iterdir()):
  if p.is_file() and p!=allzip:z.write(p,p.name)
 for p in (R/'skills/academic-paper-beamer').rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,'skill/academic-paper-beamer/'+p.relative_to(R/'skills/academic-paper-beamer').as_posix())
print('packaged four deliverables, source project, skill rules and revision record')
print('portable directory:',test)
