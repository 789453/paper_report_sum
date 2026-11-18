# 来源、采用范围与取舍

检索/访问：2026-11-15。来源不是同一层次的权威；机构建议、软件规范、社区经验和用户要求分别使用。除开源原件归档外，下列内容是摘要与实施判断，不大量复制原文。

| ID | 来源及地址 | 采用内容 | 不照搬之处 |
|---|---|---|---|
| H1 | Heidelberg, Vanberg & Enders, [Guidelines for presenting a research paper](https://www.uni-heidelberg.de/md/awi/professuren/wipol/seminar_presentation_guidelines.pdf) | 先提核心问题和结论；实验设计服务于假设；区分统计结果与解释、内部与外部有效性 | 原指南以 15–30 分钟为场景，不把其页数例子作为本项目硬限制 |
| H2 | LSE EC501, [Guidelines for Presentations](https://personal.lse.ac.uk/fischerg/Assets/EC501PresentationGuidelines.pdf) | 尽早讲问题、贡献和主要威胁；写明识别与变量；表格保留核心结果 | 不执行其课程报送/邮件要求；18/22pt 建议不直接套到物理尺寸不同的 Beamer PDF |
| M1 | MIT Communication Lab, [Virtual Presentations](https://mitcommlab.mit.edu/broad/commkit/virtual-presentations/) | 内容围绕主要信息和听众目的；事先演练 | 不把线上技术安排当作线下组会硬要求 |
| E1 | Michael Ernst, University of Washington, [How to give a technical presentation](https://homes.cs.washington.edu/~mernst/advice/giving-talk.html) | 为组会留讨论时间；用演练发现结构问题；页码便于反馈 | 不照搬计算机学科示例 |
| B1 | Beamer maintainers, [beamerug-guidelines.tex](https://github.com/josephwright/beamer/blob/main/doc/beamerug-guidelines.tex) | 文字密度与字体选择；主题应服务于内容；避免 shrink 强塞内容 | 本项目保留用户指定主题，不改为作者偏好的其他主题 |
| C1 | CTeX 官方维护入口，[CTAN ctex](https://ctan.org/pkg/ctex)、[CTAN xeCJK](https://ctan.org/pkg/xecjk) | 中文支持与引擎/字体配置；依赖冲突时采用 xeCJK 直接实现中文 | 字体可用性需本机编译验证；本次未调用 CTeX 的中文章节编号功能 |
| T1 | TeX Stack Exchange, [Fit a table into a beamer's frame](https://tex.stackexchange.com/questions/395885/fit-a-table-into-a-beamers-frame) | 认识到缩小表格会损害投影阅读，回溯 Beamer 手册后优先拆表 | 不采纳帖子里的 shrink 示例作为生产方案 |
| N1 | TeX Stack Exchange, [Don't count backup slides](https://tex.stackexchange.com/questions/70448/dont-count-backup-slides/70495)；维护者 [Beamer news 2023](https://tug.org/TUGboat/tb44-2/tb137samcarter-beamernews23.pdf) | 主体与附录独立计数；优先原生计数机制并实测 | 不叠加多个修改计数器的旧补丁 |
| Q1 | [CTAN booktabs](https://ctan.org/pkg/booktabs) | 三线表与表格排版工具 | 软件提供能力，不证明某一特定版式为学术唯一标准 |
| O1 | Overleaf 官方，[Beamer](https://www.overleaf.com/learn/latex/Beamer) | frame、目录、主题与基础结构 | 本项目用本地 XeLaTeX，不要求云端账号 |
| R1 | Wenquan Wu, [Overleaf 模板](https://cn.overleaf.com/latex/templates/ruc-beamer-theme/ssryphkjpyjt)；[作者仓库](https://github.com/GohUnTsuan/RUC-Beamer-Theme) | 原模板、层级、颜色与背景机制 | 官网标 CC BY 4.0，GitHub 标 MIT；分别保留对应说明，不把许可证混称 |
| K1 | wenlzhang, [beamer-skill](https://github.com/wenlzhang/beamer-skill) | 已有 skill 的模式目录、分栏、notes、源代码交付和视觉检查 | 这是社区 skill，不是 OpenAI 或 Beamer 官方；不照搬英文、pdflatex 和缩字建议；Beamer 已加载 hyperref，不机械强制再次最后加载 |
| P1 | ABFER，[作者原始报告 PDF](https://abfer.org/media/abfer-events-2022/annual-conference/slides-accounting/Xiaofeng-ZHAO-presentation.pdf) | 作为真实报告范例，观察“动机—知识—设计—证据—讨论”的讲述顺序 | 2022 年报告，不作为 2026 年正式版数值依据；不是通用格式标准 |

## 原件归档与版本

- RUC 仓库 commit：`cb04e44c9f66ba000a63615993d052ed389200ea`；原件在项目 `vendor/RUC-Beamer-Theme/`，含 LICENSE。水印来自 `RenminUniv.sty` 末尾 `\setbeamertemplate{background}{...}`。未发现独立无水印源文件，本地生成派生版本。
- 社区 Beamer skill commit：`f98a66bb1d3c5d93fa21a07c5151afedf2b1d535`；完整原件在项目 `vendor/beamer-skill/`，含 LICENSE、NOTICE 及 reference。衍生 skill 不冒称该作者作品。
- H1、H2、P1 的 PDF 已归档到 `sources/`。B1 原始指南已归档；其他网页的关键采用点在本表登记。
- 本 skill 是有来源的工作流组合。没有检索到可直接满足“中文＋本模板＋金融实验论文＋版本审计”的官方现成 skill，因此组合现有 skill 与专业指南，而不是虚构存在这样的现成成品。

## 冲突的处理

用户选择决定模板、语言与用途；官方文档决定语法与软件行为；机构指南决定论证和交流质量；社区案例提供排错思路。数字、因果结论和论文版本只能由论文及可核实一手来源决定，不能由演示指南推出。
