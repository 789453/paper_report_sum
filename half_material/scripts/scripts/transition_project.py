from pathlib import Path
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'archive'/'knowledge-is-power_2026-11-16'
paths=['paper/knowledge-is-power','output/Knowledge_is_Power_LaTeX源码.zip','output/pdf/Knowledge_is_Power_中文组会报告.pdf','output/封面预览.png','output/论文源码包说明.txt','docs/本次论文版本与证据说明.md','qa/final','qa/portable_compile/paper','qa/验收记录.md','scripts/export_notes_and_evidence.py','scripts/extract_paper_figures.py','scripts/prepare_materials.py','scripts/finalize_delivery.py','sources/author_presentation_2022.pdf','sources/author_presentation_2022.txt','sources/knowledge_2022_fulltext.txt','sources/knowledge_2022_january.pdf','sources/knowledge_ssrn_supplied.pdf','sources/knowledge_supplied_fulltext.txt','sources/supplied_text_initial_extract.txt','sources/manifest.json','sources/access_failures']
manifest=[]
for rel in paths:
    src=(ROOT/rel).resolve(); dst=(DEST/rel).resolve()
    assert src.is_relative_to(ROOT.resolve()) and dst.is_relative_to(DEST.resolve())
    if src.exists() and not dst.exists():
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(src),str(dst)); manifest.append(rel)
DEST.mkdir(parents=True,exist_ok=True)
(DEST/'归档说明.json').write_text(json.dumps({'date':'2026-11-16','reason':'用户更换选题；旧论文材料退出当前交付，保留可追溯记录','moved':manifest,'retained':['vendor','reusable','skills','通用模板及排版来源']},ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'On the Information Set of Individual Investors.pdf'
out=ROOT/'sources'/'information-set';out.mkdir(parents=True,exist_ok=True)
shutil.copy2(p,out/'paper.pdf')
(out/'version.json').write_text(json.dumps({'title':'On the Information Set of Individual Investors','authors':['Toomas Laarits','Jeffrey Wurgler'],'version':'2026-04-27','status':'working paper','pages':70,'input':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'SSRN':'5187645','older_NBER_title':'The Research Behavior of Individual Investors','older_NBER_doi':'10.3386/w33625','note':'所有主文数值以本地70页2026-04-27稿为准，不混用2025年旧题稿。'},ensure_ascii=False,indent=2),encoding='utf-8')
print('archived',len(manifest),'paths; source registered')
