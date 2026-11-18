# 个人投资者的信息集 · Beamer 源码

放映版以同项目《汇报叙事与视觉稿》为内容依据，使用 Laarits 与 Wurgler 的2026年4月27日工作稿。32张正文放映页含封面，按35分钟分配。

- `main.tex` 为入口，五个 `part-*.tex` 分别对应五个章节。示意图、比较表和有原始数值的条形图可从TeX编辑。
- `assets/` 保存论文 Figures 1、3、4、5 的原图裁剪。页面上的指读框另由TikZ绘制。
- `ruc-research.sty` 是本项目的无水印派生设置。`RenminUniv.sty` 及其许可随源文件提供。
- `讲述与计时.md` 给出每页现场讲法及累计时标。
- `逐页验收.md` 记录读图、排版和事实复核。

在支持 XeLaTeX 且具备 Beamer、xeCJK、TikZ 与相关字体的 TeX 环境中，执行 `pwsh -File build.ps1`，或在当前目录连续运行两次 `xelatex -interaction=nonstopmode -halt-on-error main.tex`。构建脚本将 PDF 写入 `build/main.pdf`。字体优先使用系统 KaiTi，缺失时使用 TeX Live 的 Fandol 楷体。
