"""Validate the delivered Beamer's concrete requirements, navigation and provenance."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'paper/information-set-argument-v2/projection-20261120-round2'
QA = ROOT / 'qa/information-set-round2'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    doc = fitz.open(SRC / 'build/main.pdf')
    assert len(doc) == 50, len(doc)
    labels = ['authors','section-1','chain','literature','proxies','dimensions','agenda',
              'section-2','sample','urls','yahoo','rules','assignment','section-3','funnel',
              'categories','depth','domains','topics','mixed','windows','averages','section-4',
              'empirical-why','slices','design','size-coefficients','size','adjusted','event','tilt',
              'pc-why','pc-input','pc-one','pc-two','timing','path','fast-slow','section-5',
              'scorecard','evaluation','limitations','thanks']
    aux = (SRC / 'build/main.aux').read_text(encoding='utf-8')
    for page, label in enumerate(labels, 2):
        assert re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{'+str(page)+r'\}\{'+str(page)+r'\}', aux), (label,page)
    for k in range(1,7):
        assert f'\\newlabel{{appendix-{k}}}{{{{{44+k}}}{{{44+k}}}' in aux
    tex = '\n'.join(p.read_text(encoding='utf-8') for p in SRC.glob('*.tex'))
    for deleted in ['buy-sell','next-tests','字母汤','先读零线','选列展示','风险判断未知','噪声程度未知']:
        assert deleted not in tex, deleted
    assert (SRC/'appendix.tex').read_bytes() == (SRC.parent/'projection-20261120/appendix.tex').read_bytes()
    text = [p.get_text() for p in doc]
    assert '杨博远' in text[0] and '27国金博0' in re.sub(r'\s','',text[0])
    assert 'Working Paper' in text[0]
    for term in ['showQTRChange','duration=1095','daysforward=545','year=2006','symbol=GOOG','shares=100']:
        assert term in text[10], term
    assert '7.9%' in text[31] and '9.0%' in text[31]
    assert '教学' in text[33] and '严格大于' in text[33]
    invalid_links=[]
    link_count=0
    for i,p in enumerate(doc):
        for link in p.get_links():
            link_count+=1
            if link['kind']==fitz.LINK_GOTO and not 0<=link.get('page',-1)<len(doc):
                invalid_links.append([i+1,link])
    assert not invalid_links, invalid_links
    log=(SRC/'build/main.log').read_text(encoding='utf-8',errors='replace')
    problems=re.findall(r'^.*(?:Overfull|Missing character|Undefined control sequence|LaTeX Font Warning|LaTeX Warning:.*undefined).*$',log,re.M)
    assert not problems,problems
    fonts=subprocess.check_output(['pdffonts',str(SRC/'build/main.pdf')],text=True,encoding='utf-8')
    font_rows=re.findall(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',fonts,re.M)
    assert font_rows and all(row[0]=='yes' for row in font_rows)
    oral=(SRC/'约30分钟口述讲稿.md').read_text(encoding='utf-8')
    assert len(re.findall(r'^## N\d+｜',oral,re.M))==44
    timing=(SRC/'讲述与计时.md').read_text(encoding='utf-8')
    durations=re.findall(r'\| N\d+ · [^|]* \| (\d+):(\d+) \|',timing)
    assert len(durations)==44 and sum(int(m)*60+int(s) for m,s in durations)==1800
    provenance={str(p.relative_to(ROOT)):sha(p) for p in [
        ROOT/'raw_reference/第二轮仔细微调_原文.md',
        ROOT/'On the Information Set of Individual Investors.pdf',
        ROOT/'output/information-set-projection-20261120/个人投资者的信息集_11-20组会放映.pdf',
        SRC/'appendix.tex', SRC/'build/main.pdf']}
    results={'pages':50,'main_pages':44,'appendix_pages':6,'validated_page_labels':len(labels)+6,
             'hyperlinks':link_count,'invalid_internal_links':0,'appendix_source_unchanged':True,
             'font_records':len(font_rows),'all_fonts_embedded':True,
             'oral_sections':44,'estimated_oral_seconds':1800,
             'compile_problems':problems,'source_sha256':provenance,
             'limits':'Screen renders inspected separately; no live projector or human timed rehearsal.'}
    QA.mkdir(parents=True,exist_ok=True)
    (QA/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in results.items() if k!='source_sha256'},ensure_ascii=True))

if __name__=='__main__':
    main()
