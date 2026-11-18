# 10份学术slides skill与4份去AI味skill

检索及下载日：2026-11-16。原始文件、commit、SHA256、下载路径见 `vendor/community-skills-2026-11-16/manifest.json`。以下是10个不同仓库中的实际SKILL.md，不用普通演讲指南冒充skill，也不声称它们都受过学术机构认证。

## 学术slides来源

|编号|实际来源|本次采用范围|
|---|---|---|
|S01|[wenlzhang/beamer-skill](https://github.com/wenlzhang/beamer-skill)|Beamer代码、分栏、公式、引用与编译模式；不采用其通用16:9默认|
|S02|[Noi1r/beamer-skill](https://github.com/Noi1r/beamer-skill/blob/main/beamer/SKILL.md)|先修概念、自然章节、图表与正文密度；已由用户提供的时长和听众不重复询问|
|S03|[K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer/blob/main/.claude/skills/scientific-slides/SKILL.md)|学术报告类型、结果占比、计时及逐页视觉检查；图像生成整页的默认与指定LaTeX工程冲突，不采用该后端|
|S04|[aeghnnsw/cc-toolkit: sci-slides](https://github.com/aeghnnsw/cc-toolkit/blob/master/creator-skills/skills/sci-slides/SKILL.md)|执行五遍审阅：含义、定义、图形、措辞、形式；加载slide-text与design参考|
|S05|[DELONG-L/Research-Presentation-Skill](https://github.com/DELONG-L/Research-Presentation-Skill/blob/main/research-presentation/SKILL.md)|单篇PDF的忠实讲述、证据角色及术语一致性；不套HTML输出|
|S06|[Yash-Kavaiya: paper-to-slides](https://github.com/Yash-Kavaiya/research-scholar-agent-skills/blob/main/skills/paper-to-slides/SKILL.md)|先规划讲述、选择主结果、逐页连贯讲稿、备份与超时删减顺序|
|S07|[Faust-Donf/beamer-academic](https://github.com/Faust-Donf/beamer-academic)|中文学术标题与措辞检查、不同内容使用合适构图；不替换RUC主题，不照搬其满版色章节页|
|S08|[thanhlamauto/weekly-research-slides](https://github.com/thanhlamauto/weekly-research-slides)|删除优先的内容审阅、内容/视觉/全稿循环、测量与解释区分；本文不是周进度汇报，不套用其delta-first开场|
|S09|[hanlulong/econ-slides-skill](https://github.com/hanlulong/econ-slides-skill/blob/main/skills/econ-slides/SKILL.md)|主要内容与经济学报告规范：保持论文讲述体裁、尽早交代主要发现、原图优先、精简表、适度限定、结尾回到研究发现|
|S10|[nsinha00/academic-beamer-skill](https://github.com/nsinha00/academic-beamer-skill)|对照其标题连读、单页论证、章节导向及结论收束检查。文件声明proprietary，未找到其完整许可，因此仅作阅读比较，不将原文合并进本地skill或对外源码包|

S01是通用Beamer实现skill，S08偏科研进展，S10偏内容而非特定引擎；已登记适用范围，不将其包装为10份同等适配金融论文的权威标准。另下载的HTML专用academic-slides、通用slides-content、路由型research-presentation列为额外比较，不计入这10份。

## 4份非OpenAI社区去AI味来源

|编号|来源|本次采用的规则|
|---|---|---|
|H01|[blader/humanizer](https://github.com/blader/humanizer)|删无对象的对比、格言式收尾、强凑三项和谈论文稿本身的句子；保留具体内容|
|H02|[op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)|先保留信息、条件和确定程度；处理中文套话、重复与排比；不强制口语化，不为去痕迹编细节|
|H03|[neuromechanist/research-skills: humanizer](https://github.com/neuromechanist/research-skills/blob/main/plugins/manuscript/skills/humanizer/SKILL.md)|研究写作专门校准；删除自我证明式坦诚、预先包装反对意见和反复概念注解，保留改变解释的真实限制|
|H04|[ai-zixun/humanizer-zh](https://github.com/ai-zixun/humanizer-zh)|中文原生句法、段落推进、减少口号收束和机械节奏；保持中性学术语域，不套自媒体作者声音|

H02/H03与H01有继承关系，属于4个社区维护项目，并非4套独立的检测理论；不会用它们计算所谓可靠的“AI率”。本次目标是内容和表达质量，不承诺通过检测器。

## 冲突处理：不自行拼一套任意规则

优先级依S04自身规则：当前用户要求、项目slide-rules、指定模板优先。内容主要执行S09；S04给审阅流程；S02/S06给讲述依赖、讲稿和备份；其他来源只补充相容规则。H02/H03负责中文及研究语域。

具体冲突有原文依据：S09允许经济对象标题，不强制每页assertion；S04默认每页assertion。因此标题以S09为准。S07禁itemize，而S09允许合适的1–4条；本项目保持论文内容决定构图，采用S09，不机械禁用列表。S03图像生成默认、S10通用字体与比例，均让位于用户指定可编辑LaTeX及既有主题。S06英语130词/分钟不能直接套中文，中文讲稿另记字数和停顿预算。S08内置循环最多3轮，本次用户要求3–5轮，采用5次有不同任务的实际审阅，并不伪称运行其命令5次。

## 五轮实质修订及完成证据

1. **内容取舍与体裁**：删重复的自我限定、评议式页面；主要发现提前；将测量细节归入备份。保留r0与r1源码/PDF供比较。
2. **定义与讲述顺序**：每个结果之前交代分析对象、样本与单位；去掉不解释原文结果的通用教学公式；标题连读检查研究主线。
3. **原图与数值**：逐项回原表；截取清晰单面板；补充必要t值与回归口径，避免把图宽当分钟或将PCA当分类。
4. **中文措辞与口述**：按H02/H03逐句删除口号、假对比、无内容收束和预先辩护；讲稿与屏幕分工，术语一致。
5. **形式与整稿**：双遍编译、逐页渲染、页码导航、讲稿对应和时长预算；修复实际发现的拥挤、标题换行、图中文字和引用问题。

每一轮必须留实际问题及修改记录。计划不等于完成；完成情况见qa/information-set/revisions中的记录，不以此清单宣称全部已通过。
