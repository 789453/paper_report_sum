from pathlib import Path
import json, re, zipfile, hashlib, shutil, xml.etree.ElementTree as ET
import pymupdf as fitz
from PIL import Image, ImageOps, ImageDraw

R=Path(__file__).resolve().parents[1]; P=R/'paper/information-set-redesign-20261117'
O=R/'output/information-set-redesign-20261117'; Q=R/'qa/information-set-redesign-20261117'
S=json.loads((P/'slides.json').read_text(encoding='utf-8'))
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
native=O/'01_45页报告.pptx'
with zipfile.ZipFile(native) as z:
    sn=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda x:int(re.search(r'(\d+)\.xml',x)[1]))
    assert len(sn)==45
    table_owners=[]; image_owners=[]
    for i,n in enumerate(sn):
        root=ET.fromstring(z.read(n));tx=''.join(root.itertext())
        if root.findall('.//a:tbl',NS):table_owners.append(i+1)
        if root.findall('.//p:pic',NS):image_owners.append(i+1)
        note=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i+1}.xml'))
        text=''.join(x.text or '' for x in note.findall('.//a:t',NS))
        assert S[i]['speech'] in text, f'notes mismatch {i+1}'
    assert image_owners==[s['page'] for s in S if s['asset']],image_owners
    assert table_owners==[s['page'] for s in S if s['table']],table_owners
    media=[n for n in z.namelist() if n.startswith('ppt/media/')]
    assert len(media)>=11
pdf=fitz.open(O/'01_组会报告_45页.pdf');assert len(pdf)==45
boundary=[]
for i,p in enumerate(pdf):
    text=p.get_text();assert 'elax' not in text,f'stray token {i+1}'
    assert len(text)>50
    if i:assert f'{i+1}/45' in text.replace(' ',''),f'page number {i+1}'
    for w in p.get_text('words'):
        if w[0]<-.5 or w[1]<-.5 or w[2]>p.rect.width+.5 or w[3]>p.rect.height+.5:boundary.append([i+1,list(w[:4]),w[4]])
assert not boundary,boundary
log=(P/'build/main.log').read_text(encoding='utf-8',errors='replace')
warnings=[x for x in log.splitlines() if re.search(r'Overfull|Missing character|undefined|Font Warning|^!',x,re.I)]
assert not warnings,warnings
assert '\\appendix' not in (P/'main.tex').read_text(encoding='utf-8')
manifest=json.loads((R/'skills/academic-paper-beamer/references/community-source-manifest.json').read_text(encoding='utf-8'))
skills=[]
for m in manifest:
    f=R/'vendor/community-skills-2026-11-16'/m['id']/'SKILL.md'
    match=f.exists() and sha(f)==m['sha256']
    skills.append({'id':m['id'],'original_exists':f.exists(),'sha256_matches':match})
assert len(skills)==14 and all(x['sha256_matches'] for x in skills),skills

# Render the final Beamer output and create preview contact sheets for the project.
render=Q/'pdf-render';render.mkdir(exist_ok=True)
for i,p in enumerate(pdf):p.get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(render/f'page-{i+1:02}.png')
def sheet(paths,dest,cols=3):
    tiles=[]
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGB');im.thumbnail((480,360))
        tile=Image.new('RGB',(500,392),'#eeeeee');tile.paste(im,((500-im.width)//2,20))
        ImageDraw.Draw(tile).text((12,373),str(i+1),fill='black');tiles.append(tile)
    canvas=Image.new('RGB',(cols*500,((len(tiles)+cols-1)//cols)*392),'white')
    for i,t in enumerate(tiles):canvas.paste(t,((i%cols)*500,(i//cols)*392))
    canvas.save(dest)
paths=[render/f'page-{i+1:02}.png' for i in range(45)]
for start in range(0,45,9):sheet(paths[start:start+9],Q/f'overview-{start+1:02}-{min(start+9,45):02}.jpg')
stats={'slides':45,'speech_chinese_chars':sum(sum('\u4e00'<=c<='\u9fff' for c in s['speech']) for s in S),
       'planned_seconds':sum(s['seconds'] for s in S),'docx_render_pages':23,
       'native_table_slides':table_owners,'embedded_source_figure_slides':image_owners,
       'pptx_media_files':len(media),'notes_match_all_45':True,'pdf_text_boundary_findings':boundary,
       'final_tex_warnings':warnings,'original_skill_hashes':skills,
       'native_powerpoint_run':False,'rehearsal_performed':False,
       'sha256':{p.name:sha(p) for p in O.iterdir() if p.suffix in ['.pptx','.pdf','.docx'] and p.name!='01_组会报告_45页.pptx'}}
(Q/'final_checks.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')

plan=['# 新版逐页论证与证据表','','|页|页面|讲述任务|证据及口径|秒|','|---:|---|---|---|---:|']
for s in S:plan.append(f"|{s['page']}|{s['title'].replace(chr(10),' ')}|{s['purpose']}|{s['source']}|{s['seconds']}|")
(P/'逐页论证设计.md').write_text('\n'.join(plan),encoding='utf-8')
readme='''# 信息集论文新版报告

本版为45页连续正文。以本地2026-04-27完整工作稿为唯一主表数值依据，新增参考导出用于梳理问题与解释思路。无最后讨论页或A类附录。

## 文件

- `01_45页报告.pptx`：本地PowerPoint文件，45页，21张原生表格，文字与公式文本可编辑，11幅图保留原文图像。每页备注含完整口述稿和出处。
- `01_组会报告_45页.pdf`：无水印RUC Beamer放映文件，数学公式由LaTeX排版。
- `02_逐页逐字稿_45页对应.docx`：按幻灯片编号01–45逐页对应，Word排版23页。预算41分50秒，约8,200汉字，未真人计时。
- `03_可编译源码.zip`：LaTeX、主题派生文件、原图面板、内容JSON、生成脚本、证据表和来源清单。

PPTX与PDF共用同一份内容数据。两种格式保留RUC酒红、楷体和4:3比例；PowerPoint版为原生对象重建，文字换行与Beamer略有不同。需要严格保持数学排版时直接放映PDF；修改论证内容优先编辑内容源再统一生成。

## 新版设计

开头按标题、作者与版本、分层目录、信息进入决策的链条、条件资产定价式展开。第8页即解释一条URL能看见什么，第12页进入详细数据，避免对专业听众作过长基础教学。结果依次区分投入、内容、股票差异、投资者差异、交易时间和搜索路径，结尾回到论文发现。

新要求已写入项目AGENTS.md与docs/2026-11-17_内容重建设计约定.md，并由本地academic-paper-beamer skill链接。既有10份网页原生学术slides skill及4份去AI味skill的文件和哈希均保留在原项目vendor目录，没有用本地生成规则替换。

原40页版本保留于output/information-set/。本版工程为paper/information-set-redesign-20261117/，审阅与渲染记录为qa/information-set-redesign-20261117/。
'''
(O/'README.md').write_text(readme,encoding='utf-8')
(P/'README.md').write_text('''# 45页报告可编译工程

运行 `build.ps1`，或在本目录对main.tex执行两遍xelatex，得到build/main.pdf。需要XeLaTeX及常规Beamer、fontspec、xeCJK、booktabs、tabularx依赖。优先使用KaiTi，没有时回退Fandol楷体。

上游RenminUniv.sty保留原样，背景由ruc-research.sty派生层清空；没有嵌入校徽。上游许可见RUC-theme-LICENSE，原项目保留完整vendor仓库。

slides.json是本版每页屏幕内容、讲述、时间与证据的记录。逐页逐字稿.md可直接阅读。sources.json登记论文与公开来源，assets_manifest.json登记所有原图面板裁剪坐标。build-source/含生成脚本，PPTX生成使用Codex bundled Artifact Tool，编译现有LaTeX不需要它。

图表版权属于论文作者，保留于本地学术汇报用途。不存在可用于重绘原曲线的底层样本数据。14份社区skill原文继续保留于项目vendor目录，包内只放固定版本来源清单，不重新分发许可不清楚的S10原文。
''',encoding='utf-8')
(P/'build.ps1').write_text('''$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    New-Item -ItemType Directory -Path 'build' -Force | Out-Null
    & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
    if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX first pass failed' }
    & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
    if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX second pass failed' }
} finally { Pop-Location }
''',encoding='utf-8-sig')
shutil.copy2(R/'vendor/RUC-Beamer-Theme/LICENSE',P/'RUC-theme-LICENSE')
shutil.copy2(R/'skills/academic-paper-beamer/references/community-source-manifest.json',P/'community-source-manifest.json')
with zipfile.ZipFile(O/'03_可编译源码.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for f in P.iterdir():
        if f.is_file() and f.suffix in ['.tex','.sty','.json','.md','.ps1'] or f.name=='RUC-theme-LICENSE':z.write(f,f.name)
    for f in (P/'assets').iterdir():
        if f.suffix in ['.png','.pdf']:z.write(f,'assets/'+f.name)
    for name in ['redesign_content.py','build_redesign.py','build_redesign_pptx.mjs','prepare_redesign.py','finalize_redesign.py']:
        z.write(R/'scripts'/name,'build-source/'+name)
    z.write(R/'docs/2026-11-17_内容重建设计约定.md','design-rules.md')
    z.write(Q/'修订与验收记录.md','review-record.md')
old=O/'01_组会报告_45页.pptx'
if old.exists():shutil.move(str(old),str(Q/'rejected_placeholder_export.pptx'))
print(json.dumps({k:v for k,v in stats.items() if k not in ['sha256','original_skill_hashes']},ensure_ascii=False))
