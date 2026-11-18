from pathlib import Path
import json, re, subprocess, shutil
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

R=Path(__file__).resolve().parents[1]; P=R/'paper/information-set-redesign-20261117'
O=R/'output/information-set-redesign-20261117';O.mkdir(exist_ok=True)
S=json.loads((P/'slides.json').read_text(encoding='utf-8'))

def esc(s):
    math={'ℐᵢ,ₜ':r'\(\mathcal I_{i,t}\)','R²':r'\(R^2\)','≤':r'\(\le\)','→':r'\(\rightarrow\)','≈':r'\(\approx\)','−':'-','²':r'\(^{2}\)','σ':r'\(\sigma\)'}
    out=''
    for c in s:
        out+= {'&':r'\&','%':r'\%','_':r'\_','#':r'\#','$':r'\$','{':r'\{','}':r'\}'}.get(c,c)
    for a,b in math.items():out=out.replace(a,b)
    return out

def widths(table):
    n=len(table[0])
    first=table[0][0]
    if first=='一级论证':return [.38,.50,.12]
    if first=='理论线索':return [.25,.35,.40]
    if first=='已有可观测对象':return [.32,.32,.36]
    if first=='关注覆盖广度':return [.28,.18,.27,.27]
    if first=='正向 / 近零变量':return [.38,.12,.38,.12]
    if first=='变量〔摘录〕':return [.70,.30]
    if first=='研究范围':return [.43,.19,.19,.19]
    if first.startswith('价格研究比例') or first.startswith('研究覆盖比例'):return [.60,.22,.18]
    if n==2: return [.37,.63]
    numeric=all(len(str(x))<20 for row in table[1:] for x in row[1:])
    if n==3:return [.56,.22,.22] if numeric else [.30,.45,.25]
    if n==4:return [.43,.19,.19,.19]
    return [1/n]*n

tex=[r'\documentclass[11pt,compress]{beamer}',r'\usepackage{ruc-research}',
     r'\title[个体投资者的信息集]{On the Information Set\\of Individual Investors}',
     r'\author[Laarits \& Wurgler]{Toomas Laarits\quad Jeffrey Wurgler}',
     r'\institute[NYU Stern]{NYU Stern School of Business}',r'\date{2026年4月27日工作稿}',
     r'\setbeamertemplate{page number in head/foot}{\insertframenumber/\inserttotalframenumber}',
     r'\begin{document}']
sec=None
for s in S:
    if s['section']!=sec:sec=s['section'];tex.append(r'\section{'+esc(sec)+'}')
    tex.append(f"% Physical page {s['page']:02d}: {s['purpose']}")
    if s['kind']=='cover':tex.append(r'\begin{frame}[plain]\titlepage\end{frame}');continue
    tex.append(r'\begin{frame}{'+esc(s['title'])+r'}\relax')
    if s['formula']:
        tex.append(r'\begin{equation*}'+s['formula']['tex']+r'\end{equation*}\medskip')
    if s['table']:
        t=s['table'];ws=widths(t);n=len(t[0]);cols=''.join(r'>{\hsize='+f'{w*n:.3f}'+r'\hsize\linewidth=\hsize\raggedright\arraybackslash}X' for w in ws)
        tex.extend([r'{\small\renewcommand{\arraystretch}{1.22}',r'\begin{tabularx}{\linewidth}{@{}'+cols+r'@{}}\toprule'])
        for i,row in enumerate(t):
            tex.append(' & '.join((r'\textbf{'+esc(str(x))+'}') if i==0 else esc(str(x)) for x in row)+r'\\')
            if i==0:tex.append(r'\midrule')
        tex.extend([r'\bottomrule\end{tabularx}}',r'\medskip'])
    if s['asset']:
        if s['asset'].startswith('timing_'):
            tex.append(r'\begin{columns}[c]\begin{column}{.51\textwidth}\centering\includegraphics[width=\linewidth,height=5.9cm,keepaspectratio]{assets/'+s['asset']+r'.pdf}\end{column}\begin{column}{.44\textwidth}')
            for line in s['lines']:tex.append(esc(line)+r'\par\medskip')
            tex.append(r'\end{column}\end{columns}')
        else:
            h='4.8' if s['asset'] in ['paths','buy_paths','sell_paths','less_spec_paths','more_spec_paths'] else '4.45'
            tex.append(r'\centering\includegraphics[width=\linewidth,height='+h+r'cm,keepaspectratio]{assets/'+s['asset']+r'.pdf}\par')
            for line in s['lines']:tex.append(r'{\small '+esc(line)+r'\par}')
    elif s['kind']=='chain':
        for i,line in enumerate(s['lines']):
            tex.append((r'\alert{' if i==1 else '')+esc(line)+('}' if i==1 else '')+r'\par')
            if i<4:tex.append(r'{\color{tsinghua}\(\downarrow\)}\par')
    else:
        for line in s['lines']:tex.append(esc(line)+r'\par\medskip')
    if s['source']:tex.append(r'\source{'+esc(s['source'])+'}')
    tex.append(r'\end{frame}')
tex.append(r'\end{document}')
(P/'main.tex').write_text('\n'.join(tex),encoding='utf-8')

def setfont(st,east='宋体',size=12,bold=False):
    st.font.name='Arial';st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor(0,0,0)
    rf=st.element.get_or_add_rPr().find(qn('w:rFonts'))
    if rf is None:rf=OxmlElement('w:rFonts');st.element.get_or_add_rPr().append(rf)
    rf.set(qn('w:eastAsia'),east)
    for k in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+k),None)
d=Document();se=d.sections[0]
se.page_width=Inches(8.5);se.page_height=Inches(11)
se.top_margin=Cm(1.8);se.bottom_margin=Cm(1.8);se.left_margin=Cm(2.1);se.right_margin=Cm(2.1)
se.header_distance=Cm(.7);se.footer_distance=Cm(.7)
setfont(d.styles['Normal']);d.styles['Normal'].paragraph_format.line_spacing=1.35
d.styles['Normal'].paragraph_format.space_after=Pt(7)
setfont(d.styles['Title'],'黑体',20,True)
setfont(d.styles['Subtitle'],'宋体',12,False);d.styles['Subtitle'].font.italic=False
setfont(d.styles['Heading 1'],'黑体',14,True)
d.styles['Heading 1'].paragraph_format.space_before=Pt(12);d.styles['Heading 1'].paragraph_format.space_after=Pt(7)
setfont(d.styles['Caption'],'宋体',9)
for st in d.styles:
    pp=st.element.find(qn('w:pPr'))
    if pp is not None:
        for b in list(pp.findall(qn('w:pBdr'))):pp.remove(b)
hp=se.header.paragraphs[0];hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
hp.add_run('个人投资者的信息集  逐页逐字稿').font.size=Pt(9)
fp=se.footer.paragraphs[0];fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');fp._p.append(f)
d.add_paragraph('个人投资者的信息集逐页逐字稿','Title')
d.add_paragraph('对应新版45页报告  2026年4月27日工作稿','Subtitle')
intro=d.add_paragraph('正文按幻灯片页码排列，可直接口述。全稿约8,200汉字，讲述预算约42分钟，包含读图停顿，尚未进行真人计时。每页末的出处和备讲说明不计入口述。')
intro.paragraph_format.space_after=Pt(12)
md=['# 个人投资者的信息集逐页逐字稿','',intro.text,'']
elapsed=0
for i,s in enumerate(S):
    if i>0 and i%2==0:d.add_page_break()
    title=s['title'].replace('\n',' ')
    d.add_paragraph(f"第{s['page']:02d}页  {title}",'Heading 1')
    stamp=f"{elapsed//60:02d}:{elapsed%60:02d}–{(elapsed+s['seconds'])//60:02d}:{(elapsed+s['seconds'])%60:02d}"
    cap=d.add_paragraph(f"讲述预算 {s['seconds']}秒  累计 {stamp}",'Caption')
    # Preserve speech verbatim; split only at a natural sentence boundary around the middle.
    text=s['speech'];sent=re.split(r'(?<=[。！？])',text);part=''
    for sent0 in sent:
        part+=sent0
        if len(part)>120:d.add_paragraph(part);part=''
    if part:d.add_paragraph(part)
    if s['speaker_note']:d.add_paragraph('备讲说明  '+s['speaker_note'],'Caption')
    if s['source']:d.add_paragraph('核对出处  '+s['source'],'Caption')
    md.extend([f"## 第{s['page']:02d}页 {title}",f"讲述预算：{s['seconds']}秒；累计：{stamp}",'',text,'',f"核对出处：{s['source']}",''])
    elapsed+=s['seconds']
d.core_properties.title='个人投资者的信息集逐页逐字稿';d.core_properties.author=''
d.save(O/'02_逐页逐字稿_45页对应.docx')
(P/'逐页逐字稿.md').write_text('\n'.join(md),encoding='utf-8')
(P/'pptx_content.json').write_text(json.dumps([{**s,'column_widths':widths(s['table']) if s['table'] else None} for s in S],ensure_ascii=False,indent=2),encoding='utf-8')
print('wrote main.tex, DOCX manuscript and shared PPTX content')

if '--compile' in __import__('sys').argv:
    B=P/'build';B.mkdir(exist_ok=True)
    engine=shutil.which('xelatex')
    for n in [1,2]:
        r=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=build','main.tex'],cwd=P,capture_output=True)
        (B/f'pass{n}.txt').write_bytes(r.stdout+r.stderr)
        if r.returncode:print(r.stdout.decode('utf-8',errors='replace')[-4500:]);raise SystemExit(r.returncode)
    log=(B/'main.log').read_text(encoding='utf-8',errors='replace')
    warnings=[x for x in log.splitlines() if re.search(r'Overfull|Missing character|undefined|Font Warning|^!',x,re.I)]
    print(json.dumps({'warnings':warnings},ensure_ascii=False))
    shutil.copy2(B/'main.pdf',O/'01_组会报告_45页.pdf')
