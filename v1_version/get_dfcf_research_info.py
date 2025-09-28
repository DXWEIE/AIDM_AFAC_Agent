import requests
from bs4 import BeautifulSoup
# 原始的获取研报的api，慢一点sleep多一点
import requests
import json
import time
from datetime import datetime, timedelta
from time import sleep
import pandas as pd

src_mapping = """<div id="hymore" class="select-box" style="display: none;"><ul><li><b>B</b><a target="_self" data-bkval="546">玻璃玻纤</a></li><li><a target="_self" data-bkval="474">保险</a></li><li><a target="_self" data-bkval="1036">半导体</a></li><li><a target="_self" data-bkval="733">包装材料</a></li><li><b>C</b><a target="_self" data-bkval="1017">采掘行业</a></li><li><a target="_self" data-bkval="729">船舶制造</a></li><li><b>D</b><a target="_self" data-bkval="459">电子元件</a></li><li><a target="_self" data-bkval="457">电网设备</a></li><li><a target="_self" data-bkval="428">电力行业</a></li><li><a target="_self" data-bkval="1039">电子化学品</a></li><li><a target="_self" data-bkval="1034">电源设备</a></li><li><a target="_self" data-bkval="1033">电池</a></li><li><a target="_self" data-bkval="1030">电机</a></li><li><a target="_self" data-bkval="738">多元金融</a></li><li><b>F</b><a target="_self" data-bkval="451">房地产开发</a></li><li><a target="_self" data-bkval="436">纺织服装</a></li><li><a target="_self" data-bkval="1045">房地产服务</a></li><li><a target="_self" data-bkval="1032">风电设备</a></li><li><a target="_self" data-bkval="1020">非金属材料</a></li><li><b>G</b><a target="_self" data-bkval="479">钢铁行业</a></li><li><a target="_self" data-bkval="427">公用事业</a></li><li><a target="_self" data-bkval="425">工程建设</a></li><li><a target="_self" data-bkval="1038">光学光电子</a></li><li><a target="_self" data-bkval="1031">光伏设备</a></li><li><a target="_self" data-bkval="739">工程机械</a></li><li><a target="_self" data-bkval="732">贵金属</a></li><li><a target="_self" data-bkval="726">工程咨询服务</a></li><li><b>H</b><a target="_self" data-bkval="538">化学制品</a></li><li><a target="_self" data-bkval="480">航天航空</a></li><li><a target="_self" data-bkval="471">化纤行业</a></li><li><a target="_self" data-bkval="465">化学制药</a></li><li><a target="_self" data-bkval="450">航运港口</a></li><li><a target="_self" data-bkval="447">互联网服务</a></li><li><a target="_self" data-bkval="420">航空机场</a></li><li><a target="_self" data-bkval="1019">化学原料</a></li><li><a target="_self" data-bkval="731">化肥行业</a></li><li><a target="_self" data-bkval="728">环保行业</a></li><li><b>J</b><a target="_self" data-bkval="456">家电行业</a></li><li><a target="_self" data-bkval="440">家用轻工</a></li><li><a target="_self" data-bkval="429">交运设备</a></li><li><a target="_self" data-bkval="740">教育</a></li><li><a target="_self" data-bkval="735">计算机设备</a></li><li><b>L</b><a target="_self" data-bkval="485">旅游酒店</a></li><li><b>M</b><a target="_self" data-bkval="484">贸易行业</a></li><li><a target="_self" data-bkval="437">煤炭行业</a></li><li><a target="_self" data-bkval="1035">美容护理</a></li><li><b>N</b><a target="_self" data-bkval="477">酿酒行业</a></li><li><a target="_self" data-bkval="433">农牧饲渔</a></li><li><a target="_self" data-bkval="1015">能源金属</a></li><li><a target="_self" data-bkval="730">农药兽药</a></li><li><b>Q</b><a target="_self" data-bkval="481">汽车零部件</a></li><li><a target="_self" data-bkval="1029">汽车整车</a></li><li><a target="_self" data-bkval="1016">汽车服务</a></li><li><b>R</b><a target="_self" data-bkval="1028">燃气</a></li><li><a target="_self" data-bkval="737">软件开发</a></li><li><b>S</b><a target="_self" data-bkval="482">商业百货</a></li><li><a target="_self" data-bkval="464">石油行业</a></li><li><a target="_self" data-bkval="454">塑料制品</a></li><li><a target="_self" data-bkval="438">食品饮料</a></li><li><a target="_self" data-bkval="424">水泥建材</a></li><li><a target="_self" data-bkval="1044">生物制品</a></li><li><b>T</b><a target="_self" data-bkval="545">通用设备</a></li><li><a target="_self" data-bkval="448">通信设备</a></li><li><a target="_self" data-bkval="421">铁路公路</a></li><li><a target="_self" data-bkval="736">通信服务</a></li><li><b>W</b><a target="_self" data-bkval="486">文化传媒</a></li><li><a target="_self" data-bkval="422">物流行业</a></li><li><b>X</b><a target="_self" data-bkval="1037">消费电子</a></li><li><a target="_self" data-bkval="1027">小金属</a></li><li><a target="_self" data-bkval="1018">橡胶制品</a></li><li><b>Y</b><a target="_self" data-bkval="478">有色金属</a></li><li><a target="_self" data-bkval="475">银行</a></li><li><a target="_self" data-bkval="458">仪器仪表</a></li><li><a target="_self" data-bkval="1046">游戏</a></li><li><a target="_self" data-bkval="1042">医药商业</a></li><li><a target="_self" data-bkval="1041">医疗器械</a></li><li><a target="_self" data-bkval="727">医疗服务</a></li><li><b>Z</b><a target="_self" data-bkval="539">综合行业</a></li><li><a target="_self" data-bkval="476">装修建材</a></li><li><a target="_self" data-bkval="473">证券</a></li><li><a target="_self" data-bkval="470">造纸印刷</a></li><li><a target="_self" data-bkval="1043">专业服务</a></li><li><a target="_self" data-bkval="1040">中药</a></li><li><a target="_self" data-bkval="910">专用设备</a></li><li><a target="_self" data-bkval="734">珠宝首饰</a></li><li><a target="_self" data-bkval="725">装修装饰</a></li><ul></ul></ul></div>"""
soup = BeautifulSoup(src_mapping, 'html.parser')

industry_dict = {}

for a_tag in soup.select('#hymore a[data-bkval]'):
    bid = a_tag.get('data-bkval')
    name = a_tag.text.strip()
    if bid and name:
        industry_dict[bid] = name


# 1. 行业研报
def get_dfcf_industry_research_report(industry_code, page=1, years_ago=2):
    """
    获取东方财富网的行业研报数据。
    :param industry_code: 行业代码
    :param page: 页码，默认为1
    """
    # API URL
    url = "https://reportapi.eastmoney.com/report/list" # 行业研报

    # 生成当前时间戳（毫秒级）
    timestamp = int(time.time() * 1000)
    # 当天年月日
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 将日期字符串转为 datetime 对象
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')

    two_years_ago = date_obj.replace(year=date_obj.year - years_ago).strftime('%Y-%m-%d')

    # 请求参数
    params = {
        'industryCode': str(industry_code),
        'pageSize': 50, # 每页多少条
        'industry': '*',
        'rating': '*',
        'ratingChange': '*',
        'beginTime': two_years_ago, # 2年前的
        'endTime': current_date,  # 使用系统提供的时间：2025年6月27日
        'pageNo': page,
        'fields': '',
        'qType': 1,
        'orgCode': '',
        'rcode': '',
        'p': page,
        'pageNum': page,
        'pageNumber': page,
        '_': timestamp,  # 使用动态生成的时间戳
    }

    # 设置请求头（模拟浏览器访问，防止反爬虫机制）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36'
    }

    # 发送GET请求
    response = requests.get(url, params=params, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        try:
            # 移除回调函数并解析JSON数据
            json_data = json.loads(response.text.replace('datatable3015936(', '').rstrip(')'))
            #print(json.dumps(json_data, ensure_ascii=False, indent=4))  # 打印格式化后的JSON数据
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
    else:
        print(f"Failed to retrieve data: HTTP Status Code {response.status_code}")

    return json_data


# 获取研报内容
def get_dfcf_industry_research_report_content(url):
    """
    获取东方财富网的行业研报内容。
    :param url: 研报的URL
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve report content: HTTP Status Code {response.status_code}")
        return None

# 解析研报内容
from bs4 import BeautifulSoup
# 找到 div ctx-content，里面是研报内容
def parse_dfcf_industry_research_report_content(html_content):
    """
    解析东方财富网的行业研报内容。
    :param html_content: 研报的HTML内容
    :return: 研报的文本内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', class_='ctx-content')
    pdf_link = soup.find('a', class_='pdf-link')
    pdf_url = None
    content = None
    if pdf_link:
        pdf_url = pdf_link['href']
    if content_div:
        content = content_div.get_text(strip=True)
    return content, pdf_url


# 获取行业研报
def get_dfcf_industry_research_report_list(industry_code, max_page=1, years_ago=2,save_path=None):
    """
    获取东方财富网的行业研报数据，并保存为CSV文件。
    :param industry_code: 行业代码
    :param max_page: 最大页码，默认为1
    :param years_ago: 获取多少年前的研报，默认为2年

    :return: 
        dfcf_research_df: 包含研报标题和URL的DataFrame
        save_path: 保存的CSV文件路径
    """
    if save_path is None:
        save_path = f'dfcf_industry_research_report_list_for_{industry_code}.csv'
    idx_list = []
    title_list = []
    infocede_list = []
    org_name_list = []
    url_list = []
    report_date_list = []

    idx_cnt = 0
    for page in range(1,max_page+1):
        print(f"正在获取第 {page} 页的研报数据...")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        dfcf_top50_research_url = get_dfcf_industry_research_report(industry_code, page=page, years_ago=years_ago)
        # with open(f"dfcf_industry_research_report_list_for_{industry_code}_page_{page}.json", 'w', encoding='utf-8') as f:
        #     json.dump(dfcf_top50_research_url, f, ensure_ascii=False, indent=4)
        for i in range(len(dfcf_top50_research_url['data'])):
            idx_list.append(idx_cnt)
            title_list.append(dfcf_top50_research_url['data'][i]['title'])
            infocede_list.append(dfcf_top50_research_url['data'][i]['infoCode'])
            org_name_list.append(dfcf_top50_research_url['data'][i]['orgName'])
            url_list.append('https://data.eastmoney.com/report/zw_industry.jshtml?infocode=' + dfcf_top50_research_url['data'][i]['infoCode'])
            report_date = dfcf_top50_research_url['data'][i]['publishDate']
            report_date = pd.to_datetime(report_date).strftime('%Y-%m-%d')
            report_date_list.append(report_date)
            idx_cnt += 1

    # 存储为csv文件
    import pandas as pd
    dfcf_research_df = pd.DataFrame({
        'idx': idx_list,
        'title': title_list,
        'report_date': report_date_list,
        'infocode': infocede_list,
        'url': url_list,
        'org_name': org_name_list
    })
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path


def get_dfcf_industry_resport_content(dfcf_research_df, industry_code,save_path=None):
    """
    获取东方财富网的行业研报内容，并保存为CSV文件。
    :param dfcf_research_df: 包含研报数据的DataFrame
    :param industry_code: 行业代码
    :return: 
        dfcf_research_df: 包含研报数据和内容的DataFrame
        save_path: 保存的CSV文件路径
    """
    if save_path is None:
        save_path = f'dfcf_industry_research_report_content_for_{industry_code}.csv'
    # 逐条获取研报内容
    url_content = []
    pdf_url_list = []
    for i in range(len(dfcf_research_df)):
        url = dfcf_research_df['url'][i]
        print(f"正在获取第 {i+1} 条行业研报内容，链接为：{url}")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        report_content = get_dfcf_industry_research_report_content(url)
        if report_content:
            # 解析第一个研报的内容
            parsed_content, pdf_url = parse_dfcf_industry_research_report_content(report_content) 
            if parsed_content:
                # 将解析后的内容添加到列表中
                url_content.append(parsed_content)
            else:
                url_content.append("")
            if pdf_url:
                pdf_url_list.append(pdf_url)
            else:
                pdf_url_list.append("")
        else:
            url_content.append("")
            pdf_url_list.append("")

    # 保存研报内容到CSV文件
    dfcf_research_df['content'] = url_content
    dfcf_research_df['pdf_url'] = pdf_url_list # 全文链接
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path


# 2. 个股研报
import requests
from datetime import datetime, timedelta
import time
import json
# 无法直接按照股票代码找公司研报，只能一个个行业去找，例如可以看一个行业的公司近期怎么样
def get_dfcf_company_research_report(industry_code, page=1, years_ago=2):
    
    # 生成当前时间戳（毫秒级）
    timestamp = int(time.time() * 1000)
    # 当天年月日
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 将日期字符串转为 datetime 对象
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')

    two_years_ago = date_obj.replace(year=date_obj.year - years_ago).strftime('%Y-%m-%d')

    # 1. 目标 URL，个股研报的
    url = "https://reportapi.eastmoney.com/report/list2"

    # 2. 请求体（Payload)
    json_data = {
        "beginTime": two_years_ago,
        "endTime": current_date,
        "industryCode": str(industry_code),
        "ratingChange": None,
        "rating": None,
        "orgCode": None,
        "code": "*",
        "rcode": "",
        "pageSize": 50,
        "pageNo": int(page) # 页码
    }

    # 3. 请求头（完全复现你提供的浏览器 headers）
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'reportapi.eastmoney.com',
        'Origin': 'https://data.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/report/stock.jshtml',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # 4. 发送 POST 请求
    try:
        response = requests.post(url, json=json_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 请求成功！状态码: 200")
            return data

        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print("响应内容:", response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"网络错误: {e}")

# 获取研报内容
def get_dfcf_company_research_report_content(url):
    """
    获取东方财富网的行业研报内容。
    :param url: 研报的URL
    """
    return get_dfcf_industry_research_report_content(url)

# 解析研报内容
from bs4 import BeautifulSoup
# 找到 div ctx-content，里面是研报内容
def parse_dfcf_company_research_report_content(html_content):
    """
    解析东方财富网的行业研报内容。
    :param html_content: 研报的HTML内容
    :return: 研报的文本内容
    """
    return parse_dfcf_industry_research_report_content(html_content)


# 获取个股研报
from time import sleep
import pandas as pd
def get_dfcf_company_research_report_list(industry_code, max_page=1, years_ago=2, save_path=None):
    """
    获取东方财富网的个股研报数据，并保存为CSV文件。
    :param industry_code: 公司的行业代码【暂不支持从股票代码来搜索公司】
    :param max_page: 最大页码，默认为1
    :param years_ago: 获取多少年前的研报，默认为2年
    :param save_path: 保存的CSV文件路径

    :return: 
        dfcf_research_df: 包含研报标题和URL的DataFrame
        save_path: 保存的CSV文件路径
    """
    if save_path is None:
        save_path = f'dfcf_company_research_report_list_for_{industry_code}.csv'
    idx_list = []
    title_list = []
    infocede_list = []
    url_list = []
    stock_code_list = []
    org_name_list = []
    report_date_list = []

    max_page = 1  # 最大获取研报页数
    idx_cnt = 0
    for page in range(1,max_page+1):
        print(f"正在获取第 {page} 页的研报数据...")
        sleep(0)  # 东方财富网的反爬虫机制，适当延时
        dfcf_top50_research_url = get_dfcf_company_research_report(industry_code, page=page, years_ago=years_ago)
        for i in range(len(dfcf_top50_research_url['data'])):
            idx_list.append(idx_cnt)
            title_list.append(dfcf_top50_research_url['data'][i]['title'])
            infocede_list.append(dfcf_top50_research_url['data'][i]['infoCode'])
            stock_code_list.append(dfcf_top50_research_url['data'][i]['stockCode'])
            org_name_list.append(dfcf_top50_research_url['data'][i]['orgName'])
            url_list.append('https://data.eastmoney.com/report/info/' + dfcf_top50_research_url['data'][i]['infoCode']+'.html')
            report_date = dfcf_top50_research_url['data'][i]['publishDate']
            report_date = pd.to_datetime(report_date).strftime('%Y-%m-%d')
            report_date_list.append(report_date)
            idx_cnt += 1

    # 存储为csv文件
    import pandas as pd
    dfcf_research_df = pd.DataFrame({
        'idx': idx_list,
        'title': title_list,
        'report_date': report_date_list,
        'infocode': infocede_list,
        'url': url_list,
        'stock_code': stock_code_list,
        'org_name': org_name_list
    })
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path


def get_dfcf_company_resport_content(dfcf_research_df, industry_code, save_path=None):
    """
    获取东方财富网的个股研报内容，并保存为CSV文件。
    :param dfcf_research_df: 包含研报数据list的DataFrame
    :param industry_code: 行业代码
    :param save_path: 保存的CSV文件路径
    :return:
        dfcf_research_df: 包含研报数据和内容的DataFrame
        save_path: 保存的CSV文件路径

    """
    if save_path is None:
        save_path = f'dfcf_company_research_report_content_for_{industry_code}.csv'
    url_content = []
    pdf_url_list = []
    for i in range(len(dfcf_research_df)):
        url = dfcf_research_df['url'][i]
        print(f"正在获取第 {i+1} 条企业研报内容，链接为：{url}")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        report_content = get_dfcf_company_research_report_content(url)
        if report_content:
            # 解析第一个研报的内容
            parsed_content, pdf_url = parse_dfcf_company_research_report_content(report_content) 
            if parsed_content:
                # 将解析后的内容添加到列表中
                url_content.append(parsed_content)
            else:
                url_content.append("")
            if pdf_url:
                pdf_url_list.append(pdf_url)
            else:
                pdf_url_list.append("")
        else:
            url_content.append("")
            pdf_url_list.append("")

    # 保存研报内容到CSV文件
    dfcf_research_df['content'] = url_content
    dfcf_research_df['pdf_url'] = pdf_url_list # 全文链接
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path


# 3. 宏观研究
# 原始的获取研报的api，慢一点sleep多一点
import requests
import json
import time
from datetime import datetime, timedelta

def get_dfcf_macro_research_report(page=1, years_ago=2):
    """
    获取东方财富网的宏观研报数据。
    :param page: 页码，默认为1
    """
    # API URL
    url = "https://reportapi.eastmoney.com/report/jg/" # 行业研报

    # 生成当前时间戳（毫秒级）
    timestamp = int(time.time() * 1000)
    # 当天年月日
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 将日期字符串转为 datetime 对象
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')

    two_years_ago = date_obj.replace(year=date_obj.year - years_ago).strftime('%Y-%m-%d')

    # 请求参数
    params = {
        'pageSize': 50, # 每页多少条
        'beginTime': two_years_ago, # 2年前的
        'endTime': current_date,  # 使用系统提供的时间：2025年6月27日
        'pageNo': page,
        'fields': '',
        'qType': 3,
        'orgCode': '',
        'rcode': '',
        'p': page,
        'pageNum': page,
        'pageNumber': page,
        '_': timestamp,  # 使用动态生成的时间戳
    }

    # 请求头（复现浏览器）
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'reportapi.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/report/macresearch.jshtml',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }


    # 发送GET请求
    response = requests.get(url, params=params, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        try:
            # 移除回调函数并解析JSON数据
            json_data = json.loads(response.text.replace('datatable7582033(', '').rstrip(')'))
            #print(json.dumps(json_data, ensure_ascii=False, indent=4))  # 打印格式化后的JSON数据
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
    else:
        print(f"Failed to retrieve data: HTTP Status Code {response.status_code}")

    return json_data


def get_dfcf_macro_research_report_list(max_page=1, years_ago=2, save_path=None):
    if save_path is None:
        save_path = f'dfcf_macro_research_report_list.csv'
    idx_list = []
    title_list = []
    infocede_list = []
    org_name_list = []
    url_list = []
    report_date_list = []

    max_page = 1  # 最大获取研报页数
    idx_cnt = 0
    for page in range(1,max_page+1):
        print(f"正在获取第 {page} 页的研报数据...")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        dfcf_top50_research_url = get_dfcf_macro_research_report(page=page, years_ago=years_ago)
        for i in range(len(dfcf_top50_research_url['data'])):
            idx_list.append(idx_cnt)
            title_list.append(dfcf_top50_research_url['data'][i]['title'])
            infocede_list.append(dfcf_top50_research_url['data'][i]['encodeUrl'])
            org_name_list.append(dfcf_top50_research_url['data'][i]['orgName'])
            url_list.append('https://data.eastmoney.com/report/zw_macresearch.jshtml?encodeUrl=' + dfcf_top50_research_url['data'][i]['encodeUrl'])
            report_date = dfcf_top50_research_url['data'][i]['publishDate']
            report_date = pd.to_datetime(report_date).strftime('%Y-%m-%d')
            report_date_list.append(report_date)
            idx_cnt += 1

    # 存储为csv文件
    import pandas as pd
    dfcf_research_df = pd.DataFrame({
        'idx': idx_list,
        'title': title_list,
        'report_date': report_date_list,
        'encodeUrl': infocede_list,
        'url': url_list,
        'org_name': org_name_list
    })
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path

# 获取研报内容
def get_dfcf_macro_research_report_content(url):
    """
    获取东方财富网的宏观研报内容。
    :param url: 研报的URL
    """
    return get_dfcf_industry_research_report_content(url)
    

# 解析研报内容
from bs4 import BeautifulSoup
# 找到 div ctx-content，里面是研报内容
def parse_dfcf_macro_research_report_content(html_content):
    """
    解析东方财富网的宏观研报内容。
    :param html_content: 研报的HTML内容
    :return: 研报的文本内容
    """
    return parse_dfcf_industry_research_report_content(html_content)


def get_dfcf_macro_resport_content(dfcf_research_df, save_path=None):
    """
    获取东方财富网的宏观研报内容，并保存为CSV文件。
    :param dfcf_research_df: 包含研报数据list的DataFrame
    :param save_path: 保存的CSV文件路径
    :return:
        dfcf_research_df: 包含研报数据和内容的DataFrame
        save_path: 保存的CSV文件路径

    """
    if save_path is None:
        save_path = 'dfcf_macro_research_report_content.csv'
    url_content = []
    pdf_url_list = []
    for i in range(len(dfcf_research_df)):
        url = dfcf_research_df['url'][i]
        print(f"正在获取第 {i+1} 条宏观研报内容，链接为：{url}")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        report_content = get_dfcf_macro_research_report_content(url)
        if report_content:
            # 解析第一个研报的内容
            parsed_content, pdf_url = parse_dfcf_macro_research_report_content(report_content)
            if parsed_content:
                # 将解析后的内容添加到列表中
                url_content.append(parsed_content)
            else:
                url_content.append("")
            if pdf_url:
                pdf_url_list.append(pdf_url)
            else:
                pdf_url_list.append("")
        else:
            url_content.append("")
            pdf_url_list.append("")

    # 保存研报内容到CSV文件
    dfcf_research_df['content'] = url_content
    dfcf_research_df['pdf_url'] = pdf_url_list # 全文链接
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path


# 4. 晨报
# 原始的获取研报的api，慢一点sleep多一点
import requests
import json
import time
from datetime import datetime, timedelta

def get_dfcf_chenbao_research_report(page=1, years_ago=2):
    """
    获取东方财富网的宏观研报数据。
    :param page: 页码，默认为1
    """
    # API URL
    url = "https://reportapi.eastmoney.com/report/jg/" # 行业研报

    # 生成当前时间戳（毫秒级）
    timestamp = int(time.time() * 1000)
    # 当天年月日
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 将日期字符串转为 datetime 对象
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')

    two_years_ago = date_obj.replace(year=date_obj.year - years_ago).strftime('%Y-%m-%d')

    # 请求参数
    params = {
        'pageSize': 50, # 每页多少条
        'beginTime': two_years_ago, # 2年前的
        'endTime': current_date,  # 使用系统提供的时间：2025年6月27日
        'pageNo': page,
        'fields': '',
        'qType': 4,
        'orgCode': '',
        'rcode': '',
        'p': page,
        'pageNum': page,
        'pageNumber': page,
        '_': timestamp,  # 使用动态生成的时间戳
    }

    # 请求头（复现浏览器）
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'reportapi.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/report/brokerreport.jshtml',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }


    # 发送GET请求
    response = requests.get(url, params=params, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        try:
            # 移除回调函数并解析JSON数据
            json_data = json.loads(response.text.replace('datatable7582033(', '').rstrip(')'))
            #print(json.dumps(json_data, ensure_ascii=False, indent=4))  # 打印格式化后的JSON数据
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
    else:
        print(f"Failed to retrieve data: HTTP Status Code {response.status_code}")

    return json_data

def get_dfcf_chenbao_research_report_list(max_page=1, years_ago=2, save_path=None):
    # 获取第一页的研报数据
    from time import sleep
    import pandas as pd
    if save_path is None:
        save_path = f'dfcf_chenbao_research_report_list.csv'
    idx_list = []
    title_list = []
    infocede_list = []
    org_name_list = []
    url_list = []
    report_date_list = []

    max_page = 1  # 最大获取研报页数
    idx_cnt = 0
    for page in range(1,max_page+1):
        print(f"正在获取第 {page} 页的晨报数据...")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        dfcf_top50_research_url = get_dfcf_chenbao_research_report(page=page, years_ago=2)
        for i in range(len(dfcf_top50_research_url['data'])):
            idx_list.append(idx_cnt)
            title_list.append(dfcf_top50_research_url['data'][i]['title'])
            infocede_list.append(dfcf_top50_research_url['data'][i]['encodeUrl'])
            org_name_list.append(dfcf_top50_research_url['data'][i]['orgName'])
            url_list.append('https://data.eastmoney.com/report/zw_brokerreport.jshtml?encodeUrl=' + dfcf_top50_research_url['data'][i]['encodeUrl'])
            report_date = dfcf_top50_research_url['data'][i]['publishDate']
            report_date = pd.to_datetime(report_date).strftime('%Y-%m-%d')
            report_date_list.append(report_date)
            idx_cnt += 1

    # 存储为csv文件
    import pandas as pd
    dfcf_research_df = pd.DataFrame({
        'idx': idx_list,
        'title': title_list,
        'report_date': report_date_list,
        'encodeUrl': infocede_list,
        'url': url_list,
        'org_name': org_name_list
    })
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path

# 获取研报内容
def get_dfcf_chenbao_research_report_content(url):
    """
    获取东方财富网的宏观研报内容。
    :param url: 研报的URL
    """
    return get_dfcf_industry_research_report_content(url)
    

# 解析研报内容
from bs4 import BeautifulSoup
# 找到 div ctx-content，里面是研报内容
def parse_dfcf_chenbao_research_report_content(html_content):
    """
    解析东方财富网的宏观研报内容。
    :param html_content: 研报的HTML内容
    :return: 研报的文本内容
    """
    return parse_dfcf_industry_research_report_content(html_content)


def get_dfcf_chenbao_resport_content(dfcf_research_df, save_path=None):
    """
    获取东方财富网的晨报研报内容，并保存为CSV文件。
    :param dfcf_research_df: 包含研报数据list的DataFrame
    :param save_path: 保存的CSV文件路径
    :return:
        dfcf_research_df: 包含研报数据和内容的DataFrame
        save_path: 保存的CSV文件路径

    """
    if save_path is None:
        save_path = 'dfcf_chenbao_research_report_content.csv'
    url_content = []
    pdf_url_list = []
    for i in range(len(dfcf_research_df)):
        url = dfcf_research_df['url'][i]
        print(f"正在获取第 {i+1} 条晨报内容，链接为：{url}")
        sleep(20)  # 东方财富网的反爬虫机制，适当延时
        report_content = get_dfcf_chenbao_research_report_content(url)
        if report_content:
            # 解析第一个研报的内容
            parsed_content, pdf_url = parse_dfcf_chenbao_research_report_content(report_content)
            if parsed_content:
                # 将解析后的内容添加到列表中
                url_content.append(parsed_content)
            else:
                url_content.append("")
            if pdf_url:
                pdf_url_list.append(pdf_url)
            else:
                pdf_url_list.append("")
        else:
            url_content.append("")
            pdf_url_list.append("")

    # 保存研报内容到CSV文件
    dfcf_research_df['content'] = url_content
    dfcf_research_df['pdf_url'] = pdf_url_list # 全文链接
    dfcf_research_df.to_csv(save_path, index=False, encoding='utf-8')
    return dfcf_research_df, save_path

