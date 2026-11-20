# 11 月 20 日必要调整版

[放映 PDF](../../../output/information-set-projection-20261120-necessary/个人投资者的信息集_11-20必要调整版.pdf) · [逐页修改前后对照](../../../docs/2026-11-20_必要调整逐页对照.md) · [用户原稿](../../../raw_reference/思考必要调整PPT-11-20-12.md)

本工程从 Git `59cf071` 中的 `projection-20261120-user-final` 复制。上一份主 PPT 为 `f91f167` 的两页微调版。本版共 44 页正文，备份 A1–A5 后为 A5 补图。

| TeX 文件 | 负责页面 |
|---|---|
| `main.tex` | 编译入口、主题和章节调用 |
| `part-1.tex` | 第 1–8 页，研究问题、URL 短例 |
| `part-2.tex` | 第 9–14 页，数据与 AAPL 示意 |
| `part-3.tex` | 第 15–23 页，描述性统计、原图与分位图链接 |
| `part-4a.tex` | 第 24–32 页，实证动机、回归与事件图 |
| `part-4b.tex` | 第 33–39 页，PCA 输入、得分与路径 |
| `part-5.tex` | 第 40–44 页，理论对照与致谢 |
| `appendix.tex` | A1–A5 和 A5 分位数补图 |
| `revision-layout.tex` | 共用两级定位条，保留源码里的证据位置 |

在本目录运行 `pwsh -File build.ps1`，两遍编译后打开 `build/main.pdf`。依赖与上一版相同，所需图片在 `assets/`。独立裁图可用项目根目录的 `python scripts/crop_necessary_1120.py` 复现。原论文为本地 2026 年 4 月 27 日工作稿。Figure 1–5 的物理页与裁框坐标保存在脚本里。
