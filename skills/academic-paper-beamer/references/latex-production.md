# LaTeX 生产与验收

## 引擎和主题

使用 XeLaTeX，优先 `ctex`；UTF-8 源文件。优先显式字体配置及回退，中文 Kaishu 对应原模板风格，数学保留 Computer Modern。使用 fontspec 时不要照搬 pdfLaTeX 的 inputenc/T1 设置。Beamer 自带 hyperref；无需为了上游 skill 的建议重复最后加载。

本机 2026-11-15 实测：`zhnumber` 3.1（2026）要求 2025-10-09 之后的 expl3，但本机内核为 2024-01-04。当前工程实际采用 `xeCJK` + `fontspec`，自行设定中文图表名称；本报告不使用 CTeX 的中文章节数字或日期宏。没有修改系统宏包。若后续要使用 CTeX 的扩展功能，应在一致版本的 TeX 环境里重建并验收，不能通过删除宏包版本检查强行运行。

先加载原 `RenminUniv`，再加载本项目派生设置，清空 `background` 与 `background canvas`。标题页不再插入上游封面的独立 EPS 校徽。修改在派生层进行，原仓库保持可追溯。

保留原色 RGB(151,31,48)、4:3 页面与 smoothbars。保留页眉章节提示；总目录与少量手动章节导览按当前内容安排。早期测试稿取消自动目录是局部决定，2026-11-16用户要求加强章节过渡，不应继续机械禁用。默认不为每个子节重复生成整张目录。附录计数使用 Beamer 原生 `\insertmainframenumber` 或一个明确计数策略，不同时安装多个历史补丁。

## 公式、表图与编号

- 数学用 amsmath 的 equation/aligned；需引用则 label/ref，否则不滥加编号。正文中的变量和公式字体一致；文字说明用 `\text{}`。
- 原文公式提取乱码时看原 PDF，不从 OCR 符号猜。遇到原文口径冲突登记差异；概念示意公式标明为讲解简式。
- 表用 booktabs，保留被解释变量、组别、列号、统计量及来源；只抽取必要行列。不要用 resizebox 将整张回归表无限缩小。
- 插图同时限制 width/height 并 keepaspectratio。保留坐标轴、图例、样本/窗口和来源。裁剪只去掉空白，不剪去证据。
- caption 编号和 label 一起使用；图、表、式号各自核对。正文页 i/N，附录 A1、A2；封面可不计。
- 默认禁用 overlays 以便 PDF 物理页与展示页一致；确需逐步揭示时单独记录 frame 与物理页。

## 编译与验收

建议命令：`xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex` 至少两遍。使用 bibliography 后按后端增加 biber/bibtex 步骤。保留最终编译日志，检查 missing character、undefined reference/citation、overfull h/vbox 和字体替代。

自动检查至少包括 PDF 可打开、页数、字体嵌入、可抽取中文、每页标题/页码、边界及来源。视觉检查包括全套缩略图与每页原尺寸 PNG。每个使用的图表数字回对证据表；检查主表与正文是否冲突。最终记录哪些检查实际做过、哪些如会场投影/计时尚未做，不把“脚本正常退出”称为完整验收。

本项目 reusable/ 提供最小示例与 build 脚本；先跑模板小样，再编译正式内容，避免最后才发现缺包或字体问题。
