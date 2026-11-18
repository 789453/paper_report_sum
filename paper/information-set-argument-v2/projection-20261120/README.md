# 11 月 20 日个人投资者的信息集 · Beamer

论文为 Laarits 与 Wurgler 的 2026 年 4 月 27 日工作稿。本版是以 32 页主稿为基线的逐页改版。正文物理页 1–41，答疑 A1–A6 分别为物理页 42–47。沿用人大 4:3 无水印主题。

- [语音校订与逐页方案](../../../docs/2026-11-20_语音校订与逐页改版方案.md)保留转写修复、两套旧稿及本版页的映射。
- [讲述与计时](讲述与计时.md)列出正文 41 页的指图顺序，预排 34:27。
- [逐页验收](逐页验收.md)记录事实、图件和版面检查，以及有实质影响的改动。
- [放映 PDF](../../../output/information-set-projection-20261120/个人投资者的信息集_11-20组会放映.pdf)和[可编辑源码 ZIP](../../../output/information-set-projection-20261120/个人投资者的信息集_11-20LaTeX源码.zip)是演示交付。

`main.tex` 读入五部分正文、简短定位条的定义及答疑备份。图表中的重绘数据继续用 TikZ 或 TeX 表编辑。原图裁剪位于 `assets/`，不依赖另一份工程。需要 XeLaTeX、Beamer、xeCJK、TikZ 和 colortbl。KaiTi 缺失时使用 TeX Live 的 Fandol 楷体。

在源码目录运行 `pwsh -File build.ps1`，或连续运行两次 `xelatex -interaction=nonstopmode -halt-on-error main.tex`。脚本的 PDF 位于 `build/main.pdf`。
