"""R1: deletion-first, restore an economics paper-talk rather than an audit deck."""
from pathlib import Path
import re,shutil,json
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';old=(R/'qa/information-set/revisions/r0_rejected/main.tex').read_text(encoding='utf-8')
F={}
for m in re.finditer(r'% (\d\d)\s*\n(.*?)(?=\n(?:\\(?:sub)?section|% \d\d|\\appendix|\\end\{document\}))',old,re.S):
 F[int(m[1])]=m[2].strip()
def frame(title,body):return '\\begin{frame}{'+title+'}\n'+body.strip()+'\n\\end{frame}'
def retitle(n,title):return re.sub(r'\\begin\{frame\}\{[^\n]+\}',lambda m:'\\begin{frame}{'+title+'}',F[n],count=1)
frames=[]
def add(section,sub,body):frames.append(dict(section=section,sub=sub,tex=body))
add('研究问题','',r'\begin{frame}[plain,noframenumbering]\titlepage\end{frame}')
add('研究问题','信息与交易',frame('投资者根据什么信息交易？',r'''
资产定价理论对投资者使用的信息有不同设定：
\medskip
\begin{tabularx}{\linewidth}{@{}L{3.7cm}Y@{}}\toprule
模型中的信息输入 & 对应的投资判断\\\midrule
收益方差、协方差 & 风险与组合配置\\
盈利、现金流和分红 & 公司基本价值\\
过去价格和收益 & 趋势与收益外推\\\bottomrule
\end{tabularx}
\medskip 实际交易前，投资者分别获取了多少这类信息？
'''))
add('研究问题','本文发现',frame('本文：直接观察个体投资者的股票研究',r'''
浏览器记录覆盖经纪商及财经网站，可连接研究时间、主题和交易。
\begin{enumerate}\setlength\itemsep{8pt}
\item \textbf{交易标的上的研究较短}：中位数约6分钟，均值约半小时。
\item \textbf{价格信息占优}：图表居首，分析师信息其次。
\item \textbf{研究方式不同}：信息侧重与投机性股票倾向相关。
\end{enumerate}
\source{Laarits与Wurgler（2026），Tables 2--5。第1项来自高匹配率50户子样本。}
'''))
add('研究问题','文献位置',retitle(4,'从注意强度到信息内容'))
add('研究问题','汇报安排',frame('汇报安排',r'''
\begin{enumerate}\setlength\itemsep{10pt}
\item 数据：跨网站浏览与交易记录
\item 信息获取：研究深度、主题与股票特征
\item 研究过程：投资者差异、交易时点与搜索路径
\item 讨论：对信念形成研究的启示
\end{enumerate}
'''))
add('数据','',r'\partguide{一、数据}{跨网站浏览与交易记录}{样本筛选\qquad 股票匹配\qquad 研究主题分类}')
add('数据','样本',retitle(7,'数据：484户家庭的浏览记录'))
add('数据','交易识别',frame('从订单网页识别买卖事件',r'''
交易识别依据股票代码、订单方向及相关网页序列。
\medskip
\begin{tabularx}{\linewidth}{@{}L{3cm}Y@{}}\toprule
处理步骤 & 规则\\\midrule
同股、同方向记录 & 30分钟内连续出现，合并为一笔\\
合并交易时间 & 取序列最后一次记录\\
研究样本 & 至少有一笔美国普通股或ADR交易\\\bottomrule
\end{tabularx}
\medskip 最终识别2,911笔合并交易。
\orig{§II与Appendix；合并用于避免重复网页记录}
'''))
add('数据','研究分类',frame('研究内容按网页功能分类',r'''
\begin{tabularx}{\linewidth}{@{}L{3.3cm}Y@{}}\toprule
网页内容 & 主题\\\midrule
价格及交易技术 & 价格图表、技术分析\\
财务及估值信息 & 盈利、分红、其他基本面\\
专业判断与持有人信息 & 分析师、所有权、风险统计\\
公司网站 & 按研究关联及时间上限计入\\\bottomrule
\end{tabularx}
\medskip Snapshot、新闻、留言板等混合页面另外处理。\par
登录、转账、下单及持仓展示不计为研究。
\orig{§III与Appendix，pp.58--70}
'''))
add('数据','股票匹配',retitle(10,'股票匹配：全样本与50户子样本'))
add('信息获取','',r'\partguide{二、信息获取}{研究深度、信息主题与股票特征}{每笔投入多少时间？\qquad 主要研究哪些内容？}')
add('信息获取','研究时间',retitle(13,'交易标的研究：中位数5.7分钟'))
add('信息获取','时间分布',retitle(14,'研究时间的分布高度右偏'))
add('信息获取','显式访问',frame('直接访问也以价格图表为主',r'''
\begin{table}\centering
\caption{直接识别的研究类别：全样本摘录}\label{tab:direct}
\begin{tabularx}{\linewidth}{@{}Yrr@{}}\toprule
类别 & 分钟/笔，均值 & 有访问的家庭\%\\\midrule
价格图表 & 39.1 & 93\\
分析师 & 12.5 & 71\\
其他基本面 & 2.6 & 53\\
盈利 & 1.7 & 40\\
分红 & 0.6 & 17\\\bottomrule
\end{tabularx}\end{table}
\medskip 价格类关注既体现在投入时间，也体现在覆盖家庭数。
\orig{Table 3，p.48；分摊前，484户}
'''))
add('信息获取','混合内容',retitle(15,'混合页面分摊后，价格图表仍居首'))
add('信息获取','风险信息',retitle(16,'很少有家庭专门查询风险统计'))
add('信息获取','图表期限',retitle(18,'图表期限：默认窗口与主动选择'))
add('信息获取','股票关注',retitle(19,'市值与研究关注广度'))
add('信息获取','相对侧重',frame('价格与基本面关注的相对侧重',r'''
因变量：价格类关注家庭百分比减去基本面类关注家庭百分比。
\begin{table}\centering\small
\caption{股票—月份回归，原表第(5)列摘录}\label{tab:relative}
\begin{tabularx}{\linewidth}{@{}Yrr@{}}\toprule
标准化股票特征 & 系数 & $t$值\\\midrule
波动率 & 0.04*** & 3.67\\
过去第2--12月收益 & 0.05** & 2.25\\
分析师覆盖 & -0.09** & -2.40\\\bottomrule
\end{tabularx}\end{table}
\small 行业固定效应；3,962个观测。***、**分别为1\%、5\%。
\medskip 波动及较早收益，与价格类相对关注正相关。
\orig{Table 4，pp.49--50；两类家庭可重叠}
'''))
add('信息获取','事件',retitle(20,'财报公告附近的研究活动'))
add('研究过程','',r'\partguide{三、研究过程}{研究差异、交易时点与搜索路径}{投资者之间如何不同？\qquad 一次研究如何展开？}')
add('研究过程','异质性',frame('用主成分概括研究侧重',r'''
\begin{tabularx}{\linewidth}{@{}L{3.2cm}Y@{}}\toprule
PCA输入 & 构造\\\midrule
各主题的研究活动 & 每月是否超过2分钟\\
投机性股票倾向 & 对高波动、小市值、年轻、低价股的侧重\\\bottomrule
\end{tabularx}
\medskip
\textbf{第一成分}：多数主题载荷同向，解释26.81\%方差。\par
\medskip
\textbf{第二成分}：短期信息与盈利、分红的相对侧重，解释8.77\%。
\orig{Table 5，p.51；股票匹配研究；风险类因访问过少排除}
'''))
add('研究过程','研究侧重',retitle(23,'信息侧重与投机性股票倾向'))
add('研究过程','交易时点',frame('平均研究时间在交易前集中增加',r'''
\centering\includegraphics[width=.70\linewidth,height=5.6cm,keepaspectratio]{assets/timing_mean.pdf}
\orig{Figure 3左面板，p.54；50户；横轴为相对交易小时，纵轴为累计分钟}
'''))
add('研究过程','交易时点',frame('中位数投资者的研究更接近交易时点',r'''
\centering\includegraphics[width=.70\linewidth,height=5.6cm,keepaspectratio]{assets/timing_median.pdf}
\orig{Figure 3右面板，p.54；50户；最右端符号表示48小时以后的累计总量}
'''))
add('研究过程','路径构造',retitle(27,'从网页序列构造跨主题搜索路径'))
add('研究过程','搜索路径',retitle(28,'多数路径在少量主题后结束'))
add('研究过程','路径差异',frame('投机性侧重较强者的搜索更集中',r'''
\begin{columns}[T]
\begin{column}{.49\linewidth}\centering\small 第二主成分最低五分位\par
\includegraphics[width=\linewidth,height=4.1cm,keepaspectratio]{assets/less_spec_paths.pdf}\end{column}
\begin{column}{.49\linewidth}\centering\small 第二主成分最高五分位\par
\includegraphics[width=\linewidth,height=4.1cm,keepaspectratio]{assets/more_spec_paths.pdf}\end{column}
\end{columns}
\small 低分组的研究分布于更多主题；高分组较集中于Snapshot与价格。
\orig{Figure 5C/D，p.56；交易前10天路径，按第二主成分分组}
'''))
add('讨论','理论含义',frame('对信念形成模型的启示',r'''
\begin{tabularx}{\linewidth}{@{}L{3.3cm}Y@{}}\toprule
可观察事实 & 需要解释的理论对象\\\midrule
价格信息受到较多关注 & 投资者如何从历史价格推断收益\\
基本面研究强度不一 & 不同投资者如何选择信息来源\\
搜索临近交易发生 & 研究的停止规则与交易决策\\\bottomrule
\end{tabularx}
\medskip 本文提供信息获取事实，后续可与调查信念及账户持仓连接。
'''))
add('讨论','讨论问题',frame('讨论：短时间研究反映了什么？',r'''
观察到的研究时间较短，至少有两种经济解释：
\medskip
\textbf{新增信息有限}：投资者依赖少量显著信号作出交易决定。\par
\medskip
\textbf{新增需求有限}：投资者已有知识、持仓经验或其他信息来源。
\bigskip
区分二者，需要研究前的信息与信念，以及研究后的配置结果。
'''))
add('讨论','结论',frame('结论',r'''
跨网站浏览记录显示，个体投资者的股票研究具有明显的信息侧重。
\begin{itemize}\setlength\itemsep{10pt}
\item 价格图表最受关注，分析师信息其次。
\item 研究投入分布右偏，交易前出现集中搜索。
\item 投机性股票倾向与较集中的短期信息研究共同出现。
\end{itemize}
\medskip 解释信念形成，需要将这种信息选择纳入模型。
'''))
# 9 backups, covering precisely named anticipated questions.
add('备份','',retitle(11,'A1\quad 每笔研究时间：分母与家庭权重'))
add('备份','',retitle(8,'A2\quad 浏览、交易与路径的时间单位'))
add('备份','',retitle(36,'A3\quad 主题分摊前后的数值'))
add('备份','',retitle(37,'A4\quad 股票特征回归的推断口径'))
add('备份','',retitle(38,'A5\quad PCA的构造与稳健性问题'))
add('备份','',retitle(26,'A6\quad 累计研究时间的构造'))
add('备份','',retitle(29,'A7\quad 买入与卖出前的研究路径'))
add('备份','',retitle(39,'A8\quad 复现时需确认的测量细节'))
add('备份','',retitle(40,'A9\quad 主要参考文献'))
assert len(frames)==40,len(frames)
preamble=old[:old.index('\\begin{document}')]
preamble=re.sub(r'\\subtitle\{[^\n]*\}\n','',preamble)
preamble=preamble.replace('\\author[Laarits \\& Wurgler]{Toomas Laarits \\qquad Jeffrey Wurgler}',r'\author[Laarits \& Wurgler]{\texorpdfstring{Toomas Laarits\quad Jeffrey Wurgler}{Toomas Laarits; Jeffrey Wurgler}}')
preamble=preamble.replace(r'\institute[NYU Stern · 论文组会]{NYU Stern School of Business}',r'\institute[NYU Stern]{NYU Stern School of Business\\Jeffrey Wurgler: also NBER}')
preamble=preamble.replace('40 physical pages: cover + 33 main frames + 6 appendix frames.','40 physical pages: cover + 30 main frames + 9 appendix frames.')
out=[preamble,'\\begin{document}'];sec=sub=None
for i,x in enumerate(frames,1):
 if i==32:out.append('\\appendix\n\\section*{备份}');sec='备份'
 if x['section']!=sec:out.append('\\section{'+x['section']+'}');sec=x['section'];sub=None
 if x['sub'] and x['sub']!=sub:out.append('\\subsection{'+x['sub']+'}');sub=x['sub']
 out.append(f'% Physical page {i:02d}\n'+x['tex'])
out.append('\\end{document}')
(P/'main.tex').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
(P/'frame_manifest.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2),encoding='utf-8')
print('R1: reorganized 40 pages; 30 numbered main frames, 9 backups')
