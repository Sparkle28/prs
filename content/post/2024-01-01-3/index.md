---
title: '基金研究笔记（四）：大类资产配置'
author: '令纪泽'
date: '2024-01-01'
slug: ''
categories:
  - Work
tags:
  - 基金
  - 资产配置
---

资产配置是指依据投资者的投资目标和风险偏好，在各类资产间分配资金的决策。典型的资产类别包括股票、债券、大宗商品及私募股权等另类资产。Brinson et al.(1991)的经典研究表明，资产配置决定了一个投资组合波动的90%甚至更多，这充分说明了资产配置在现代投资组合管理中的基石地位。若能进行恰当的管理，大类资产配置将为投资组合提供显著的超额收益。

大类资产配置，实质上是通过在不同资产--不同的收益/风险来源之间做分散化投资，最大化投资收益，从而获取更优的长期风险调整后回报。从这个角度来看，Brinson et al.(1991)发现的大类资产配置对于投资组合长期绩效的决定性地位，是非常合情合理的。

大类资产配置可以分为战略性资产配置和战术性资产配置。战略性资产配置基于较长周期的投资研究和决策，战术配置是在战略配置的基础之上基于短期趋势的研判，适当调整权重。

目前，主要可以配置的大类资产包括权益、债券、黄金、货币。

+ 对于权益资产，考虑到当前公募基金持仓主要集中在中证800成分股中，同时中证800指数包含了沪深300、中证500的成分股，整体对于A股权益市场的代表性较强，因此选择中证800指数代表权益资产
+ 对于债券资产，选择覆盖面较广的中证全债指数代表债券资产
+ 对于黄金以及货币资产，分别选择当前存在流动性相对较好的场内基金所跟踪的SGE黄金、中证短融指数代表黄金资产以及货币资产。


将整个策略回测区间固定在2016.01.01-2024.01.01。




# 战略配置模型：固定比例

固定比例配置主要源于主观判断及投资管理目标，如设定固定比例模型的基准为：权益20%+债券70%+黄金5%+货币5%，那么整个区间的资产组合收益如下：

<img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-3-1.png" width="1440" />

```
## 配置比例： [0.2, 0.7, 0.05, 0.05]
```

```
## 年化收益率是4.06%
```

```
## 年化波动率是3.18%
```

```
## 最大回撤是2.44%
```

# 战略配置模型：风险平价模型

风险平价模型是一种投资组合优化方法，旨在通过最小化组合的整体风险（通常以波动率或方差来衡量）来分配资产权重。主要步骤如下：

1. 定义现金权重，由于现金几乎是无风险的资产，故现金不参与权重优化，否在大部分资产都会配置在现金中。不暴露风险则不会获得高收益。这里设置为0.1，表示投资组合中有10%的权重分配给现金。

2. 计算协方差矩阵 cov_matrix，cov_matrix用于衡量资产之间的风险关联性。

3. 使用cvxpy实现风险平价模型： 
  - 定义优化问题的约束条件：确保除了现金权重外的所有资产权重之和等于90%（即1减去现金权重）：所有资产的权重都是非负的。
  - 定义优化目标，使用cp.Minimize来最小化权重和协方差矩阵的二次形式，最小化投资组合的总体风险。

4. 求解可得最优的权重。

```python
cash_weight = 0.1
cov_matrix  = pd.DataFrame(drr_train.iloc[:,:3]).cov()
weights = cp.Variable(num_assets - 1) 
constraints = [cp.sum(weights) == (1 - cash_weight),
              weights >= 0
] 
objective = cp.Minimize(cp.quad_form(weights, cov_matrix))  

prob = cp.Problem(objective, constraints)  
result = prob.solve()  

optimal_weights = list(weights.value) + [cash_weight]
# print('配置比例：',optimal_weights)
asset_ratio = pd.Series(optimal_weights)
```

<img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-3.png" width="1440" />

```
## 配置比例： [0.008820071085146734, 0.8911799289148533, -1.709883997749817e-17, 0.1]
```

```
## 年化收益率是5.57%
```

```
## 年化波动率是1.0%
```

```
## 最大回撤是0.64%
```





```python
cash_weight = 0.1

pca_cov_matrix  = pd.DataFrame(drr_train.iloc[:,:3]).cov()
weights = cp.Variable(num_assets - 1) 
constraints = [cp.sum(weights) == (1 - cash_weight),
              weights >= 0
] 
objective = cp.Minimize(cp.quad_form(weights, pca_cov_matrix))  

prob = cp.Problem(objective, constraints)  
result = prob.solve()  

optimal_weights = list(weights.value) + [cash_weight]
print(optimal_weights)
```

```
## [0.008820071085146734, 0.8911799289148533, -1.709883997749817e-17, 0.1]
```

