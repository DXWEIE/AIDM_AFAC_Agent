from langchain_openai import ChatOpenAI
import os
import re
import json
import pandas as pd
import numpy as np
import base64
from e2b_code_interpreter import Sandbox
from langchain_community.chat_models.tongyi import ChatTongyi
from PIL import Image
import io
import base64
from openai import OpenAI

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
import json
import pandas as pd
import textwrap
from datetime import datetime
import requests
import dashscope
from http import HTTPStatus
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import jieba
# 在 Jupyter Cell 中运行
from playwright.async_api import async_playwright
import asyncio
import re
import requests
from urllib.parse import urlparse
from pathlib import Path
from typing import Tuple, Optional
import arxiv

# 确保安装这些库：
# pip install requests pdf4llm openpyxl pandas python-docx PyMuPDF

import pdf4llm
import nest_asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter


import os
from openai import OpenAI

##################################################  常量 ##################################################


E2B_API_KEY = 'e2b_xxxx'
ALI_API_KEY = 'sk-xxxx'
BAIDU_KEY='bce-v3/ALTAK-xxxx/xxxx'


qwen_plus = ChatTongyi(
    model="qwen-plus-latest",
    api_key=ALI_API_KEY, temperature=0
)

deepseek_v3 = ChatOpenAI(model="deepseek-v3", temperature=0, api_key=ALI_API_KEY,
                         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

qwen_vl_model = "qwen-vl-plus-latest"
os.environ["E2B_API_KEY"] = E2B_API_KEY

client = OpenAI(
    api_key=ALI_API_KEY, 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


deepseek_r1 = ChatOpenAI(model="deepseek-r1-0528", temperature=0, api_key=ALI_API_KEY,
                         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

deepseek_v3 = ChatOpenAI(model="deepseek-v3", temperature=0, api_key=ALI_API_KEY,
                         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

kimi_model = ChatOpenAI(model="Moonshot-Kimi-K2-Instruct", temperature=0, api_key=ALI_API_KEY,
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

qwen_plus = ChatTongyi(
    model="qwen-plus-latest",
    api_key=ALI_API_KEY, temperature=0
)




qwen_flash = ChatTongyi(
    model="qwen-flash",
    api_key=ALI_API_KEY, temperature=0
)

base_model = ChatTongyi(
    model="qwen-flash",
    api_key=ALI_API_KEY, temperature=0
)

EMBEDDING_MODEL ="multimodal-embedding-v1"  # embedding的模型，这个暂时免费

# 获取文本的embedding向量，维度为1-24维度
def get_text_embedding(text):
    input = [{'text': text}]
    # 调用模型接口，向量维度1024
    resp = dashscope.MultiModalEmbedding.call(
        model=EMBEDDING_MODEL, # 这个暂时免费
        input=input,
        api_key=ALI_API_KEY
    )
    if resp.status_code == HTTPStatus.OK:
        # 返回向量1024维的
        vec = resp['output']['embeddings'][0]['embedding']
        # 变成numpy数组
        vec = np.array(vec)
        return vec
    else:
        return None
    # resp = dashscope.TextEmbedding.call(
    #     model="text-embedding-v4",
    #     input=text,
    #     dimension=1024,  # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    #     output_type="dense&sparse",api_key=ALI_API_KEY
    # )
    # if resp.status_code == HTTPStatus.OK:
    #     vec = resp['output']['embeddings'][0]['embedding']
    #     vec = np.array(vec)
    #     return vec
    # else:
    #     return None