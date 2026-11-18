"""Compile XeLaTeX twice and fail on errors that invalidate the output."""
import argparse
from pathlib import Path
import shutil
import subprocess
import re

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('target', choices=['minimal','paper'], default='paper', nargs='?')
parser.add_argument('--paper-id',default='information-set-argument-v2')
args = parser.parse_args()
target = ROOT/'reusable' if args.target=='minimal' else ROOT/'paper'/args.paper_id
if not target.resolve().is_relative_to(ROOT.resolve()):
    raise SystemExit('Target must be inside the project root')
name = 'minimal' if args.target=='minimal' else 'main'
out = ROOT/'output/pdf' if args.target=='minimal' else target/'build'
out.mkdir(parents=True,exist_ok=True)
if args.target=='minimal':
    shutil.copy2(ROOT/'vendor/RUC-Beamer-Theme/RenminUniv.sty',target/'RenminUniv.sty')
else:
    for filename in ['RenminUniv.sty','ruc-research.sty']:
        base=ROOT/'vendor/RUC-Beamer-Theme' if filename=='RenminUniv.sty' else ROOT/'reusable'
        if not (target/filename).exists():
            shutil.copy2(base/filename,target/filename)
for run in range(2):
    proc=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
                         '-file-line-error','-output-directory='+str(out),name+'.tex'],
                        cwd=target,capture_output=True,encoding='utf-8',errors='replace')
    (out/f'{name}.pass{run+1}.txt').write_text(proc.stdout+'\n'+proc.stderr,encoding='utf-8')
    if proc.returncode:
        print(proc.stdout[-6500:]); print(proc.stderr[-1000:]); raise SystemExit(proc.returncode)
log=(out/(name+'.log')).read_text(encoding='utf-8',errors='replace')
patterns=[r'Overfull \\[hv]box',r'Missing character:',r'LaTeX Warning:.*undefined',
          r'There were undefined references',r'Citation .* undefined',r'Font Warning:']
problems=[line for line in log.splitlines() if any(re.search(p,line) for p in patterns)]
if problems:
    print('\n'.join(problems)); raise SystemExit('Review final LaTeX log before delivery.')
print('Compiled and log-checked: '+str(out/(name+'.pdf')))
