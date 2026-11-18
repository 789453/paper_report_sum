from pathlib import Path
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw
import sys,json
R=Path(__file__).resolve().parents[1];rev=sys.argv[1] if len(sys.argv)>1 else 'final';Q=R/'qa/information-set'/rev;Q.mkdir(parents=True,exist_ok=True)
d=fitz.open(R/'paper/information-set/build/main.pdf')
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(2.2,2.2),alpha=False).save(Q/f'slide-{i+1:02}.png')
for batch in range(0,len(d),8):
 c=Image.new('RGB',(1600,1260),'#dddddd');draw=ImageDraw.Draw(c)
 for k in range(batch,min(batch+8,len(d))):
  a=Image.open(Q/f'slide-{k+1:02}.png');a.thumbnail((780,585));x=(k-batch)%2*800;y=(k-batch)//2*315
  a.thumbnail((390,292));x=(k-batch)%4*400;y=(k-batch)//4*630
  # Two rows of four, enlarged sheets can be inspected with native page files.
  a=Image.open(Q/f'slide-{k+1:02}.png');a.thumbnail((390,585));c.paste(a,(x,y+24));draw.text((x+5,y+4),f'{k+1:02}',fill='black')
 c.save(Q/f'contact-{batch//8+1}.jpg',quality=94)
print('rendered',len(d),'pages to',Q)
