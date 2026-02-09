# strategies/rsi_strategy.py
import pandas as pd
import numpy as np


class RSIStrategy:
    """RSI指标策略"""

    def __init__(self, period=14, overbought=70, oversold=30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def calculate_rsi(self, prices):
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self, data):
        """生成交易信号"""
        data['rsi'] = self.calculate_rsi(data['close'])

        # 初始化信号列
        data['signal'] = 0

        # RSI低于超卖线，买入信号
        data.loc[data['rsi'] < self.oversold, 'signal'] = 1

        # RSI高于超买线，卖出信号
        data.loc[data['rsi'] > self.overbought, 'signal'] = -1

        return data