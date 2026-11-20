# 11 月 20 日放映微调版

[放映 PDF](../../../output/information-set-projection-20261120-ready/个人投资者的信息集_11-20放映微调版.pdf) · [逐页对照与附录索引](../../../docs/2026-11-20_放映微调与附录排序.md)

基于 `d95e6b2` 的终校版。43 页正文，6 页附录。第 18 页的分位数图入口直达 A6。A2 两张回归表来自本地 2026 年 4 月 27 日工作稿第 49–50 页。

`main.tex` 为编译入口。各部分放在 `part-*.tex`，备份集中在 `appendix.tex`，图片放在 `assets/`。在本目录运行 `pwsh -File build.ps1`，连续两遍 XeLaTeX 后得到 `build/main.pdf`。
