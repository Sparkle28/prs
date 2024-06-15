import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'SimSun'

class NumericalIndicators:
    
    def __init__(self, net_asset_values, days_in_a_year=252, risk_free_rate=0.1):  
        # 去掉序列最前面的连续1  
        cumsum_equals_one = net_asset_values.eq(1).cumsum()  
        first_non_one_idx = (cumsum_equals_one != (cumsum_equals_one.index + 1)).idxmax() - 1  
          
        if first_non_one_idx >= 0:  # 确保索引是有效的  
            self.net_asset_values = net_asset_values.iloc[first_non_one_idx:].reset_index(drop = True)  
        else:  
            self.net_asset_values = net_asset_values  
          
        self.days_in_a_year = days_in_a_year  
        self.risk_free_rate = risk_free_rate
        
    def calculate_max_drawdown(self):
        peak = self.net_asset_values[0]  
        max_drawdown = 0  
        for value in self.net_asset_values[1:]:
            if value > peak:
                peak = value
            else:
                drawdown = (peak - value) / peak
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
        return max_drawdown
    
    def calculate_annual_return_rate(self):
        daily_return_mean = np.mean(self.net_asset_values.pct_change().dropna())
        annualized_return = (1 + daily_return_mean) ** self.days_in_a_year - 1
        return annualized_return 
    
    
    def calculate_annualized_volatility(self):
        daily_returns = self.net_asset_values.pct_change()
        avt = daily_returns.std() * np.sqrt(self.days_in_a_year)
        return avt

    def calculate_annualized_sharpe_ratio(self):
        trading_days_per_year = self.days_in_a_year
        
        daily_returns = self.net_asset_values.pct_change()  
        daily_returns = daily_returns.dropna()  
          
        annual_return = ((daily_returns + 1).prod() ** (trading_days_per_year / len(daily_returns))) - 1  

        daily_volatility = daily_returns.std()  
        annual_volatility = daily_volatility * np.sqrt(trading_days_per_year) 

        annual_sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility  
          
        return annual_sharpe_ratio  
        
    def print_numerical_indicators(self):
        md = self.calculate_max_drawdown()
        arr = self.calculate_annual_return_rate()
        avt = self.calculate_annualized_volatility()
        csr = self.calculate_annualized_sharpe_ratio()
        print('年化收益率是%s%%' % np.around(arr*100,2))
        print('年化波动率是%s%%' % np.around(avt*100,2))
        print('最大回撤是%s%%' % np.around(md*100,2))
        print('年化夏普比率是%s' % np.around(csr,2))

class DrawPortfolioLines:
    def __init__(self, net_asset_values):
        initial_ones = net_asset_values['Unit Net Value'].eq(1).cumsum()
        first_non_one_index = (initial_ones != (initial_ones.index + 1)).idxmax() - 1
        
        if first_non_one_index is not None:
            self.net_asset_values = net_asset_values.loc[first_non_one_index:]
        else:
            self.net_asset_values = net_asset_values
    
    def nuv_lines(self,draw_title):
        plt.figure(figsize=(18,6))  
        plt.plot(self.net_asset_values['Date'],self.net_asset_values['Unit Net Value'] , linestyle='-')  
        plt.title(draw_title)  
        plt.xlabel('日期')  
        plt.ylabel('单位净值') 
        
        plt.show()

    def drawdown_bars(self,draw_title):
        drawdown = self.net_asset_values['Unit Net Value'] / self.net_asset_values['Unit Net Value'].cummax() - 1  
      
        # 绘制回撤柱状图，y轴朝下  
        fig, ax = plt.subplots(figsize=(18, 6))  
        ax.bar(self.net_asset_values['Date'], -drawdown, color='red',align='center')  
        ax.invert_yaxis()  # 反转y轴，使y轴朝下  
        ax.set_ylabel('Drawdown')  
        ax.set_title(draw_title)  
        ax.grid(True)  
          
        plt.show()  
