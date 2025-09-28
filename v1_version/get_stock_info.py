import akshare as ak

def get_cn_stock_info(symbol, period="monthly", start_date="20250101", end_date="20250601"):
    """
    获取中国股票的基本信息
    :param stock_code: 6位股票代码，不带交易所代码
    :param period: 数据周期，默认为"monthly"
    :param start_date: 开始日期，格式为"YYYYMMDD"，默认为"20250101"
    :param end_date: 结束日期，格式为"YYYYMMDD"，默认为"20250601"
    :return: 股票的基本信息dataframe
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    stock_info = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
    return stock_info

def get_hk_stock_info(symbol, period="monthly", start_date="20250101", end_date="20250601"):
    """
    获取香港股票的基本信息
    :param stock_code: 5位股票代码
    :param period: 数据周期，默认为"monthly"
    :param start_date: 开始日期，格式为"YYYYMMDD"，默认为"20250101"
    :param end_date: 结束日期，格式为"YYYYMMDD"，默认为"20250601"
    :return: 股票的基本信息dataframe，单位为港元
    # ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
    """
    symbol = symbol.upper()
    symbol = ''.join(filter(str.isdigit, symbol))  # 只保留数字
    if len(symbol) > 4:
        symbol = symbol[-4:]
    stock_info = ak.stock_hk_hist(symbol='0'+symbol, period=period, start_date=start_date, end_date=end_date)
    return stock_info


