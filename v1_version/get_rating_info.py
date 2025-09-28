from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import akshare as ak

def get_hk_rating_info(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    url = f'https://basic.10jqka.com.cn/HK{symbol}/rating.html'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=header)
    soup_rating_hk = BeautifulSoup(response.content, 'html.parser')
    #<table class="m_table m_hl mt15">
    rating_info = soup_rating_hk.find('table', class_='m_table m_hl mt15')
    # 获取表格数据
    rating_data = []
    # 获取表格表头
    rating_title = rating_info.find('thead')
    rating_title_data = [th.get_text(strip=True) for th in rating_title.find_all('th')]
    rating_data.append(rating_title_data)  # 将表头作为第一行数据
    for tr in rating_info.find_all('tr')[1:]:  # 跳过表头
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        rating_data.append(row_data)
    # 将数据转换为DataFrame
    import pandas as pd
    df_rating_hk = pd.DataFrame(rating_data, columns=rating_title_data)
    # 删除第一行
    df_rating_hk = df_rating_hk[1:]  # 去掉第一行
    # 重置索引
    df_rating_hk = df_rating_hk.reset_index(drop=True)
    return df_rating_hk

    # stock_hk_profit_forecast_et_df = ak.stock_hk_profit_forecast_et(symbol='0'+symbol,indicator="盈利预测概览")
    # return stock_hk_profit_forecast_et_df


def get_cn_rating_info(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    stock_profit_forecast_ths_df = ak.stock_profit_forecast_ths(symbol=symbol, indicator="业绩预测详表-详细指标预测")
    return stock_profit_forecast_ths_df
