# RUC Beamer 中文汇报模板（无水印版）

这是基于 RUC Beamer Theme 的 LaTeX 演示文稿模板。它沿用 4:3 画幅、酒红配色（`#971F30`）、顶部章节导航、中文楷体和双行页脚。七页样例涵盖封面、目录、分栏、公式、三线表、可编辑流程图和可选附录，正文为通用占位内容。

## 开始使用

1. 将整个文件夹复制到新项目，或将 ZIP 解压到新文件夹。
2. 修改 `main.tex` 顶部的标题、姓名、机构和日期。用 `\section{章节名}` 设置目录与顶部导航，按需复制或删除 `frame`。页脚使用标题和姓名等命令方括号里的短文本。
3. 在 `main.tex` 所在目录运行以下两遍 XeLaTeX，生成 `main.pdf`。第二遍会更新目录、引用和总页数。

```sh
xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

在 Overleaf 中可上传 ZIP 创建项目，主文件选择 `main.tex`，编译器选择 **XeLaTeX**。

## 依赖

本地需要配有 XeLaTeX 的 TeX 发行版，例如完整安装的 TeX Live。精简安装时，需要补齐 `beamer`、`fontspec`、`xecjk`、`lm`、`amsmath`、`amsfonts`、`booktabs`、`graphics`、`tools`、`pgf` 和 `fandol`。中文优先使用系统中的 KaiTi 和 FangSong，缺少时分别使用 TeX 发行版的 FandolKai 和 FandolFang。工程只使用包内的主题文件和 TeX 环境的宏包与字体，流程图由 TikZ 直接生成。

## 文件与来源

| 文件 | 用途 |
| --- | --- |
| `main.tex` | 编辑封面、章节和页面的主文件 |
| `ruc-research.sty` | 本地派生层，控制无水印背景、字体、页脚和来源小字 |
| `RenminUniv.sty` | 原样保留的上游主题样式 |
| `LICENSE-RUC.txt` | 上游主题的 MIT 许可 |

`RenminUniv.sty` 来自 Wenquan Wu 的 GitHub 仓库，使用 MIT 许可，版本为 `cb04e44c9f66ba000a63615993d052ed389200ea`。[RUC Beamer Theme 源码](https://github.com/GohUnTsuan/RUC-Beamer-Theme/tree/cb04e44c9f66ba000a63615993d052ed389200ea)

本地派生层在加载原主题后清空校徽背景，封面使用普通标题页。目录按需插入。封面免编号，正文显示当前页和总页数，附录独立显示为 A1/1 等。重新分发时随附上游 MIT 许可。
