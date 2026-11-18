from pathlib import Path
import json,re,hashlib,zipfile
import pymupdf as fitz
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';Q=R/'qa/information-set/final';Q.mkdir(parents=True,exist_ok=True)
d=fitz.open(P/'build/main.pdf');plan=json.loads((P/'slide_plan.json').read_text(encoding='utf-8'));issues=[];fonts={};pages=[]
assert len(d)==len(plan)==40
for i,(pg,item) in enumerate(zip(d,plan)):
 text=pg.get_text();compact=re.sub(r'\s+','',text)
 if i>0:
  expected=f'{i}/30' if i<=30 else f'A{i-30}/9'
  if expected not in compact:issues.append(f'page {i+1}: missing counter {expected}')
 if '\ufffd' in text or '??' in text:issues.append(f'page {i+1}: unresolved character/reference')
 for b in pg.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l.get('spans',[]):
    x0,y0,x1,y1=s['bbox']
    if s['text'].strip() and (x0<-.6 or y0<-.6 or x1>pg.rect.width+.6 or y1>pg.rect.height+.6):issues.append(f'page {i+1}: out-of-page text {s["text"][:40]}')
 for xref,ext,typ,base,*_ in pg.get_fonts(full=True):
  if xref not in fonts:
   _,_,_,buf=d.extract_font(xref);fonts[xref]={'base':base,'type':typ,'embedded_bytes':len(buf)}
   if not buf:issues.append(f'unembedded font {base}')
 pages.append({'page':i+1,'title':item['title'],'text_chars':len(text),'size_points':list(pg.rect)[2:]})
log=(P/'build/main.log').read_text(encoding='utf-8',errors='replace')
for line in log.splitlines():
 if re.search('Overfull|Missing character|undefined|Font Warning|^!',line,re.I):issues.append(line)
for name,terms in [(12,['144.2','96.8','29.1','5.7']),(13,['31.5','157.4']),(14,['39.1','12.5']),(15,['64.4','18.6']),(18,['1.03','1.13','14.42','11.35']),(19,['3.67','2.25','-2.40']),(23,['35.58','8.77'])]:
 t=d[name-1].get_text().replace('−','-')
 for term in terms:
  if term not in t:issues.append(f'page {name}: expected source value {term} absent')
body=(P/'研究分析.md').read_text(encoding='utf-8').split('## 参考文献')[0];body=re.sub(r'^#+[^\n]*','',body,flags=re.M)
if len(re.findall('[\u4e00-\u9fff]',body))<10000:issues.append('analysis body below 10000 Han characters')
docs={}
for name in ['02_逐页讲稿.docx','03_专业问答清单.docx','04_论文研究分析.docx']:
 f=R/'output/information-set'/name
 with zipfile.ZipFile(f) as z:
  xml=z.read('word/document.xml').decode();docs[name]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'math_objects':xml.count('<m:oMath>'),'tables':xml.count('<w:tbl>')}
  if '[[EQ:' in xml:issues.append(name+': raw equation placeholder')
result={'pdf_pages':len(d),'main_frames':30,'appendix_frames':9,'title_unnumbered':True,'fonts':fonts,'pages':pages,'docs':docs,'issues':issues,'visual_review':'see 验收记录.md; automated checks are not a visual verdict'}
(Q/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':len(d),'fonts':len(fonts),'issues':issues},ensure_ascii=False))
if issues:raise SystemExit(1)
