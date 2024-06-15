---
title: "基金研究笔记（五）：基于大类资产配置的FOF组合"
author: "令纪泽"
date: "2024-01-20"
categories: Work
tags:
- 基金
- 资产配置
slug: fof
---

FOF组合的配置精髓在于大类资产的组合带来的Beta收益，基于上一篇笔记提到的风险平价模型，选取四类资产进行组合：股票、债券、黄金、现金

在具体配置时，利用各大类资产的指数来跟踪其收益率，具体地：
  + 股票：000906.SH
  + 债券：H11001.CSI
  + 黄金：AU9999.SGE
  + 现金：H11014.CSI





 `get_assets_weight`这个函数用于根据指定的优化策略计算资产的权重，同时考虑是否要加入现金比率作为权重的一部分。

**参数说明：**

- `data_slice`：一个包含资产历史数据的数据框（DataFrame），用于计算权重。
- `strategy_flag`：一个字符串，表示要使用的优化策略类型。
- `cash_rate`：一个浮点数，表示现金的权重比率，默认为0.1（即10%）。

**实现步骤**

  * **1. 策略映射**：函数首先定义了一个名为 `optimization_strategies` 的字典，将策略标志映射到对应的优化策略类。这样，通过 `strategy_flag` 参数，函数可以灵活地选择不同的优化算法。  
  
  * **2. 获取优化函数**：使用 `strategy_flag` 从 `optimization_strategies` 字典中获取相应的优化策略类，并将其赋值给 `optimization_func`。如果传入的 `strategy_flag` 不在字典的键中，函数将抛出一个 `ValueError` 异常。  
  
  * **3. 处理现金权重**：如果 `cash_rate` 不为零，则函数会修改 `data_slice`，排除最后一列（与现金相关的数据），然后调用 `optimization_func` 计算除现金外的其他资产的权重。接着，根据 `cash_rate` 调整这些权重，并为现金分配一个固定的权重。  
  
  * **4. 返回权重**：无论是否考虑现金权重，函数最终都会返回一个包含资产权重的列表。这些权重将用于指导资金在不同资产之间的分配。       




```python
# 定义获取资产权重的函数
def get_assets_weight(data_slice, strategy_flag, cash_rate = 0.1):
    
    optimization_strategies = { 
    'simple_std_reverse':optimal_strategy.SimpleStdReverse,
    'risk_parity': optimal_strategy.RiskParityModel,  
    # 'mean_variance': MeanVarianceOptimization, 
    'equal_weight': optimal_strategy.EqualWeighting,  
    } 
    optimization_func = optimization_strategies.get(strategy_flag)
    if optimization_func is None:  
        raise ValueError(f"Invalid strategy flag: {strategy_flag}. Please use one of the following: {list(optimization_strategies.keys())}")
    
    if cash_rate != 0:
        data_slice = data_slice.iloc[:,:-1]
        optimal_weights = optimization_func(data_slice)
        optimal_weights = [weight * (1- cash_rate) for weight in optimal_weights]
        optimal_weights = optimal_weights + [cash_rate]
        
        return optimal_weights
    else:
        optimal_weights = optimization_func(data_slice)
        
        return optimal_weights
```



主函数中进行策略的模拟交易回测，输入参数是回测周期，回测方法，无风险利率，正权重和初始资金。接受以下几个参数：

- **`rebalance_period`**：一个整数，表示投资组合调仓的频率（以天为单位）。
- **`strategy_flag`**：一个字符串标识符，用于指定正在实施的具体投资策略，可能作为`get_assets_weight`函数的一个参数。
- **`risk_free_rate`**：无风险利率，用于计算某些绩效指标。
- **`non_neg`**（可选）：一个布尔标志，指示策略是否应强制资产权重为非负值（默认为`True`）。
- **`initial_investment`**：投资组合的起始资金（默认为`10000000`）。

**实现步骤**  
  
  * **1. 初始化**  
    - 将初始投资组合价值设置为`initial_investment`。  
    - 初始化两个空字典`current_weights`和`current_holdings`，分别用于存储每次重新平衡时的资产权重和持有量。  
    - 创建一个名为`data_frames`的字典，该字典包含三个`pandas` `DataFrame`对象：`weights`、`holdings`和`portfolio_value`，用于在模拟过程中记录历史数据。  
  
  * **2. 模拟循环**  
    - 遍历时间序列`DataFrame` `drr_dt`的索引，该索引假定包含了多种资产的日收益率。  
  
      * **2.1 调仓**  
        - 检查当前交易日是否为调仓日（即`i % rebalance_period == 0`）。  
        - 如果是调仓日，则检索过去调仓周期个交易日的数据（如果不足调仓天数，则取所有可用数据）。  
        - 调用`get_assets_weight`函数，使用选定的数据切片和`strategy_flag`计算投资组合的新资产权重。  
        - 根据计算出的权重和`initial_investment`更新`current_weights`和`current_holdings`。  
  
      * **2.2 投资组合价值计算**  
        - 通过将每个资产的持有量与其当日收益率的乘积求和，计算投资组合的更新价值。假设没有交易成本或其他费用。  
  
      * **2.3 数据记录**  
        - 将当前日期、资产权重、投资组合价值和单位净值（投资组合价值除以`initial_investment`）分别追加到`data_frames`中的相应`DataFrame`。  
        - 对于持有的每项资产，将当前日期、资产名和持有量追加到`holdings DataFrame`。  
  
  * **3. 绩效评估**  
    - 模拟结束后，使用`evaluate_unv`模块中的`DrawPortfolioLines`类绘制投资组合的单位净值（NUV）线图和回撤柱状图。图表标题中包含指定的`strategy_flag`和`rebalance_period`。  
    - 实例化同一模块中的`NumericalIndicators`类的对象，传入单位净值序列和`risk_free_rate`。  
    - 打印该对象计算出的数值指标，包括夏普比率、最大回撤和年化收益率等。


```python
def main(rebalance_period, strategy_flag, risk_free_rate, non_neg = True, initial_investment = 10000000):
        
    # 初始化策略状态
    portfolio_value = initial_investment
    current_weights = {}
    current_holdings = {}
    
    # 初始化数据框列表
    data_frames = {
        'weights': pd.DataFrame(),
        'holdings': pd.DataFrame(),
        'portfolio_value': pd.DataFrame(),
    }
    
       
    # 模拟策略执行
    for i, date in enumerate(drr_dt.index):
        # 如果当前交易日是调仓日期，则重新分配资产权重
        if (i + 1) % rebalance_period == 0:
          
            if i >= rebalance_period:
                data_slice = drr_dt.iloc[i - rebalance_period:i]
            else:
                data_slice = drr_dt.iloc[:i]
            
            # 计算权重 ,即实施策略
            new_weights = get_assets_weight(data_slice,strategy_flag)
    
            
            # 更新策略状态
            current_weights = dict(zip(data_slice.columns, new_weights))
            current_holdings = {asset: initial_investment * weight for asset, weight in current_weights.items()}
        
        # 计算投资组合的价值变化（这里我们忽略交易成本和其他费用）
        portfolio_value += sum(current_holdings[asset] * drr_dt.at[date, asset] for asset in current_holdings)
        
        data_frames['weights'] = pd.concat([data_frames['weights'],
                pd.DataFrame({**{'Date': [date]}, **current_weights})],
                ignore_index=True            
            )
        
        data_frames['portfolio_value'] = pd.concat([data_frames['portfolio_value'],
                pd.DataFrame({'Date': [date], 'Value': portfolio_value , 'Unit Net Value':portfolio_value / initial_investment})],
                ignore_index=True
            )
        
        for asset in current_holdings:
            data_frames['holdings'] = pd.concat([data_frames['holdings'],
                    pd.DataFrame({'Date': [date], 'Asset': asset, 'Holding': current_holdings[asset]})],
                    ignore_index=True
                )
           
    
    dr = evaluate_unv.DrawPortfolioLines(data_frames['portfolio_value'])
    dr.nuv_lines(draw_title=str(rebalance_period) + '天' + strategy_flag)
    dr.drawdown_bars(draw_title=str(rebalance_period) + '天' + strategy_flag)
    ni = evaluate_unv.NumericalIndicators(data_frames['portfolio_value']['Unit Net Value'], risk_free_rate = risk_free_rate)
    ni.print_numerical_indicators()
```

在20，60，120个交易日进行换仓回测，对应的自然月约是1，3，6个月，结果如下：


```python
for i in [20,60,120]:
    for strategy in ['simple_std_reverse','risk_parity','equal_weight']:
        print('调仓周期是：{}天'.format(i))
        print('策略是' + strategy)
        main(i,strategy,risk_free_rate= 0.02)
        print('*'*100)
```

```
## 调仓周期是：20天
## 策略是simple_std_reverse
## 年化收益率是4.39%
## 年化波动率是1.29%
## 最大回撤是3.11%
## 年化夏普比率是1.85
## ****************************************************************************************************
## 调仓周期是：20天
## 策略是risk_parity
## 年化收益率是4.12%
## 年化波动率是0.98%
## 最大回撤是3.16%
## 年化夏普比率是2.15
## ****************************************************************************************************
## 调仓周期是：20天
## 策略是equal_weight
## 年化收益率是5.16%
## 年化波动率是5.25%
## 最大回撤是8.01%
## 年化夏普比率是0.58
## ****************************************************************************************************
## 调仓周期是：60天
## 策略是simple_std_reverse
## 年化收益率是4.11%
## 年化波动率是1.35%
## 最大回撤是3.18%
## 年化夏普比率是1.56
## ****************************************************************************************************
## 调仓周期是：60天
## 策略是risk_parity
## 年化收益率是3.69%
## 年化波动率是0.94%
## 最大回撤是3.26%
## 年化夏普比率是1.79
## ****************************************************************************************************
## 调仓周期是：60天
## 策略是equal_weight
## 年化收益率是4.62%
## 年化波动率是5.4%
## 最大回撤是8.51%
## 年化夏普比率是0.46
## ****************************************************************************************************
## 调仓周期是：120天
## 策略是simple_std_reverse
## 年化收益率是4.06%
## 年化波动率是1.34%
## 最大回撤是3.24%
## 年化夏普比率是1.53
## ****************************************************************************************************
## 调仓周期是：120天
## 策略是risk_parity
## 年化收益率是3.84%
## 年化波动率是0.93%
## 最大回撤是3.29%
## 年化夏普比率是1.98
## ****************************************************************************************************
## 调仓周期是：120天
## 策略是equal_weight
## 年化收益率是4.47%
## 年化波动率是5.48%
## 最大回撤是8.74%
## 年化夏普比率是0.42
## ****************************************************************************************************
```

<img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-1.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-2.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-3.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-4.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-5.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-6.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-7.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-8.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-9.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-10.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-11.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-12.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-13.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-14.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-15.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-16.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-17.png" width="1728" /><img src="{{< blogdown/postref >}}index_files/figure-html/unnamed-chunk-5-18.png" width="1728" />

