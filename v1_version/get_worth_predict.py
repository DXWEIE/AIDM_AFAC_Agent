from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import akshare as ak

def get_cn_worth_predict(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    url = f'https://basic.10jqka.com.cn/{symbol}/worth.html'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=header)
    soup_worth_cn = BeautifulSoup(response.content, 'html.parser')
    # 查找目标表格
    worth_predict = soup_worth_cn.find('table', class_='m_table m_hl ggintro ggintro_1 organData')

    # 初始化数据存储列表
    worth_predict_data = []

    # 表格可能存在或不存在 thead，所以先判断
    thead = worth_predict.find('thead')
    if thead:
        # 提取表头
        worth_predict_title_data = [th.get_text(strip=True) for th in thead.find_all('th')]
        worth_predict_data.append(worth_predict_title_data)

    # 提取表格主体数据
    tbody = worth_predict.find('tbody') or worth_predict  # 如果没有 tbody，则直接读取 table 下的 tr

    predict_flag = False
    for tr in tbody.find_all('tr'):
        row_data = []
        
        # 获取所有单元格（包括 th 和 td）
        cells = tr.find_all(['th', 'td'])
        for cell in cells:
            if cell.name == 'th' and cell.get('class')[0] == 'tl':
                # 第一列通常是 th，直接获取文本
                row_data.append(cell.get_text(strip=True))
                predict_flag = False
            else:
                # 处理 td 数据
                pr_div = cell.find('div')
                if pr_div:
                    if pr_div.get('class')[0] == 'pr':
                        # 如果有 class='pr'，则获取里面的 span 文本
                        span = pr_div.find('span')
                        text = span.get_text(strip=True) if span else ''
                        predict_flag = True
                    else:
                        continue
                else:
                    if predict_flag==False:
                        text = cell.get_text(strip=True)
                    else:
                        continue
                row_data.append(text)
        if row_data:  # 防止空行
            worth_predict_data.append(row_data)
        #predict_flag = False  # 重置标志位

    # dataframe
    import pandas as pd
    df_worth_predict = pd.DataFrame(worth_predict_data)
    # 需要转置，因为每行第一列是表头
    df_worth_predict = df_worth_predict.T
    # 设置第一行作为列名
    df_worth_predict.columns = df_worth_predict.iloc[0]
    df_worth_predict = df_worth_predict[1:]  # 去掉第一行
    # 重置索引
    df_worth_predict.reset_index(drop=True, inplace=True)
    return df_worth_predict

def get_hk_worth_predict(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    
    stock_hk_profit_forecast_et_df = ak.stock_hk_profit_forecast_et(symbol="0"+symbol, indicator="盈利预测概览")
    return stock_hk_profit_forecast_et_df