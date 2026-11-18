"""Author editable DOCX with bundled python-docx; math stays native OMML."""
from pathlib import Path
import re,json,math
from docx import Document
from docx.shared import Pt,Inches,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';O=R/'output/information-set';O.mkdir(parents=True,exist_ok=True)

def font(style,name='Times New Roman',east='宋体',size=11.5,bold=False):
 style.font.name=name;style.font.size=Pt(size);style.font.bold=bold;style.font.color.rgb=RGBColor(0,0,0)
 el=style.element.get_or_add_rPr();f=el.find(qn('w:rFonts'))
 if f is None:f=OxmlElement('w:rFonts');el.insert(0,f)
 for k in ['ascii','hAnsi','cs']:f.set(qn('w:'+k),name)
 f.set(qn('w:eastAsia'),east)
 for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
  f.attrib.pop(qn('w:'+key),None)
def field(p,name):
 r=p.add_run();e=OxmlElement('w:fldSimple');e.set(qn('w:instr'),name);r._r.addnext(e)
def base(kind):
 d=Document();s=d.sections[0];s.page_width=Inches(8.5);s.page_height=Inches(11)
 s.top_margin=Cm(2.0);s.bottom_margin=Cm(2.0);s.left_margin=Cm(2.3);s.right_margin=Cm(2.3)
 s.header_distance=Cm(.8);s.footer_distance=Cm(.8)
 for st in d.styles:
  if st.type==1:
   font(st);pf=st.paragraph_format;pf.widow_control=True
 font(d.styles['Title'],east='黑体',size=20,bold=True)
 d.styles['Title'].paragraph_format.space_after=Pt(10);d.styles['Title'].paragraph_format.first_line_indent=Pt(0)
 for nm,sz in [('Heading 1',14),('Heading 2',12.5),('Heading 3',11.5)]:
  font(d.styles[nm],east='黑体',size=sz,bold=True);pf=d.styles[nm].paragraph_format
  pf.space_before=Pt(14);pf.space_after=Pt(7);pf.first_line_indent=Pt(0);pf.keep_with_next=True
 pf=d.styles['Normal'].paragraph_format;pf.line_spacing=1.32;pf.space_after=Pt(6);pf.first_line_indent=Pt(23)
 font(d.styles['Caption'],size=10);d.styles['Caption'].paragraph_format.first_line_indent=Pt(0)
 for st in d.styles:
  rpr=st.element.find(qn('w:rPr'))
  if rpr is not None:
   for co in rpr.findall(qn('w:color')):
    co.set(qn('w:val'),'000000');co.attrib.pop(qn('w:themeColor'),None)
  ppr=st.element.find(qn('w:pPr'))
  if ppr is not None:
   for b in list(ppr.findall(qn('w:pBdr'))):ppr.remove(b)
 hp=s.header.paragraphs[0];hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT;hp.paragraph_format.first_line_indent=Pt(0)
 hr=hp.add_run('Laarits & Wurgler｜'+kind);hr.font.size=Pt(9)
 fp=s.footer.paragraphs[0];fp.alignment=WD_ALIGN_PARAGRAPH.CENTER;fp.paragraph_format.first_line_indent=Pt(0)
 fp.add_run('第 ');field(fp,'PAGE');fp.add_run(' 页')
 d.core_properties.title=kind+'：On the Information Set of Individual Investors';d.core_properties.subject='2026-04-27工作稿阅读与中文组会准备'
 d.core_properties.author='';d.core_properties.keywords='individual investors; information acquisition; clickstream; 中文组会'
 return d
def hyperlink(p,url,label='来源链接'):
 rel=p.part.relate_to(url,RT.HYPERLINK,is_external=True);h=OxmlElement('w:hyperlink');h.set(qn('r:id'),rel)
 r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),'000000');pr.append(co);r.append(pr)
 t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)
def textpara(d,text,style=None):
 p=d.add_paragraph(style=style)
 if text.startswith('['):p.paragraph_format.first_line_indent=Pt(0)
 parts=re.split(r'(https?://[^\s；。]+)',text)
 for chunk in parts:
  if chunk.startswith('http'):hyperlink(p,chunk.rstrip('.,'))
  else:p.add_run(chunk)
 return p
def mr(t):
 r=OxmlElement('m:r');n=OxmlElement('m:t');n.text=t;r.append(n);return r
def sub(base,idx):
 s=OxmlElement('m:sSub');e=OxmlElement('m:e');e.append(mr(base));s.append(e);q=OxmlElement('m:sub');q.append(mr(idx));s.append(q);return s
def frac(num,den):
 f=OxmlElement('m:f');a=OxmlElement('m:num');a.append(num);b=OxmlElement('m:den');b.append(den);f.extend([a,b]);return f
def sigma(lower,upper,terms):
 n=OxmlElement('m:nary');pr=OxmlElement('m:naryPr');ch=OxmlElement('m:chr');ch.set(qn('m:val'),'∑');pr.append(ch)
 loc=OxmlElement('m:limLoc');loc.set(qn('m:val'),'subSup');pr.append(loc)
 if not upper:
  hide=OxmlElement('m:supHide');hide.set(qn('m:val'),'1');pr.append(hide)
 n.append(pr)
 for tag,txt in [('sub',lower),('sup',upper)]:e=OxmlElement('m:'+tag);e.append(mr(txt));n.append(e)
 e=OxmlElement('m:e')
 for t in terms:e.append(t)
 n.append(e);return n
def equation(d,kind):
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Pt(0)
 p.paragraph_format.keep_with_next=True
 om=OxmlElement('m:oMathPara');o=OxmlElement('m:oMath');om.append(o)
 if kind=='ratio':
  o.extend([sub('r','i'),mr(' = '),frac(sub('M','i'),sub('T','i')),mr('，   ')])
  bar=OxmlElement('m:bar');pr=OxmlElement('m:barPr');pos=OxmlElement('m:pos');pos.set(qn('m:val'),'top');pr.append(pos);bar.append(pr);e=OxmlElement('m:e');e.append(mr('r'));bar.append(e)
  o.extend([bar,mr(' = '),frac(mr('1'),mr('N')),sigma('i = 1','N',[sub('r','i')])])
 else:o.extend([sub('PC','ik'),mr(' = '),sigma('j','',[sub('w','jk'),sub('z','ij')])])
 p._p.append(om)
def literature_table(d):
 cap=d.add_paragraph('表1　相邻文献的观测对象比较',style='Caption');cap.paragraph_format.keep_with_next=True
 rows=[['研究','观测单位/对象','本文可补充的部分'],['Da等（2011）','聚合搜索强度','家庭、主题与路径'],['Barber–Odean（2008）','注意吸引与买入','进入之后研究什么'],['Gargano–Rossi（2018）','账户平台注意活动','平台外研究内容'],['Giglio等（2021）','调查信念与组合','信念形成前的信息输入'],['本篇（2026）','跨平台家庭浏览','待连接完整信念及持仓']]
 t=d.add_table(rows=0,cols=3);t.autofit=False
 widths=[Cm(4.0),Cm(5.0),Cm(7.0)]
 for rowi,values in enumerate(rows):
  cells=t.add_row().cells
  for j,(cell,txt) in enumerate(zip(cells,values)):
   cell.width=widths[j];cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   tcpr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for side in ['top','left','bottom','right','insideH','insideV']:
    e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
   tcpr.append(b);mar=OxmlElement('w:tcMar')
   for side in ['top','left','bottom','right']:
    e=OxmlElement('w:'+side);e.set(qn('w:w'),'100');e.set(qn('w:type'),'dxa');mar.append(e)
   tcpr.append(mar);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E7E6E6' if rowi==0 else ('F5F5F5' if rowi%2==0 else 'FFFFFF'));tcpr.append(shade)
   p=cell.paragraphs[0];p.paragraph_format.first_line_indent=Pt(0);p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1.15
   rr=p.add_run(txt);rr.font.size=Pt(10.5);rr.bold=rowi==0
  if rowi==0:
   h=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(h)
  no=OxmlElement('w:cantSplit');t.rows[-1]._tr.get_or_add_trPr().append(no)
 d.add_paragraph('比较维度为测量覆盖；各研究识别任务不同。',style='Caption')
def from_md(path,name,kind):
 d=base(kind);content=path.read_text(encoding='utf-8');inserted=False
 for block in re.split(r'\n\s*\n',content):
  block=block.strip()
  if not block:continue
  if block.startswith('# '):d.add_paragraph(block[2:],'Title')
  elif block.startswith('## '):
   if kind=='论文研究分析' and block.startswith('## 5　') and not inserted:literature_table(d);inserted=True
   d.add_heading(block[3:],level=1)
  elif block.startswith('[[EQ:'):equation(d,block[5:-2])
  else:textpara(d,block.replace('\n',' '))
 d.save(O/name);return d
def clean_title(s):
 s=s.replace('\\quad',' ').replace('\\&','&').replace('\\\\',' ')
 return re.sub(r'\\[a-zA-Z]+','',s).strip()
def speech():
 s=(P/'main.tex').read_text(encoding='utf-8');notes=json.loads((P/'讲稿正文.json').read_text(encoding='utf-8'))
 chunks=re.split(r'% Physical page \d+\n',s)[1:];records=[]
 for i,(chunk,note) in enumerate(zip(chunks,notes),1):
  m=re.search(r'\\begin\{frame\}(?:\[[^\]]*\])?\{([^\n]+)\}',chunk)
  if m:title=clean_title(m[1])
  else:
   m=re.search(r'\\partguide\{([^}]+)\}',chunk);title=m[1] if m else 'On the Information Set of Individual Investors'
  han=len(re.findall('[\u4e00-\u9fff]',note));en=len(re.findall(r'[A-Za-z]+',note));nums=len(re.findall(r'\d+(?:\.\d+)?',note));units=han+2*en+1.5*nums
  pause=6 if i<=31 else 0
  if i in [12,13,14,15,17,18,19,20,23,24,25,27,28]:pause=14
  sec=5*round((units/200*60+pause)/5) if i<=31 else 0
  records.append({'physical_page':i,'title':title,'main':i<=31,'han':han,'english_words':en,'seconds':sec,'note':note})
 assert len(records)==40
 secs=sum(x['seconds'] for x in records);mins=round(secs/60,1)
 d=base('逐页讲稿');d.add_paragraph('逐页讲稿','Title');textpara(d,'On the Information Set of Individual Investors｜与40页放映PDF逐页对应。')
 textpara(d,f'主体为第1—31物理页（封面及30个编号页），第32—40页为条件使用的备份。讲述预算约{mins}分钟，提问另计。按每分钟约200个中文等价单位及读图停顿估算，尚未真人计时演练。')
 textpara(d,'超时删减：优先缩短第20页事件案例、第19页相对内容回归及第28页路径分组，约可节省3—4分钟；保留第12—16页主结果和第24—27页过程事实。不要加快读表。')
 md=['# 逐页讲稿',f'讲述预算：{mins}分钟；备份不计入。']
 elapsed=0
 for x in records:
  i=x['physical_page'];title=f'第{i:02}页｜'+x['title'];d.add_heading(title,1)
  if x['main']:
   e=elapsed+x['seconds'];label=f"{x['seconds']}秒｜累计 {elapsed//60:02}:{elapsed%60:02}—{e//60:02}:{e%60:02}";elapsed=e
  else:label='备份｜仅在对应问题出现时使用'
  p=d.add_paragraph(label,style='Caption');p.paragraph_format.keep_with_next=True
  textpara(d,x['note']);md.extend(['\n## '+title,label,'',x['note']])
 d.save(O/'02_逐页讲稿.docx');(P/'逐页讲稿.md').write_text('\n\n'.join(md),encoding='utf-8')
 (P/'slide_plan.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 return mins
if __name__=='__main__':
 from_md(P/'研究分析.md','04_论文研究分析.docx','论文研究分析')
 from_md(P/'专业问答.md','03_专业问答清单.docx','专业问答')
 mins=speech();body=(P/'研究分析.md').read_text(encoding='utf-8').split('## 参考文献')[0];body=re.sub(r'^#+[^\n]*','',body,flags=re.M)
 report={'analysis_body_han_excluding_headings_references':len(re.findall('[\u4e00-\u9fff]',body)),'qa_questions':36,'physical_pages':40,'main_end_page':31,'speech_design_minutes':mins,'docx_math':'native OMML: 2 equations','runtime':'bundled Python 26.1112.11011'}
 (O/'delivery_metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
