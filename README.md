# 科研论文汇报项目

当前论文：Laarits、Wurgler，*On the Information Set of Individual Investors*，本地2026-04-27工作稿，70页。

## 本轮研究文稿

最新为按用户手改生成的[汇报总结版 PDF](output/information-set-projection-20261120-user-final/个人投资者的信息集_用户定稿_汇报总结版.pdf)，[TeX 入口](paper/information-set-argument-v2/projection-20261120-user-final/README.md)与[对照记录](docs/2026-11-18_用户定稿对照与总结页调整.md)。其余历史版本继续保留。

**当前交付是第二轮仔细微调。** [放映 PDF](output/information-set-projection-20261120-round2/个人投资者的信息集_11-20组会放映_第二轮.pdf)、[工程与交付入口](paper/information-set-argument-v2/projection-20261120-round2/README.md)、[语义校订](docs/第二轮微调_01_语义校订与执行规范.md)、[逐页清单](docs/第二轮微调_02_逐页调整清单.md)和[核查记录](docs/第二轮微调_03_核查记录.md)。正文 44 页，备份 A1–A6；六块 Markdown/TeX 分阶段修改并提交。另有完整口述稿及约 30 分钟预算。下列版本保留作历史对照。

用户自行调整请使用独立的[用户微调版](paper/information-set-argument-v2/projection-20261120-user-edit/README.md)。复制起点与第二轮一致，附逐页文件定位和编译命令；在该副本修改 TeX 后重新生成 PDF。

11 月 20 日组会改版已单独成稿。入口包括[放映 PDF](output/information-set-projection-20261120/个人投资者的信息集_11-20组会放映.pdf)、[编译与讲述说明](paper/information-set-argument-v2/projection-20261120/README.md)和[语音校订及逐页改版方案](docs/2026-11-20_语音校订与逐页改版方案.md)。正文 41 页，备份 A1–A6。

11 月 18 日的[32 页无水印人大 Beamer PDF](output/information-set-projection-20261118/个人投资者的信息集_组会放映.pdf)留作旧版对照，编译入口、讲述时标和验收记录见[旧版源码说明](paper/information-set-argument-v2/projection-20261118/README.md)。

2026-11-18新版为[汇报叙事与视觉稿](paper/information-set-argument-v2/manuscript/汇报叙事与视觉稿.md)。同一份Markdown包含完整论证、32个展示单元、关键图件、读图顺序与版式参数，以及与《AI初始分析》的逐段比较。

上一阶段的[五章研究底稿](paper/information-set-argument-v2/manuscript/README.md)收录连续正文、结构比较和证据定位，供对照与回查。

用户关注点及事实纠偏已写入[研究叙述规范与反馈落实](docs/2026-11-17_研究叙述规范与反馈落实.md)，并更新AGENTS与项目skill。五章约1.3万汉字，是研究解释底稿，不是逐字口述稿。

## 保留的46页基线材料

2026-11-17已把用户 `half_material` 中的最新46页材料接入。当前版本是待重写的工作基线，内容尚未认可。

|入口|用途|
|---|---|
|[46页PDF](output/information-set-argument-v2/01_组会报告_46页.pdf)|用户最新放映文件，原样复制|
|[46页PPTX](output/information-set-argument-v2/01_论证重建_46页.pptx)|用户最新PPT，含46页对应备注|
|[逐页讲稿](output/information-set-argument-v2/02_逐页逐字稿_46页对应.docx)|用户最新DOCX，原样复制|
|[内容诊断与四部分重写方案](paper/information-set-argument-v2/内容诊断与四部分重写方案.md)|以原文和当前页码说明问题、原因及连续文稿方案|
|[源码说明](paper/information-set-argument-v2/README.md)|JSON、TeX、主题、原论文裁剪及代码用法|
|[整理记录](docs/2026-11-17_材料接入与清理记录.md)|导入、删除、保留范围及真实检查边界|

46页基线的编辑入口为 `paper/information-set-argument-v2/slides.json`，当前新叙述在manuscript目录独立研究和写作，不从旧页JSON生成。旧稿源代码讲述预算47分25秒，未进行真人计时，超过原先30多分钟目标。

## 构建与检查

在项目根目录运行：

```powershell
$env:PYTHONUTF8='1'
python scripts/verify_argument_v2.py
python scripts/build_argument_v2.py
python scripts/build.py paper
```

前两条分别检查输入接入一致性、导出当前源文件；第三条编译两遍，结果在当前paper目录的 `build/`，不会覆盖用户导入的放映PDF。明确需要重新生成DOCX时，使用 `python scripts/build_argument_v2.py --documents`。PPTX导出环境说明见源码README。

本轮确认三份原件哈希一致、PDF/PPTX各46页、46页备注和DOCX讲稿与源内容对应；LaTeX两遍编译及日志检查通过。没有重新导出PPTX或重做DOCX，没有进行新版全套视觉验收，也没有声称内容合格。

## 保留的工具性材料

- `AGENTS.md`、`docs/`：用户要求、历史纠偏、经验、来源取舍及此次整理记录。
- `skills/academic-paper-beamer/`、`vendor/`：本地skill、原生社区skill、固定版本、许可与上游源码。
- `reusable/`、通用模板ZIP及模板测试：无水印RUC主题与可复用设计。
- `reusable/legacy-tools/`：此前的裁剪、DOCX、公式、验证、打包和归档工具设计；历史路径可能失效，不能作为当前入口。
- `raw_reference/chatgpt-export_论文深度讲解.md`：保留用户提示与纠偏历史；其中夹带的旧报告片段不作为当前正文或原始证据。
- `sources/`与根目录原论文：原始学术材料及参考资料。

旧40页、45页的正文、成品、重复源码包、预览图和内容快照已从项目工作目录删除；修订经验另存 `docs/history/`。`half_material`保留原样，作为本次输入。后续重点是先写完整研究解释，再按听众理解需要转为页面。
