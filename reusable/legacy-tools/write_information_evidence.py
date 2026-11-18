from pathlib import Path
import csv,json,shutil
R=Path(__file__).resolve().parents[1];P=R/'paper/information-set';rows=[]
def put(slide,src,page,quantity,value,unit,sample,note='原表摘录'):
 rows.append({'slide_physical_page':slide,'source_object':src,'source_pdf_page':page,'quantity':quantity,'value':value,'unit':unit,'sample':sample,'verification':note})
for q,v,u in [('家庭数','484','户'),('合并交易数','2911','笔'),('网址约数','8500000','条')]:put('7,8','§II/Table 1',46,q,v,u,'全样本')
for q,v in [('年龄均值','50.1'),('年龄中位数','50.0')]:put(7,'Table 1',46,q,v,'岁','467户')
for q,v in [('每月交易均值','2.2'),('每月交易中位数','0.7')]:put(7,'Table 1',46,q,v,'笔/月','484户；家庭—月份归一化')
for sample,q,mean,med in [('484户','全部研究/每笔','144.2','36.4'),('50户','全部研究/每笔','96.8','51.7'),('50户','交易标的研究/每笔','29.1','5.7'),('484户','全部研究/每月','118.0','37.1')]:
 for stat,val in [('均值',mean),('中位数',med)]:put('12,13','Table 2',47,q+stat,val,'分钟',sample)
for quant,v in [('P5','0.0'),('P25','1.7'),('P50','5.7'),('P75','31.5'),('P95','157.4')]:put(13,'Table 2C',47,'交易标的每笔研究'+quant,v,'分钟','50户')
for q,m,pct in [('价格图表','39.1','93'),('分析师','12.5','71'),('其他基本面','2.6','53'),('盈利','1.7','40'),('分红','0.6','17'),('风险','0.0','1'),('Snapshot','37.0','93')]:
 put('14,16,34','Table 3',48,q+'直接访问均值',m,'分钟/笔','484户','直接查看横向原表；风险0.0为取整')
 put('14,34','Table 3',48,q+'有直接访问家庭',pct,'百分比','484户','原表取整百分比')
for q,m,med in [('价格图表','64.4','14.7'),('分析师','18.6','2.1'),('盈利','10.6','1.8'),('其他基本面','6.8','1.1'),('分红','4.6','0.8'),('风险','1.8','0.2')]:
 for stat,val in [('均值',m),('中位数',med)]:put('15,16,34','Table 3',48,q+'分摊后'+stat,val,'分钟/笔','484户')
put(16,'§III',22,'明确查询风险统计家庭','7','户','484户','正文数值；不能将取整时间0.0读成无访问')
for q,b,t in [('第1列ln市值','1.03','14.42'),('第3列ln市值','1.13','11.35'),('第3列波动率','0.09','2.80'),('第5列波动率','0.04','3.67'),('第5列过去2至12月收益','0.05','2.25'),('第5列分析师覆盖','-0.09','-2.40')]:
 put('18,19','Table 4',49,q+'系数',b,'因变量百分点/自变量标准差','3962股票—月份；市值前1000股')
 put('18,19','Table 4',49,q+'t值',t,'t','同上；NW lag 2 months')
for q,v in [('第1列R2','0.315'),('第3列R2','0.484'),('观测数','3962')]:put(18,'Table 4',50,q,v,'原表单位','股票—月份')
for q,v in [('留言板','.46'),('投机性股票倾向','.43'),('Snapshot','.30'),('价格图表','.19'),('分红','-.47'),('盈利','-.34'),('其他基本面','-.29'),('技术分析','-.11')]:put(23,'Table 5',51,'第二主成分'+q,v,'载荷','家庭层面PCA')
put(22,'Table 5',51,'第一成分解释方差','26.81','百分比','家庭层面PCA')
put('22,23','Table 5',51,'第二成分解释方差','8.77','百分比','家庭层面PCA')
put(23,'Table 5',51,'前两成分方差合计','35.58','百分比','家庭层面PCA','派生：26.81+8.77；非原文新增估计')
put(26,'Figure 4 caption',55,'融合研究路径数','16930','家庭—股票—窗口','484户')
put(26,'Figure 4 caption',55,'融合窗口','10','天','同家庭同股')
put(26,'Figure 4 caption',55,'起始排除期','20','天','样本前20天开始研究的股票排除')
with (P/'evidence.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
shutil.copy2(R/'sources/information-set/version.json',P/'source_version.json')
print('wrote',len(rows),'traceable evidence records')
