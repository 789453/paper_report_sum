# 11 月 20 日组会 · 第二轮仔细微调

本轮以用户指定的 47 页主 PDF 为基线，对照 Claude 旧稿及 2026 年 4 月 27 日原论文。保留五部分结构、无水印人大 4:3 主题和主要表述，按六个文件分块修改。最终为 **44 页正文、A1–A6 六页备份**；原主 PDF 和原始转写不覆盖。

- [最终放映 PDF](../../../output/information-set-projection-20261120-round2/个人投资者的信息集_11-20组会放映_第二轮.pdf)
- [可编译 TeX 工程 ZIP](../../../output/information-set-projection-20261120-round2/个人投资者的信息集_第二轮LaTeX源码.zip)
- [约 30 分钟逐页口述讲稿](约30分钟口述讲稿.md)及[逐页计时预算](讲述与计时.md)
- [语义校订与执行规范](../../../docs/第二轮微调_01_语义校订与执行规范.md)、[R01–R47 调整清单](../../../docs/第二轮微调_02_逐页调整清单.md)、[实际核查记录](../../../docs/第二轮微调_03_核查记录.md)

`main.tex` 依次读入下表源文件。Markdown 记录实际内容、图形安排与承接；逐页口述稿在页面完成后另写，不能替代上屏逻辑。旧页 M 与本版 N 的对应见调整清单。

| 本版页 | 内容 Markdown | TeX |
|---|---|---|
| N1–8 | [开场与研究问题](manuscript/01_开场与研究问题.md) | `part-1.tex` |
| N9–14 | [数据与测度](manuscript/02_数据与测度.md) | `part-2.tex` |
| N15–23 | [描述性统计](manuscript/03_描述性统计.md) | `part-3.tex` |
| N24–32 | [股票比较](manuscript/04a_股票比较.md) | `part-4a.tex` |
| N33–39 | [投资者与交易情境](manuscript/04b_投资者与交易情境.md) | `part-4b.tex` |
| N40–44 | [贡献评价与结尾](manuscript/05_贡献评价与结尾.md) | `part-5.tex` |
| N45–50 | A1–A6，正文按需跳转 | `appendix.tex`，与上一轮逐字相同 |

在此目录执行：

```powershell
pwsh -File build.ps1
```

需要 TeX Live 的 XeLaTeX、Beamer、xeCJK、TikZ、colortbl、Latin Modern。中文优先 KaiTi/FangSong，缺失时回退 Fandol。脚本连续编译两遍，PDF 在 `build/main.pdf`；发现溢出、缺字、未定义引用或字体警告时退出。所有图件均在 `assets/`，不依赖旧工程或绝对路径。`RenminUniv.sty` 与许可保留；无水印改动在本地派生文件 `ruc-research.sty`。

真实行情截图的完整原图、三个放大局部及裁切坐标见 [来源说明](assets/yahoo-snapshot-source.md)。它是当代页面的教学实例，不是论文原始数据。PCA 的 A/B/C 输入表同样明示为教学构造例。

项目根目录的 `scripts/verify_round2.py` 核对具体页码、URL 字段、删除要求、身份、链接、附录一致性及编译日志；`scripts/review_round2.py` 渲染完整逐页图像供目视检查。检查记录区分屏幕渲染、技术验证与尚未进行的真人计时/会场投影。
