from bs4 import BeautifulSoup
import re
import pandas as pd
import requests



def get_company_finance_summary_hk(symbol):
    """
    港股是返回2024年的摘要
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    url = f"https://basic.10jqka.com.cn/HK{symbol}/business.html"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response_stock_summary = requests.get(url, headers=headers)
        soup_stock_summary = BeautifulSoup(response_stock_summary.content, 'html.parser')
        stock_summary_info = soup_stock_summary.find('p', class_='f14').get_text(strip=True, separator=' ')[:-5]
        stock_summary_info_remain = soup_stock_summary.find('span', class_='text-remain').get_text(strip=True, separator=' ')
        stock_summary_info = stock_summary_info + ' ' + stock_summary_info_remain
        date = soup_stock_summary.find('a', class_='businessTab').get_text(strip=True) # 日期
        return {
            date: stock_summary_info
        }
    except Exception as e:
        print(f"Error fetching company finance summary: {e}")
        return {}
    

def get_company_finance_summary_cn(symbol):
    """
    cn股票通常返回近3次的摘要
    """
    try:
        symbol = symbol.upper()
        symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
        if len(symbol) > 6:
            symbol = symbol[-6:]
        url = f"https://basic.10jqka.com.cn/{symbol}/operate.html"
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response_stock_summary = requests.get(url, headers=headers)
        soup_stock_summary = BeautifulSoup(response_stock_summary.content, 'html.parser')
        stock_summary_divs = soup_stock_summary.select('div[class="m_tab_content m_tab_content2"]')#.find_all('div', class_='m_tab_content m_tab_content2') 
        stock_summary_data = []
        for div in stock_summary_divs:
            # 获取标题
            content = div.find('p', class_='f14 none clearfix pr').get_text(strip=True, separator=' ')
            
            # 添加到列表
            stock_summary_data.append(
                content
        )
        date_div = soup_stock_summary.select('div[class="m_tab"]')#.find_all('a',class_='operateTab')
        data_a_list = date_div[0].find_all('a', class_='operateTab')
        date_list = []
        for a in data_a_list:
            # 获取日期
            date = a.get_text(strip=True)
            
            # 添加到列表
            date_list.append(
                date
            )
        result_dict = {}
        for i, date in enumerate(date_list):
            if i < len(stock_summary_data):
                result_dict[date] = stock_summary_data[i]
            else:
                result_dict[date] = ""
        return result_dict
    except Exception as e:
        print(f"Error fetching company finance summary: {e}")
        return {}