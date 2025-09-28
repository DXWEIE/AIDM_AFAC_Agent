
import akshare as ak
# 用于从url信息获取的库
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_company_info_util_ths(url):
    """
    通过同花顺获取目标公司基本信息
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        main_business = soup.find('strong', class_='hltip fl', text=lambda x: '业务' in x if x else False)
        if main_business:
            main_business_info = main_business.find_next('span').text
        else:
            main_business_info="NULL"
        
        main_field = soup.find('strong', class_='hltip fl', text=lambda x: '行业' in x if x else False)
        if main_field:
            main_field_info = main_field.find_next('span').text
        else:
            main_field_info="NULL"

        # 公司简介 company_intro
        company_intro = ''
        all_tr = soup.find_all('tr')
        for tr in all_tr:
            # 如果tr里面有strong才看，否则跳过
            strong = tr.find('strong')
            if strong:
                # 如果strong里面有公司简介才看，否则跳过
                if '公司简介' in strong.text:
                    p = tr.find('p')
                    company_intro = p.text.strip() if p else ''
            else:
                continue
        if company_intro:
            company_intro_info = company_intro if company_intro else "NULL"
        else:
            company_intro_info = "NULL"
        
        # 公司名称 company_name
        company_name = soup.find('strong', class_='hltip fl', text=lambda x: '公司名称' in x if x else False)
        if company_name:
            company_name_info = company_name.find_next('span').text
        else:
            company_name_info = "NULL"
        
        # 公司英文名称 company_en_name
        company_en_name = soup.find('strong', class_='hltip fl', text=lambda x: '英文名称' in x if x else False)
        if company_en_name:
            company_en_name_info = company_en_name.find_next('span').text
        else:
            company_en_name_info = "NULL"
        
        # 结果返回
        company_info = {
            '公司名称': company_name_info,
            '英文名称': company_en_name_info,
            '主营业务': main_business_info,
            '所属行业': main_field_info,
            '公司简介': company_intro_info
        }
        return company_info
    except Exception as e:
        print(f"Error fetching company info from {url}: {e}")
        return {
            '公司名称': "NULL",
            '英文名称': "NULL",
            '主营业务': "NULL",
            '所属行业': "NULL",
            '公司简介': "NULL"
        }
    

def get_company_profile_ths_cn(symbol):
    """
    # https://basic.10jqka.com.cn/000066/company.html
    获取中国大陆上市公司的基本信息，来自同花顺
    :param symbol: 6位股票代码，不带交易所代码
    :return: 公司基本信息dataframe，公司名称、所属行业、主营业务、公司简介，没有的为空
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    url = f"https://basic.10jqka.com.cn/{symbol}/company.html"
    company_info = get_company_info_util_ths(url)
    
    return company_info


def get_company_profile_ths_hk(symbol):
    """
    # https://basic.10jqka.com.cn/HK0020/company.html
    # 获取香港上市公司的基本信息，来自同花顺
    # symbol需要是后4位，前面加上'HK'前缀
    """
    # 去掉symbol里面的字母，判断symbol位数，取最后4位
    # symbol的字母可能大写可能小写
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    url = f"https://basic.10jqka.com.cn/HK{symbol}/company.html"
    company_info = get_company_info_util_ths(url)
    
    return company_info



def get_cn_company_profile_ak(symbol):
    """
    获取中国上市公司的基本信息
    :param symbol: 6位股票代码，不带交易所代码
    :return: 公司基本信息dataframe
    # ['股票代码', '主营业务', '产品类型', '产品名称', '经营范围']
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    company_profile = ak.stock_zyjs_ths(symbol=symbol)
    return company_profile

def get_hk_company_profile_ak(symbol):
    """
    获取香港上市公司的基本信息
    :param symbol: 5位股票代码
    :return: 公司基本信息dataframe
    #['公司名称', '英文名称', '注册地', '注册地址', '公司成立日期', '所属行业', '董事长', '公司秘书', '员工人数',
       '办公地址', '公司网址', 'E-MAIL', '年结日', '联系电话', '核数师', '传真', '公司介绍']
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    company_profile = ak.stock_hk_company_profile_em(symbol='0'+symbol)
    return company_profile
