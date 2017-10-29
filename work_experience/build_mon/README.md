# Coder
1. lili36
 * 异常分析框架
 * 异常分析策略
 * 前端展现
2. zhushengcheng
 * 数据采集
 * 异常处理

# 目录结构说明</br>
monitor-v2</br>
&nbsp;&nbsp;&nbsp;|---bin</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//程序入口</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---access_meta_data.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//访问数据通用接口，包括插入、更新、读取数据，当前基本数据存放在mysql，所以当前基本以操作mysql方法为主</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---Command.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//程序参数处理类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---load_config.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//初始化程序运行时配置；读取用户配置；</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---strategy_schedule.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//策略分析加载；支持私有、共用两种策略加载；如果需要新增策略，需要在这里注册；</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---monitor_start.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//监控启动，由主程序解析到start参数后调用</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---noah.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//noah获取配置库种监控项-值的工具，使用方式：python &nbsp;noah.py &nbsp;kutype</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---modules &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//常用的功能封装方法</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---__init__.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---Util.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---strategy &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//策略module</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---__init__.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---private &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//私有策略module</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---__init__.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---swift_analysis.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---public &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//共用策略module</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---AnalysisBase.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//共有策略分析基类，封装了分析使用的共有方法</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---dag_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//dag分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---download_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//download分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---error_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//error分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---flow_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//flow粒度分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---__init__.py</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---job_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//job粒度分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---kutype_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//kutype粒度分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---output_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//output分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---parser_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//parser分析类</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---transmint_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//写mint分析类</br>
&nbsp;&nbsp;&nbsp;|---call-back &nbsp;&nbsp;&nbsp;//异常处理</br>
&nbsp;&nbsp;&nbsp;|---conf</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---monitor.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//监控agent配置，包含mysql配置、分析策略注册等</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---register.json &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//库种监控配置，自定义配置监控库种简单属性，调用的监控项</br>
&nbsp;&nbsp;&nbsp;|---data &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//存放程序debug信息</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---debug_public_strategy.data &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//程序共有策略的debug中间数据，方便程序异常分析定位；由debug级别控制输出内容丰富度；</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---debug_private_strategy.data &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//程序私有策略的debug中间数据，方便程序异常分析定位；由debug级别控制输出内容丰富度；</br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---debug_sql_sentence.data &nbsp;&nbsp;&nbsp;//程序所有mysql操作的sql语句记录，方便程序异常分析定位；</br>
&nbsp;&nbsp;&nbsp;|---log&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//存放程序log信息</br>
&nbsp;&nbsp;&nbsp;|---web&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//前端展示页面</br>
&nbsp;&nbsp;&nbsp;|---makefile &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//makefile文件</br>
&nbsp;&nbsp;&nbsp;|---status &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//库种的监控值输出目录</br>
&nbsp;&nbsp;&nbsp;|---tmp &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//临时文件存放</br>
