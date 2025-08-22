from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

def get_capital_structure_util(url):
    try:
        # 获取股本结构
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response_eq = requests.get(url, headers=headers)
        soup_eq = BeautifulSoup(response_eq.content, 'html.parser')

        # div = <div class="m_box gqtz">下面有股本的表格
        equity_table = soup_eq.find('div', class_='m_box gqtz')
        # 把股本表格进行解析，包括表头，只有表头列，没有表头行
        # 这个表不规范，第一行的tr里面都是th的形式
        equity_rows = equity_table.find_all('tr')

        # 假设 equity_table 是你已经提取到的 div 包含的表格部分
        equity_rows = equity_table.find_all('tr')

        # 用于存储最终结果
        table_data = []

        # 第一行处理：提取“公告日期”和各个日期
        first_row = equity_rows[0]

        # 获取第一个 tr 的原始 HTML 字符串
        row_html = str(first_row)

        # 使用正则提取所有的日期（格式为 YYYY-MM-DD）
        dates = re.findall(r'>(\d{4}-\d{2}-\d{2})\n<', row_html)

        # 添加表头
        header = first_row.find('th').get_text(strip=True) if first_row.find('th') else '时间' + dates
        table_data.append(header)

        # 处理后续每一行（每个指标）
        for row in equity_rows[1:]:
            cells = row.find_all(['th', 'td'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            
            # 确保长度一致，补空
            while len(row_data) < len(dates) + 1:
                row_data.append('')
                
            table_data.append(row_data)

        # # 打印结果查看
        # for row in table_data:
        #     print(row)

        data_dict = {}
        for row in table_data:
            key = row[0]              # 指标名，如“总股本”
            values = row[1:]          # 对应值
            data_dict[key] = values
        df = pd.DataFrame(data_dict)
        return df
    except Exception as e:
        print(f"Error fetching capital structure data: {e}")
        return pd.DataFrame()  # 返回空的DataFrame以表示失败



def get_capital_structure_cn_ths(symbol):
    """
    # https://basic.10jqka.com.cn/000066/equity.html
    获取中国大陆上市公司的基本信息，来自同花顺
    :param symbol: 6位股票代码，不带交易所代码
    :return: 公司基本信息dataframe，公司名称、所属行业、主营业务、公司简介，没有的为空
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 6:
        symbol = symbol[-6:]
    url = f"https://basic.10jqka.com.cn/{symbol}/equity.html"
    company_info = get_capital_structure_util(url)
    
    return company_info


def get_capital_structure_hk_ths(symbol):
    """
    # https://basic.10jqka.com.cn/HK0020/equity.html
    # 获取香港上市公司的基本信息，来自同花顺
    # symbol需要是后4位，前面加上'HK'前缀
    """
    # 去掉symbol里面的字母，判断symbol位数，取最后4位
    # symbol的字母可能大写可能小写
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    url = f"https://basic.10jqka.com.cn/HK{symbol}/equity.html"
    company_info = get_capital_structure_util(url)
    
    return company_info