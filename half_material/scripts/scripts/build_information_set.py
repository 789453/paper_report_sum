from pathlib import Path
import subprocess,re,json,shutil,sys
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';B=P/'build';B.mkdir(exist_ok=True)
engine=shutil.which('xelatex') or r'D:\Total_Tools\Writing_tools\MiKTeX\miktex\bin\x64\xelatex.exe'
for n in [1,2]:
 p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=build','main.tex'],cwd=P,capture_output=True)
 (B/f'pass{n}.txt').write_bytes(p.stdout+p.stderr)
 if p.returncode:print(p.stdout.decode('utf-8',errors='replace')[-5000:]);sys.exit(p.returncode)
s=(B/'main.log').read_text(encoding='utf-8',errors='replace')
bad=[x for x in s.splitlines() if re.search(r'Overfull|Missing character|undefined|Font Warning|^!',x,re.I)]
print(json.dumps({'pages_expected':40,'warnings':bad},ensure_ascii=False))
if bad:sys.exit(1)
if len(sys.argv)>1:
 d=R/'qa/information-set/revisions'/sys.argv[1];d.mkdir(parents=True,exist_ok=True)
 for f in [P/'main.tex',B/'main.pdf',B/'main.log']:shutil.copy2(f,d/f.name)
