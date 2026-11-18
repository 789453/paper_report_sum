from pathlib import Path
import fitz,shutil
R=Path(__file__).resolve().parents[1]; P=R/'paper'/'information-set';A=P/'assets'; A.mkdir(parents=True,exist_ok=True)
for name in ['ruc-research.sty','RenminUniv.sty']:shutil.copy2(R/'reusable'/name,P/name)
s=(P/'ruc-research.sty').read_text(encoding='utf-8')
s=s.replace('用户提供的 SSRN 稿（封面标 2023.10），','Laarits 与 Wurgler（2026.4.27），')
(P/'ruc-research.sty').write_text(s,encoding='utf-8')
d=fitz.open(R/'sources'/'information-set'/'paper.pdf')
crops={'chart_all':(52,(125,130,490,390)),'chart_optin':(52,(125,405,490,657)), 'event_msft':(53,(180,168,422,355)), 'timing':(54,(75,173,546,515)), 'timing_mean':(54,(75,173,300,515)), 'timing_median':(54,(311,173,546,515)), 'paths':(55,(72,195,502,485)), 'buy_paths':(56,(130,134,393,311)), 'sell_paths':(56,(424,134,684,311)), 'less_spec_paths':(56,(130,375,392,546)), 'more_spec_paths':(56,(405,375,686,546))}
for name,(pg,rect) in crops.items():
    pg0=d[pg-1];clip=fitz.Rect(rect)
    q=fitz.open();q.new_page(width=clip.width,height=clip.height);q[0].show_pdf_page(q[0].rect,d,pg-1,clip=clip);q.save(A/(name+'.pdf'));q.close()
    pg0.get_pixmap(matrix=fitz.Matrix(2,2),clip=clip,alpha=False).save(A/(name+'.png'))
print('prepared',len(crops),'original figure panels')
