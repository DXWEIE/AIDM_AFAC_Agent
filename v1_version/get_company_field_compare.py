from bs4 import BeautifulSoup
import re
import pandas as pd
import requests


def get_hk_company_field_compare(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    
    url = f"https://basic.10jqka.com.cn/HK{symbol}/field.html"
    # 获取页面内容
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=header)
    soup_field_hk = BeautifulSoup(response.content, 'html.parser')
    data_list = []

    # 最上面的，HK的是价值表现
    # <p class="threecate f14 fl tip">
    title_and_filed_0 = soup_field_hk.find('p', class_='threecate f14 fl tip').get_text(strip=True, separator=' ') # 标题和行业信息
    #<div class="field_date1" id="dateSelect">
    field_date_div = soup_field_hk.find('div', class_='field_date1')
    # 获取里面的<a>的tag="0"和tag="1"的文本
    issue_0 = field_date_div.find('a', tag='0').get_text(strip=True)  # 最新
    issue_1 = field_date_div.find('a', tag='1').get_text(strip=True)  # 上一期

    #<p class="clearfix p10_0">
    field_data_p = soup_field_hk.find_all('p', class_='clearfix p10_0')
    # 可能是一个列表，"注："里面的内容，可能是换算为港币
    notation_list = []
    for p in field_data_p:
        # 获取每个<p>的文本
        notation = p.get_text(strip=True, separator=' ')
        notation_list.append(notation)
    
    table_0_0 = soup_field_hk.find('table', class_='m_table m_hl', id='hy3_table_1')
    
    # 获取表头
    table_0_header = table_0_0.find('thead').find_all('th')
    # 获取表头文本
    table_0_header_text = [th.get_text(strip=True) for th in table_0_header]
    # 获取表格数据
    table_0_rows = table_0_0.find('tbody').find_all('tr')
    # 获取每一行的数据
    table_0_data = []
    for row in table_0_rows:
        cols = row.find_all('td')
        cols_text = [col.get_text(strip=True) for col in cols]
        table_0_data.append(cols_text)
    
    table_0_df = pd.DataFrame(table_0_data, columns=table_0_header_text)

    data  = dict()
    data['issue'] = issue_0
    data['title'] = title_and_filed_0
    data['ps'] = notation_list[0] if len(notation_list) > 0 else ''
    data['table'] = table_0_df
    data_list.append(data)

    table_0_1 = soup_field_hk.find('table', class_='m_table m_hl', id='hy3_table_2')
    # 获取表头
    table_1_header = table_0_1.find('thead').find_all('th')
    # 获取表头文本
    table_1_header_text = [th.get_text(strip=True) for th in table_1_header]
    # 获取表格数据
    table_1_rows = table_0_1.find('tbody').find_all('tr')
    # 获取每一行的数据
    table_1_data = []
    for row in table_1_rows:
        cols = row.find_all('td')
        cols_text = [col.get_text(strip=True) for col in cols]
        table_1_data.append(cols_text)

    # 变成dataframe格式
    table_1_df = pd.DataFrame(table_1_data, columns=table_1_header_text)
    data = dict()
    data['issue'] = issue_1
    data['title'] = title_and_filed_0
    data['ps'] = notation_list[0] if len(notation_list) > 1 else ''
    data['table'] = table_1_df
    data_list.append(data)

    title_and_filed_1 = soup_field_hk.find('p', class_='threecate fl f14 tip').get_text(strip=True, separator=' ') # 标题和行业信息
    #<div class="field_date1" id="dateSelect">
    field_date_div = soup_field_hk.find('div', class_='field_date1')
    if field_date_div is not None:
        # 获取里面的<a>的tag="0"和tag="1"的文本
        issue_2 = field_date_div.find('a', tag='0').get_text(strip=True)  # 最新
        issue_3 = field_date_div.find('a', tag='1').get_text(strip=True)  # 上一期

        table_1_0 = soup_field_hk.find('table', class_='m_table m_hl', id='hy2_table_1')
        # 获取表头
        table_1_0_header = table_1_0.find('thead').find_all('th')
        # 获取表头文本
        table_1_0_header_text = [th.get_text(strip=True) for th in table_1_0_header]
        # 获取表格数据
        table_1_0_rows = table_1_0.find('tbody').find_all('tr')
        # 获取每一行的数据
        table_1_0_data = []
        for row in table_1_0_rows:
            cols = row.find_all('td')
            cols_text = [col.get_text(strip=True) for col in cols]
            table_1_0_data.append(cols_text)
        # 变成dataframe格式
        table_1_0_df = pd.DataFrame(table_1_0_data, columns=table_1_0_header_text)

        data = dict()
        data['issue'] = issue_2
        data['title'] = title_and_filed_1
        data['ps'] = notation_list[1] if len(notation_list) > 1 else ''
        data['table'] = table_1_0_df
        data_list.append(data)

        tabel_1_1 = soup_field_hk.find('table', class_='m_table m_hl', id='hy2_table_2')
        # 获取表头
        table_1_1_header = tabel_1_1.find('thead').find_all('th')
        # 获取表头文本
        table_1_1_header_text = [th.get_text(strip=True) for th in table_1_1_header]
        # 获取表格数据
        table_1_1_rows = tabel_1_1.find('tbody').find_all('tr')
        # 获取每一行的数据
        table_1_1_data = []
        for row in table_1_1_rows:
            cols = row.find_all('td')
            cols_text = [col.get_text(strip=True) for col in cols]
            table_1_1_data.append(cols_text)

        # 变成dataframe格式
        table_1_1_df = pd.DataFrame(table_1_1_data, columns=table_1_1_header_text)
        data = dict()
        data['issue'] = issue_3
        data['title'] = title_and_filed_1
        data['ps'] = notation_list[1] if len(notation_list) > 1 else ''
        data['table'] = table_1_1_df
        data_list.append(data)
    return data_list


def get_cn_company_field_compare(symbol):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    url = f"https://basic.10jqka.com.cn/{symbol}/field.html"
    # 获取页面内容
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=header)
    soup_field_cn = BeautifulSoup(response.content, 'html.parser')
    data_list_cn = []

    # 获取标题和行业信息
    # <p class="threecate fl">三级行业分类：<span class="tip f14">计算机 -- 计算机设备 -- 其他计算机设备 （共<strong>57</strong>家）</span></p>
    title_and_filed_0_cn = soup_field_cn.find('p', class_='threecate fl').get_text(strip=True, separator=' ')  # 标题和行业信息
    # 获取日期选择
    field_date_div_cn = soup_field_cn.find('div', class_='field_date1')
    # 获取里面的<a>的tag="0"和tag="1"的文本
    issue_0_cn = field_date_div_cn.find('a', tag='0').get_text(strip=True)  # 最新
    issue_1_cn = field_date_div_cn.find('a', tag='1').get_text(strip=True)  # 上一期

    # 获取注释信息
    field_data_p_cn = soup_field_cn.find_all('p', class_='clearfix p10_0')
    notation_list_cn = []
    for p in field_data_p_cn:
        # 获取每个<p>的文本
        notation = p.get_text(strip=True, separator=' ')
        notation_list_cn.append(notation)

    # 第一个表 <table class="m_table m_hl" id="hy3_table_1">
    # 获取表格数据
    table_0_0 = soup_field_cn.find('table', id='hy3_table_1')
    # 获取表格表头
    table_0_0_title = table_0_0.find('thead').get_text(strip=True, separator=' ')
    # 获取表格数据
    table_0_0_data = []
    for tr in table_0_0.find_all('tr')[1:]:  # 跳过表头
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        table_0_0_data.append(row_data)
    # dataframe
    import pandas as pd
    df_table_0_0 = pd.DataFrame(table_0_0_data, columns=table_0_0_title.split())
    data = dict()
    data['issue'] = issue_0_cn
    data['title'] = title_and_filed_0_cn
    data['ps'] = notation_list_cn[0] if len(notation_list_cn) > 0 else ''
    data['table'] = df_table_0_0
    data_list_cn.append(data)

    # 第二个表 <table class="m_table m_hl" id="hy3_table_2">
    table_0_1 = soup_field_cn.find('table', id='hy3_table_2')
    # 获取表格表头
    table_0_1_title = table_0_1.find('thead').get_text(strip=True, separator=' ')
    # 获取表格数据
    table_0_1_data = []
    for tr in table_0_1.find_all('tr')[1:]:  # 跳过表头
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        table_0_1_data.append(row_data)
    # dataframe
    df_table_0_1 = pd.DataFrame(table_0_1_data, columns=table_0_1_title.split())
    data = dict()
    data['issue'] = issue_1_cn
    data['title'] = title_and_filed_0_cn
    data['ps'] = notation_list_cn[0] if len(notation_list_cn) > 0 else ''
    data['table'] = df_table_0_1
    data_list_cn.append(data)


    # 获取行业标题 <p class="threecate">二级行业分类：<span class="tip f14">计算机 -- 计算机设备 （共<strong>80</strong>家）</span></p>
    title_and_filed_1_cn = soup_field_cn.find('p', class_='threecate').get_text(strip=True, separator=' ')  # 标题和行业信息
    # 获取期数
    field_date_div_1_cn = soup_field_cn.find('div', class_='field_date2')
    if field_date_div_1_cn is not None:
        # 获取里面的<a>的tag="0"和tag="1"的文本
        issue_2_cn = field_date_div_1_cn.find('a', tag='0').get_text(strip=True)  # 最新
        issue_3_cn = field_date_div_1_cn.find('a', tag='1').get_text(strip=True)  # 上一期

        # 表格1  hy2_table_1
        table_1_0 = soup_field_cn.find('table', id='hy2_table_1')
        # 获取表格表头
        table_1_0_title = table_1_0.find('thead').get_text(strip=True, separator=' ')
        # 获取表格数据
        table_1_0_data = []
        for tr in table_1_0.find_all('tr')[1:]:  # 跳过表头
            row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
            table_1_0_data.append(row_data)
        # dataframe
        df_table_1_0 = pd.DataFrame(table_1_0_data, columns=table_1_0_title.split())
        data = dict()
        data['issue'] = issue_2_cn
        data['title'] = title_and_filed_1_cn
        data['ps'] = notation_list_cn[1] if len(notation_list_cn) > 1 else ''
        data['table'] = df_table_1_0
        data_list_cn.append(data)

        # 表格2 hy2_table_2
        table_1_1 = soup_field_cn.find('table', id='hy2_table_2')
        # 获取表格表头
        table_1_1_title = table_1_1.find('thead').get_text(strip=True, separator=' ')
        # 获取表格数据
        table_1_1_data = []
        for tr in table_1_1.find_all('tr')[1:]:  # 跳过表头
            row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
            table_1_1_data.append(row_data)
        # dataframe
        df_table_1_1 = pd.DataFrame(table_1_1_data, columns=table_1_1_title.split())
        data = dict()
        data['issue'] = issue_3_cn
        data['title'] = title_and_filed_1_cn
        data['ps'] = notation_list_cn[1] if len(notation_list_cn) > 1 else ''
        data['table'] = df_table_1_1
        data_list_cn.append(data)
    return data_list_cn

