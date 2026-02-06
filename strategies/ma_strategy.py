# strategies/ma_strategy.py
import pandas as pd
import numpy as np


class MovingAverageStrategy:
    """简单移动平均线策略"""

    def __init__(self, short_window=10, long_window=30):
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, data):
        """计算交易信号"""
        # 计算移动平均线
        data['short_ma'] = data['close'].rolling(window=self.short_window).mean()
        data['long_ma'] = data['close'].rolling(window=self.long_window).mean()

        # 生成信号
        data['signal'] = 0
        data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1  # 买入
        data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1  # 卖出

        return data

    def backtest(self, data, initial_capital=100000):
        """简单回测"""
        signals = self.calculate_signals(data.copy())
        positions = signals['signal'].diff()  # 仓位变化

        # 计算收益
        returns = data['close'].pct_change()
        strategy_returns = positions.shift(1) * returns

        # 计算累计收益
        cumulative_returns = (1 + strategy_returns).cumprod()

        return {
            'signals': signals,
            'returns': strategy_returns,
            'cumulative_returns': cumulative_returns
        }


if __name__ == "__main__":
    # 测试策略
    print("移动平均策略加载成功！")