"""Package the verified round-two PDF and a standalone, auditable TeX project."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'paper/information-set-argument-v2/projection-20261120-round2'
OUT = ROOT / 'output/information-set-projection-20261120-round2'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(p, text):
    p.write_text(text, encoding='utf-8', newline='\n')

def main():
    result = json.loads((ROOT/'qa/information-set-round2/verification.json').read_text(encoding='utf-8'))
    pdf = SRC/'build/main.pdf'
    assert result['source_sha256'][str(pdf.relative_to(ROOT))] == sha(pdf.read_bytes())
    assert not result['compile_problems'] and result['all_fonts_embedded']
    source_commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    OUT.mkdir(parents=True, exist_ok=True)
    pdfname = '个人投资者的信息集_11-20组会放映_第二轮.pdf'
    zipname = '个人投资者的信息集_第二轮LaTeX源码.zip'
    shutil.copy2(pdf, OUT/pdfname)
    for name in ['约30分钟口述讲稿.md','讲述与计时.md']:
        shutil.copy2(SRC/name, OUT/name)
    write(OUT/'验收结果.json', json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    shutil.copy2(SRC/'build/main.log', OUT/'最终编译日志.txt')
    docs = [ROOT/'docs'/name for name in [
        '第二轮微调_01_语义校订与执行规范.md',
        '第二轮微调_02_逐页调整清单.md',
        '第二轮微调_03_核查记录.md']]
    merged = '# 第二轮微调：校订要求、逐页清单与核查\n\n'
    merged += f'本文件合并三份过程文档供连续阅读。最终内容节点：`{source_commit[:7]}`。原始输入不覆盖；各块 Markdown 与 TeX 保留独立文件。\n\n'
    merged += f'[放映 PDF]({pdfname}) · [源码工程]({zipname}) · [口述讲稿](约30分钟口述讲稿.md) · [计时预算](讲述与计时.md)\n\n'
    for doc in docs:
        merged += re.sub(r'^(#{1,5}) ', r'\1# ', doc.read_text(encoding='utf-8'), flags=re.M)+'\n\n'
    write(OUT/'第二轮微调_校订要求与核查.md', merged)
    standalone = '''# 个人投资者的信息集 · 第二轮 TeX 工程

最终稿为 44 页正文和 6 页备份。解压后在本目录运行 `pwsh -File build.ps1`，等待两遍 XeLaTeX 全部结束；PDF 输出到 `build/main.pdf`。

需要 TeX Live 的 XeLaTeX、Beamer、xeCJK、TikZ、colortbl 和 Latin Modern。中文优先 KaiTi/FangSong，缺失时使用 Fandol。全部输入和图件均在包内，不依赖旧工程。主题上游文件与许可保留，本地无水印设置在 ruc-research.sty。

- [完整口述稿](约30分钟口述讲稿.md)和[30 分钟预算](讲述与计时.md)
- 六块内容设计在 `manuscript/`；正文依次为 part-1、part-2、part-3、part-4a、part-4b、part-5.tex。
- [语义校订](review/第二轮微调_01_语义校订与执行规范.md)、[逐页清单](review/第二轮微调_02_逐页调整清单.md)、[核查记录](review/第二轮微调_03_核查记录.md)及原始转写在 review。
- [截图来源及裁切坐标](assets/yahoo-snapshot-source.md)。图中当代行情只作教学实例，PCA 输入三行也是构造例。

`项目README.md` 是仓库版入口的原件，其外部相对链接按仓库结构解释；本包请从当前 README 开始。`源码文件清单.json` 记录归档文件 SHA256。包不含临时编译文件；实际投影与真人计时仍需排练。
'''
    payload = {'README.md': standalone.encode('utf-8')}
    for p in sorted(SRC.rglob('*')):
        rel = p.relative_to(SRC)
        if p.is_file() and 'build' not in rel.parts and '__pycache__' not in rel.parts:
            name = '项目README.md' if rel.as_posix() == 'README.md' else rel.as_posix()
            payload[name] = p.read_bytes()
    for doc in docs:
        payload['review/'+doc.name] = doc.read_bytes()
    raw = ROOT/'raw_reference/第二轮仔细微调_原文.md'
    payload['review/'+raw.name] = raw.read_bytes()
    payload['review/验收结果.json'] = (OUT/'验收结果.json').read_bytes()
    manifest = {'source_commit': source_commit, 'files': {name:sha(data) for name,data in payload.items()}}
    payload['源码文件清单.json'] = json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
    prefix = '个人投资者的信息集_第二轮/'
    with zipfile.ZipFile(OUT/zipname, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(payload.items()):
            entry = zipfile.ZipInfo(prefix+name, date_time=(2026,11,18,18,0,0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry,data)
    with zipfile.ZipFile(OUT/zipname) as archive:
        assert archive.testzip() is None
        for name,data in payload.items():
            assert archive.read(prefix+name) == data
        for p in SRC.rglob('*'):
            if p.is_file() and 'build' not in p.relative_to(SRC).parts:
                rel = p.relative_to(SRC).as_posix()
                assert archive.read(prefix+('项目README.md' if rel=='README.md' else rel)) == p.read_bytes()
    tex = '\n'.join(p.read_text(encoding='utf-8') for p in SRC.glob('*.tex'))
    for name in re.findall(r'\\input\{([^}]+)\}', tex):
        assert name in payload, name
    for name in re.findall(r'\{([A-Za-z0-9_-]+\.(?:pdf|png|jpg))\}', tex):
        assert 'assets/'+name in payload, name
    delivery = {'source_commit':source_commit, 'archive_files':len(payload),
                'files':{name:sha((OUT/name).read_bytes()) for name in [pdfname,zipname,'约30分钟口述讲稿.md','讲述与计时.md','第二轮微调_校订要求与核查.md','验收结果.json']},
                'archive_crc_and_bytes_validated':True,'all_tex_inputs_and_figures_in_archive':True}
    write(OUT/'交付清单.json',json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
    readme = f'''# 第二轮仔细微调交付

正文 **44 页**，备份 **A1–A6**。保持五部分结构及无水印人大主题，基线 47 页主稿保留。封面为“杨博远 · 27国金博0”。

- [放映 PDF]({pdfname})
- [完整可编译 TeX 工程]({zipname})：含六块 Markdown、图件、主题及许可、编译脚本、原始转写和过程文档
- [语义校订、调整清单与核查合并文档](第二轮微调_校订要求与核查.md)
- [约 30 分钟口述讲稿](约30分钟口述讲稿.md)及[逐页预算](讲述与计时.md)
- [技术验收结果](验收结果.json)、[编译日志](最终编译日志.txt)及[文件 SHA256](交付清单.json)

原始要求以 M 页码定位，新稿用 N；完整映射在合并文档。最终内容节点 `{source_commit[:7]}`，此前六块已依次提交：`0ae9eed`、`32dfaf2`、`50b47b2`、`a48fdb1`、`3ee65b3`、`6a5d337`；前期语义与规划节点 `5ed4685`。文件交付另作一个 Git 节点。

两遍编译、50 页渲染、字体嵌入与链接检查已完成。30:00 为口述预算，尚未进行真人计时和会场投影；问答不含在预算中。源码包已核对 CRC、文件内容及全部 TeX 输入/图件，未在另一台机器复编。
'''
    write(OUT/'README.md', readme)
    print(json.dumps({k:v for k,v in delivery.items() if k!='files'},ensure_ascii=False))
    print('PDF bytes', (OUT/pdfname).stat().st_size, 'ZIP bytes', (OUT/zipname).stat().st_size)

if __name__ == '__main__':
    main()
