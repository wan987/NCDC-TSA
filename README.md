本项目围绕气象数据展开，涵盖了大数据处理（Hadoop/Hive/Sqoop）、数据分析建模（Python时间序列）和数据可视化（Django/ECharts）三大核心技术栈。经过严格的部署和开发流程，本项目已成功搭建并实现全部功能。
 
1. 技术架构概览 (E-H-P Stack)
模块	使用技术	任务目标	状态
平台搭建	CentOS 7, VMware, Hadoop 2.9.2, Hive 2.1.0, MySQL 5.7	构建 1 Master + 2 Slave 集群，配置 SSH 免密，打通底层环境。	
数据清洗 (ETL)	Java MapReduce	读取 2000-2022 年 NCDC 原始数据，提取基站 ID，格式化为逗号分隔的 clean data。	
数据分析 (SQL)	HiveSQL	统计 2022 年各省/市的平均气温、风速、降水 TOP10、气压等 5 张核心业务表。	
数据预测 (ML)	Python (Pandas/Statsmodels)	使用 Holt-Winters 指数平滑法，基于 2000-2022 年历史数据预测 2023 年全国各省平均气温，并更新到 MySQL。	
数据导出 (ETL)	Sqoop	将 Hive/HDFS 中计算出的 6 张结果表安全、批量地导入到 MySQL 关系型数据库。
数据展示 (Web)	Django, ECharts 5.x, JavaScript	创建 Web 平台，连接 MySQL，渲染中国地图、气温预测折线图、气压矩形树图等 5 大图表。	
 
2. 关键难点突破
在项目实施过程中，遇到了多个技术难点，均通过分析原理得到解决：
1.	Hadoop 集群通讯故障：集群启动后 DataNode 无法加入，经诊断是 Linux 防火墙未彻底关闭所致，通过 systemctl disable firewalld 永久禁用解决。
2.	MapReduce 输入问题：MapReduce 任务无法读取 /china 目录下的子文件夹，通过在 ChinaDriver.java 中增加配置参数 conf.setBoolean("mapreduce.input.fileinputformat.input.dir.recursive", true) 开启递归读取功能解决。
3.	Windows 兼容性：解决了本地 IDEA 运行 Hadoop 客户端时的 Java 11 与 Java 8 冲突（通过调整 Path 优先级）和 Hadoop 客户端 winutils.exe 缺失（通过配置 HADOOP_HOME）问题。
4.	Web 可视化数据崩溃：解决了后端 Python (NumPy) 的 np.int64/NaN 类型传递给前端 JavaScript 时导致浏览器脚本崩溃的问题，最终采用 json.dumps 进行标准序列化传输解决。
Ⅱ. 核心技能掌握与反思
1. 大数据平台运维能力 (Hadoop/Hive/Sqoop)
•	集群管理：熟练掌握 Hadoop 集群的启动、停止、进程监控（jps）和 HDFS 文件系统操作（hadoop fs）。
•	数据仓库：掌握 Hive 外部表和内部表的创建，能够使用复杂的 HiveQL（如 row_number() 窗口函数）进行多维度聚合分析和数据排名。
•	异构数据传输：掌握 Sqoop 导出命令的配置，成功实现了 HDFS 与 MySQL 之间的数据双向流动。
2. MapReduce & 数据建模能力
•	MapReduce ETL：通过编写 ChinaMapper，实现了从文件名中提取 stn（基站 ID）的核心业务逻辑，并成功将原始的空格分隔数据转换成了标准的 CSV 格式，为后续分析奠定了基础。
•	时间序列预测：掌握了 Holt-Winters 指数平滑法的使用，成功预测了全国各省份的气温趋势，并利用 SQLAlchemy 将结果写入关系型数据库。
3. Web 数据可视化能力 (Django/ECharts)
•	Django 架构：掌握了 Django 项目的创建、应用注册、settings.py 数据库连接配置以及路由（urls.py）和业务逻辑（views.py）的编写。
•	前后端分离：实现了后端 Python 视图函数连接 MySQL、处理 Pandas 数据并将其序列化后，通过 mark_safe 传递给前端模板。
•	ECharts 绘制：成功利用 ECharts 绘制了地图、折线图、矩形树图、词云等五种复杂图表，实现了数据的动态切换和可视化展示。
