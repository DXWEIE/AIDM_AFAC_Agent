from bs4 import BeautifulSoup
import re
import pandas as pd
import requests


def get_cn_control(symbol):
    # 控盘变化
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    url = f'https://basic.10jqka.com.cn/{symbol}/'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=header)

    soup_news_cn = BeautifulSoup(response.content, 'html.parser')

    # 主力控盘 <div class="m_box clearfix" id="main" stat="index_main">
    # <table class="m_table m_hl">
    main_control_table = soup_news_cn.find('div', id='main').find('table', class_='m_table m_hl')
    # 获取表格数据，没有表头，都是数据, thead里面也是数据
    main_control_data = []
    # 获取thead里面的数据
    thead_data = main_control_table.find('thead').find_all('tr')#.get_text(strip=True, separator=' ')
    for tr in thead_data:
        row_data = [td.get_text(strip=True) for td in tr.find_all('th')]
    main_control_data.append(row_data)  # 将表头作为第一行数据
    # 获取tbody里面的数据

    # find all的tr或者tl
    tbody_data = main_control_table.find('tbody').find_all(['tr', 'tl'])  # tbody里面的tr和td
    for tr in tbody_data:
        row_data = [td.get_text(strip=True) for td in tr.find_all(['th', 'td'])]
        main_control_data.append(row_data)
    # 最后一行是提示，单独拿出来，其余每行的第0个是表头，其他的是数据
    # 将数据转换为DataFrame
    import pandas as pd
    # 第一列是表头，最后一行是提示
    df_main_control = pd.DataFrame(main_control_data[:-1])
    # 转置，因为第一列是表头
    df_main_control = df_main_control.T
    # 设置第一行作为列名
    df_main_control.columns = df_main_control.iloc[0]
    df_main_control = df_main_control[1:]  # 去掉第一行
    # 重置索引
    df_main_control.reset_index(drop=True, inplace=True)
    return df_main_control



