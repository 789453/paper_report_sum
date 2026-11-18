# 用户自行微调版

这份工程专供杨博远继续修改，独立复制自第二轮最终稿。当前正文、图件、主题与原版相同，仅给 TeX 增加编辑器的主文件/编译器注释。第二轮交付目录保持原样。本副本的起点为 44 页正文、6 页备份。

**直接修改下列 TeX 文件，再重新编译 PDF。** PDF 是编译结果，适合预览与放映；文字、公式、图表说明和排版在源文件中调整。

| 起点页码 | 修改文件 | 对应内容 |
|---|---|---|
| N1–8 | [part-1.tex](part-1.tex) | 封面、作者、研究问题、模型、注意力代理、四个维度及目录 |
| N9–14 | [part-2.tex](part-2.tex) | 数据、三个 URL、Yahoo 页面、会话/订单、补码及归属 |
| N15–23 | [part-3.tex](part-3.tex) | 双样本、内容分类、研究分钟、主题、混合页、窗口和模型表 |
| N24–32 | [part-4a.tex](part-4a.tex) | 实证动机、回归定义、市值、控制后比较、事件及主题倾斜 |
| N33–39 | [part-4b.tex](part-4b.tex) | PCA 输入、两个主成分、交易时点和路径 |
| N40–44 | [part-5.tex](part-5.tex) | 贡献、评价、事实核对表和致谢 |
| A1–A6 | [appendix.tex](appendix.tex) | 备份页；通常无需改动 |

具体到单页的标题、文件和行号见[页面定位表](页面定位表.md)。在编辑器中搜索该页标题，或搜索 `label=...` 即可定位。**页码是当前起点，增删页面后会变化。**

一个普通页面以 `\begin{frame}` 开始，以 `\end{frame}` 结束；章节页用 `\sectionlead`。先只改这些块里的中文、公式或数字。保留 `label=...`、`\jump` 及 `\hyperlink` 的目标名称，可以保持目录与回跳链接。`\finding{...}` 是底部粉色框的文字；`\crumb{...}{...}{...}` 是顶部定位/来源行。表格的 `&` 和 `\\` 分隔列与行，修改时不要误删。

[main.tex](main.tex) 是编译入口，负责读入上述文件与全局元信息，通常不用改。`ruc-research.sty`、`RenminUniv.sty`、`revision-layout.tex` 负责主题和公共布局；只改文字时无需改它们。替换原图或截图时改 `assets/`，并保留来源说明。TikZ 重绘图的数字与绘图代码直接在相应 part 文件里。

在 PowerShell 执行以下命令，无需先切换目录：

```powershell
pwsh -File "D:\softmove\科研项目人大\paper\information-set-argument-v2\projection-20261120-user-edit\build.ps1"
```

脚本会编译两遍。完成后打开 [build/main.pdf](build/main.pdf)，它只覆盖本副本的预览。该路径已经放入一份与第二轮交付相同的起点 PDF，便于立即对照。建议一次修改一两页，编译后检查该页；若报溢出或缺字，先检查本次改动和 `build/main.log`。

`manuscript/` 是内容设计底稿，`约30分钟口述讲稿.md` 是口述稿，**它们不会自动生成或覆盖 TeX**。上屏文字先在 TeX 改，讲述发生变化时再同步讲稿。旧交付的入口说明原样留在 `第二轮交付说明.md`，其链接仍指向第二轮归档文件。

本副本另存为一个本地 Git 起点；后续用 `git diff -- paper/information-set-argument-v2/projection-20261120-user-edit` 可以检查自行修改的内容。无需修改原来已交付的 PDF 或 ZIP。
