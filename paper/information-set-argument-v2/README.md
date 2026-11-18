# 当前46页工作基线

2026-11-18的内容工作入口为[汇报叙事与视觉稿](manuscript/汇报叙事与视觉稿.md)。下文记录46页基线及相应工具用法。

2026-11-17从用户的 `half_material` 接入。当前文件是待重写的工作基线，更新完成不代表内容获得认可。

- 用户原始成品：`../../output/information-set-argument-v2/`，PDF、PPTX、DOCX均按字节复制。
- 内容编辑入口：`slides.json`；页面、讲稿、预计秒数分别保存，尚保留现稿内容。
- LaTeX：`main.tex`、两份主题及 `assets/`；四组图片均为当前页面仍使用的原论文裁剪。
- 原文：根目录70页、2026-04-27工作稿；`sources.json`记录来源。
- 旧证据定位：`legacy_evidence.csv`，只用于回查原文，其中旧报告页码已经失效，不作为当前页码。
- 内容诊断：`内容诊断与四部分重写方案.md`。

源内容7202个汉字，代码讲述预算2845秒，即47分25秒；未进行真人演练。原DOCX写“约47分钟”。

## 使用代码

在项目根目录执行：

```powershell
$env:PYTHONUTF8='1'
python scripts/verify_argument_v2.py
python scripts/build_argument_v2.py
python scripts/build.py paper
```

第一条检查接入完整性及讲稿一致性；第二条从当前JSON导出TeX和Markdown，不改写用户DOCX；第三条编译两遍并检查日志，结果在本目录 `build/`，不会覆盖导入的放映PDF。明确需要重做DOCX时，第二条加 `--documents`；此后导入原件哈希检查应改为新版本验收。

`scripts/build_argument_v2_generated.mjs`保留PPTX导出工具；旧机器硬编码已改为环境变量。须从当前会话的 `load_workspace_dependencies` 获取 `RUNTIME_NODE_MODULES`、`CODEX_BUNDLED_PYTHON`，完整验证还需 `CODEX_PRESENTATIONS_SKILL`。本轮只做语法检查，没有重新导出PPTX。导入的PPTX仍为用户原件。

`half_material`保留原样，作为此次输入；下一次更新须另做差异核对，不重复运行已经完成的一次性清理脚本。
