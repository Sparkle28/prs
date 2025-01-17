---
title: 投资研究笔记（二）：期权市场观察
author: 令纪泽
date: '2024-05-22'
slug: ''
categories:
  - Work
tags:
  - 资产配置
---

# 期权市场的交易信息可以反映现货市场的情绪

因为：

* 多空方向的情绪博弈：期权拥有4个方向的交易，反应多空方向情绪

* 不同期限反应情绪时间段：期权合约拥有多个到期月份，可以细化不同时间段情绪

* 不同执行价的情绪强弱：投资者对不同执行价期权的选择，反应市场的情绪强弱

* 期权隐波率反应未来预期：根据B-S定价公式，由市场定价的期权价格隐含的波动率反应投资者对未来市场的整体预期

* 细分不同参与类别情绪：机构与个人投资者参与期权交易方式不同，细化情绪

# 期权PCR指标：成交量PCR追踪市场走势

   - PCR指标，即期权认购量（Call）与认沽量（Put）之比，是衡量市场情绪和投资者对未来市场走势预期的重要指标。
   - 持仓量PCR与成交额PCR是PCR指标的两个重要维度，分别反映了市场投资者对未来市场反转的担忧程度（持仓量PCR）和看跌期权与看涨期权上的资金消耗比例（成交额PCR）。

1. **成交量PCR**追踪市场走势：
   - 成交量PCR通常作为反映期权市场投资者情绪的指标在使用，成交量PCR更多的反映期权投资者追涨追跌的情绪
   - 标的持续上涨时，往往伴随着成交量PCR的走弱；标的持续下跌时，成交PCR又会走强


2. **持仓量PCR**反映市场担忧程度：
   - **较高持仓量PCR**：当持仓量PCR较高时，代表投资者对未来标的反转下跌的担忧较为强烈，这通常发生在市场处于上升趋势中，投资者通过持有认沽期权来对冲潜在的市场下跌风险。
   - **较低持仓量PCR**：相反，当持仓量PCR较低时，可能表明投资者正在提前布局认购期权，预期市场将继续上涨或已经处于下跌趋势中，投资者通过持有认购期权来捕捉市场上涨的机会。
   - **波动性**：持仓量PCR的波动较大且分散，没有相对稳定的均值，特别是在均值以上的数据波动更为显著。

3. **成交额PCR**细化投资者行为：
   - **定义**：成交额PCR反映的是看跌期权上消耗的资金与看涨期权上消耗的资金的比值，能够更细致地刻画市场主力的交易行为。
   - **市场主力与极端投机者**：相比成交量PCR，成交额PCR更能反映市场主力的选择倾向，因为它过滤掉了极端投机者在深度虚值期权上的“赌博”行为。市场主力通常更倾向于交易平值附近的期权。
   - **资金消耗视角**：成交额PCR通过资金消耗的角度，提供了对市场情绪和投资者行为的另一重解读，有助于更全面地理解市场动态。

# 期权价格指标：反映市场的分歧度和多空力量强弱







<img src="figures/000016.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/000016.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/000016.SH_PCR2024-01-01.png" width="705" /><img src="figures/000016.SH_PCRNone.png" width="705" /><img src="figures/000300.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/000300.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/000300.SH_PCR2024-01-01.png" width="705" /><img src="figures/000300.SH_PCRNone.png" width="705" /><img src="figures/000852.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/000852.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/000852.SH_PCR2024-01-01.png" width="705" /><img src="figures/000852.SH_PCRNone.png" width="705" /><img src="figures/159901.SZ_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/159901.SZ_DBTP_CGTPNone.png" width="705" /><img src="figures/159901.SZ_PCR2024-01-01.png" width="705" /><img src="figures/159901.SZ_PCRNone.png" width="705" /><img src="figures/159915.SZ_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/159915.SZ_DBTP_CGTPNone.png" width="705" /><img src="figures/159915.SZ_PCR2024-01-01.png" width="705" /><img src="figures/159915.SZ_PCRNone.png" width="705" /><img src="figures/159919.SZ_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/159919.SZ_DBTP_CGTPNone.png" width="705" /><img src="figures/159919.SZ_PCR2024-01-01.png" width="705" /><img src="figures/159919.SZ_PCRNone.png" width="705" /><img src="figures/159922.SZ_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/159922.SZ_DBTP_CGTPNone.png" width="705" /><img src="figures/159922.SZ_PCR2024-01-01.png" width="705" /><img src="figures/159922.SZ_PCRNone.png" width="705" /><img src="figures/510050.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/510050.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/510050.SH_PCR2024-01-01.png" width="705" /><img src="figures/510050.SH_PCRNone.png" width="705" /><img src="figures/510300.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/510300.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/510300.SH_PCR2024-01-01.png" width="705" /><img src="figures/510300.SH_PCRNone.png" width="705" /><img src="figures/510500.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/510500.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/510500.SH_PCR2024-01-01.png" width="705" /><img src="figures/510500.SH_PCRNone.png" width="705" /><img src="figures/588000.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/588000.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/588000.SH_PCR2024-01-01.png" width="705" /><img src="figures/588000.SH_PCRNone.png" width="705" /><img src="figures/588080.SH_DBTP_CGTP2024-01-01.png" width="705" /><img src="figures/588080.SH_DBTP_CGTPNone.png" width="705" /><img src="figures/588080.SH_PCR2024-01-01.png" width="705" /><img src="figures/588080.SH_PCRNone.png" width="705" />



