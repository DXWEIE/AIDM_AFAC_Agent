from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

# 获取财务状况-主要指标
def download_hk_financial_data(symbol,type='main'):
    """
    # 通过同花顺获取香港公司的财务盈利状况年度详细数据，下载xls
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    symbol = '0' + symbol
    main_url = ('http://basic.10jqka.com.cn/api/hk/export.php?export=keyindex&type=report&code='+symbol) # 主要指标
    debt_url = ('http://basic.10jqka.com.cn/api/hk/export.php?export=debt&type=report&code='+symbol) # 资产负债表
    benift_url = ('http://basic.10jqka.com.cn/api/hk/export.php?export=benefit&type=report&code='+symbol) # 利润表
    cash_url = ('http://basic.10jqka.com.cn/api/hk/export.php?export=cash&type=report&code='+symbol) # 现金流量表
    # 在点击下载按钮时，浏览器会请求这个URL
    # 现在要把这个xls文件下载下来
    urls = {
        'main': main_url,
        'debt': debt_url,
        'benift': benift_url,
        'cash': cash_url
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(urls[type], headers=headers)
        response.raise_for_status()  # 确保请求成功
        filename = f"{symbol}_{type}_financial_data.xls"
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    except Exception as e:
        print(f"Error downloading financial data: {e}")
        return None


def download_cn_financial_data(symbol,type='main'):
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    main_url = f"http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=report&code={symbol}"
    debt_url = f"http://basic.10jqka.com.cn/api/stock/export.php?export=debt&type=report&code={symbol}"
    benift_url = f"http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=report&code={symbol}"
    cash_url = f"http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=report&code={symbol}"
    urls = {
        'main': main_url,
        'debt': debt_url,
        'benift': benift_url,
        'cash': cash_url
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(urls[type], headers=headers)
        response.raise_for_status()  # 确保请求成功
        filename = f"{symbol}_financial_data.xls"
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    except Exception as e:
        print(f"Error downloading financial data: {e}")
        return None
