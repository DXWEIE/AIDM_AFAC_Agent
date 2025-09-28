from constants import *


full_answer_generation_template_financial = """
你是能够解决复杂研究问题的专家。在用户询问问题时，你的任务是为用户的任务提供简洁清晰的答案；在用户希望获取数据或据此撰写时，你需要提供一份全面的报告。
请注意，你需要根据所提供的参考资料生成答案。

用户的问题/研究主题：
{task}

参考资料：
{references}

请判断用户的意图，仔细分析参考资料，并依据用户的需求，将参考整合为一份连贯的报告/答案。

报告撰写说明：
- 使用清晰、专业的语言，符合商业或技术受众的阅读习惯
- 逻辑连贯地整合信息，不添加无依据的主张
- 如果用户的问题/研究主题涉及对详细数据的问询，请务必包含所有相关的关键的事实信息、原始数据、统计数据等

问题回答说明：
- 基于所提供的参考资料，提供全面且简洁的答案，完整回应问题。

请勿包含免责声明、过程说明或对来源格式的提及。撰写时需符合最终交付成果的标准。

注意事项：
- 必须使用与用户问题/研究主题相同的语言（英文或中文）。所有内容均需采用markdown格式，包括适当的标题、项目符号等格式元素，以提升可读性，写入content字段中。
- 若参考资料中不包含任何相关信息，在"finished"字段中回复"no"，在"content"字段中留空字符串。
- 若参考资料不足以回答问题且需要更多背景信息，在"finished"字段中回复"no"，在"content"字段中根据现有信息生成部分答案。

你的最终回应必须是符合以下格式的有效JSON对象，无需解释：
```json
{{"language": "中文"
,"content": "以markdown格式生成的答案或报告",
"finished": "yes"}}```
"""


full_answer_generation_template_en = """
You are an expert in solving complex research questions. Your task is to provide a concise and clear answer to the user's task or write a comprehensive report accordingly.
Note that you need to generate your answer based on the provided reference materials.

User's question/research topic:
{task}

Reference materials:
{references}

Carefully analyze the references and synthesize the information into a coherent report/answer.

Instructions for writing the report:
- Focus on key aspects such as current status, challenges, and practical applications
- Use clear and professional language suitable for a business or technical audience
- Integrate information logically without adding unsupported claims

Instructions for question answering:
- Provide a comprehensive yet concise answer that fully addresses the question using the provided reference materials.

Do not include disclaimers, explanations of your process, or references to the source format. Write as if producing a final deliverable.

Attention: 
- You must use the same language as the user's question/research topic, whether it's English or Chinese. All content must be in markdown format, including appropriate headings, bullet points, and other formatting elements to enhance readability.
- If the reference materials do not contain any relevant information, respond with "no" in "finished" field, and left a empty string in the "content" field.
- If the reference materials are insufficient to answer the question and need more context, respond with "no" in "finished" field, and generate parts of the answer based on the available information in "content" field.

Your final response must be a valid JSON object in the following format, without any additional text or explanation:
```json
{{"language": "English"
,"content": "[The answer or report you generated in markdown format]",
"finished": "yes"}}```
"""


find_most_relevant_url_prompt_template = """
You are a web search and navigation expert. Your task is to find the most relevant URL which may contain the answer to the user's query.
Given the user's query and a list of candidate URLs with their titles and content snippets, identify the URL that is most likely to contain the answer. 
Just return the index (0-based) of the most relevant URL. If none of the URLs seem relevant, respond with -1.
Note that you need to recall the background knowledge from the user query and the candidate URLs.
You also need to consider both the title and the text snippet and the user query when making your decision.

User query: {query}
Candidate content:
{urls}

Note that you can return at most 2 indices, separated by commas, if you believe multiple URLs are relevant.
Now, please provide your answer. No explanations, just the index or indices.
"""


find_most_relevant_html_prompt_template_financial = """
你是一名网络搜索专家。你的任务是找到最相关的参考资料，这些资料可能包含用户查询问题的答案。
给定用户的查询以及带有标题和内容片段的候选资料列表，请识别出最有可能包含答案的资料。
只需返回最相关资料的索引（从0开始计数）。如果所有资料似乎都不相关，请回复-1。
请注意，你需要结合用户查询和候选资料中的背景信息进行判断。
在做决定时，你还需要同时考虑标题、文本片段以及用户的查询。

用户查询：{query}
候选内容：
{search_results}

请注意，如果你认为多个资料均相关，最多可返回2个索引，用逗号分隔。
现在，请提供你的答案。无需解释，只需返回索引即可。
"""

find_most_relevant_html_prompt_template = """
You are a web search and navigation expert. Your task is to find the most relevant reference material which may contain the answer to the user's query.
Given the user's query and a list of candidate materials with their titles and content snippets, identify the material that is most likely to contain the answer.
Just return the index (0-based) of the most relevant material. If none of the materials seem relevant, respond with -1.
Note that you need to recall the background knowledge from the user query and the candidate materials.
You also need to consider both the title and the text snippet and the user query when making your decision.

User query: {query}
Candidate content:
{search_results}

Note that you can return at most 2 indices, separated by commas, if you believe multiple materials are relevant.
Now, please provide your answer. No explanations, just the index or indices.
"""



search_answer_prompt_template_en = """
You are an expert research assistant with deep knowledge across multiple domains. 

# QUESTION:
{query}

# REFERENCE MATERIALS:
{relevant_docs}

Your task is to answer the question / write a report based on the provided reference materials.
If the task is about to write a report, you need to write a structured report with clear sections. Otherwise, just give a direct answer to the question.

# Instructions for writing the report:
1. **Knowledge Integration**: Synthesize information from all relevant sections of the reference materials to form a complete answer
2. **Direct Quotation**: Include all relevant factual information, numbers, statistics, etc., if available.
3. **Confidence Assessment**: 
   - If the references provide complete information: Deliver a definitive answer
   - If the references provide partial information: Answer based on available information and note any limitations
   - If the references don't contain relevant information: State that the answer cannot be found in the provided materials
4. **Structural Clarity**: Organize complex answers with clear section headings or bullet points when appropriate
5. **Precision**: Avoid speculative content or information not present in the references

# Instructions for answering questions:
- Provide a comprehensive yet concise answer that fully addresses the question using the provided reference materials.

# Attention:
**Language Consistency**: Use the same language as the QUESTION, whether it's English or Chinese
**Markdown Format**: Use markdown format for the answer, including appropriate headings, bullet points, and other formatting elements to enhance readability.

Please begin.
"""


search_rewrite_template_financial = """
当前时间：{date}

你是一名搜索专家，需要使用搜索引擎查找相关信息以解答用户提出的问题：
{query}

为了更好地开展搜索，你首先需要判断是否有必要重写问题表述，使其更适合在搜索引擎中查找相关知识。若需要重写，在is_change字段返回true，并在query_rewrite字段输出重写后的问题；若无需重写，在is_change字段返回false。
请注意，必须使用与用户原始问题相同的语言（英文或中文）。

按以下格式输出内容（仅输出JSON，不提供任何额外内容或信息）：
```json
{{
     "is_change":true/false,
     "query_rewrite":"重写后的问题"
}}```
"""

search_rewrite_template_en = """
Current time is {date}

You are a search expert and need to use a search engine to find relevant information to answer the question posed by the user:
{query}

In order to conduct a better search, you first need to determine whether it is necessary to rewrite the question statement to make it more suitable for finding relevant knowledge in the search engine. If a rewrite is necessary, return is_change as true and output the rewritten question in the query_rewrite field; otherwise, output is_search as false.
Note that you must use the same language as the user's original question, whether it's English or Chinese.

Output the content in the following format (only output JSON, do not provide any extra content or information):
```json
{{
     "is_change":true/false,
     "query_rewrite":"Rewritten question"
}}```
"""


task_rewrite_template_financial = """
你是一位擅长解决复杂研究问题的专家。你的任务是将用户的话题优化为一个定义清晰、适合开展研究的话题，便于后续的信息检索、资料收集与分析处理。

改写后的主题应满足以下要求：
- 具备具体性和可检索性，便于开展多步骤的信息搜集与分析。
- 若涉及时效性，需结合当前日期。
- 使用与用户原始主题相同的语言（中文或英文）。

当前日期：
{date}

用户原始主题：
{task}

优化后的主题（无需解释，保留原意，简洁且可操作）：
"""


task_rewrite_template_en = """
You are an expert in solving complex research questions. Your task is to refine the user's topic into a well-defined, research-ready theme suitable for searching, information gathering and processing.

The rewritten topic should:
- Focus on a clear technological or business concept.
- Include key aspects such as current status, challenges, and practical applications.
- Be specific and searchable, enabling effective multi-step information gathering.
- Incorporate the current date if time-sensitive.
- Use the same language as the user's original topic, whether it's English or Chinese.

Current date:
{date}

User's original topic:
{task}

Refined report topic (do not add explanations, keep the intent, make it concise and actionable):
"""


sub_task_divide_template_financial = """
你是一位擅长解决复杂研究问题的专家。你的任务是将用户的提问或研究主题拆解为一系列清晰、可操作的子任务，以便开展信息搜集。

目标是支持撰写一份结构清晰的报告，涵盖该主题的现状、关键挑战及实际应用。为确保研究高效推进，请将主题拆解为最多5个子任务，要求：
- 逻辑有序，可独立开展研究
- 若主题具有时效性，需包含明确的时间范围（例如“截至2025年”），避免使用“近期”“今年”等模糊表述
- 语言简洁，面向用户提问或研究主题
- 使用与用户原始问题相同的语言（中文或英文）

用户的问题/研究主题：
{task}

输出格式：
- 使用如下格式：
  #1# 子任务 1
  #2# 子任务 2
  ...
- 不要使用任何 Markdown
- 不要包含任何解释性文字

请开始。
"""


sub_task_divide_template_en = """
You are an expert in solving complex research questions. Your task is to break down the user's question/research topic into a sequence of clear, actionable subtasks for information gathering.

The goal is to support the writing of a structured report covering the current status, key challenges, and practical applications of the topic. To ensure effective research, please decompose the topic into up to 5 subtasks that:
- Are logically ordered and can be researched independently
- Focus on specific aspects such as definitions, current trends, technical/business challenges, real-world applications, or future outlook
- Include explicit time references (e.g., 'as of 2025') if the topic is time-sensitive—avoid vague terms like 'recently' or 'this year'
- Are concise and research-oriented
- Use the same language as the user's question/research topic, whether it's English or Chinese

User's question/research topic:
{task}

Output format:
- Use the format:
  #1# Subtask 1
  #2# Subtask 2
  ...
- Do not use any Markdown
- Do not include any explanatory text

Please begin.
"""

direct_answer_template_financial = """
你是解决复杂研究问题的专家。请根据你的知识，为用户的任务提供简洁清晰的答案，或据此撰写一份全面的报告。

用户的问题/研究主题：
{subtask}

注意：严禁进行网络搜索或参考外部来源，仅基于你的内部知识作答。
此外，必须使用与用户问题/研究主题相同的语言（英文或中文）。

请提供直接、详实的回应，无需任何额外说明。
你的答案：
"""

direct_answer_template_en = """
You are an expert in solving complex research questions. Based on your knowledge, provide a concise and clear answer to the user's task or write a comprehensive report accordingly.

User's question/research topic:
{subtask}

Note: You must not perform web searches or reference external sources. Answer solely based on your internal knowledge.
Besides, you must use the same language as the user's question/research topic, whether it's English or Chinese. 

Provide a direct, informative response without any additional explanation.
Your answer:
"""

question_router_template_financial = """
你是一位专业的研究评估专家。请分析用户的任务，判断是否需要调用搜索引擎获取外部信息。

任务：
{subtask}

如果该任务需要获取以下类型的信息，请回复 "yes"：
- 最新的市场动态、政策变化、行业趋势、经济和金融财务数据
- 公司新闻、项目进展、监管文件
- 权威媒体报道或第三方研究报告

如果该任务仅涉及通用知识、基本概念、常识性内容，无需外部信息，请回复 "no"。

仅回复 "yes" 或 "no"，不要包含任何解释。
你的回复：
"""

question_router_template_en = """
You are an expert research evaluator. Analyze the user's task and determine the most appropriate information source.

task:
{subtask}

Classify the task into one of three categories:

- "knowledge": The task can be answered using general domain knowledge (e.g., definitions, established principles, widely known facts). No external data needed.
- "search": The task requires up-to-date, real-world, or policy-related information (e.g., recent events, market trends, geopolitical developments, government policies, industry reports). Use a general search engine.
- "arxiv": The task involves a technical, scientific, or academic research question (e.g., model feasibility, algorithm comparison, theoretical analysis, peer-reviewed advances). Use academic databases like arXiv.

Respond ONLY with one word: "knowledge", "search", or "arxiv". Do not include any explanation.
Your response:
"""



arxiv_search_rewrite_template_en = """
Current time is {date}

You are a search expert and need to find relevant information in arXiv to answer the question posed by the user:
{query}

In order to conduct a better search, you first need to determine whether it is necessary to rewrite the question statement to make it more suitable for finding relevant knowledge in the arXiv search engine. If a rewrite is necessary, return is_change as true and output the rewritten question in the query_rewrite field; otherwise, output is_search as false.

Output the content in the following format (only output JSON, do not provide any extra content or information):
```json
{{
     "is_change":true/false,
     "query_rewrite":"Rewritten question"
}}```
"""



find_most_relevant_paper_prompt = """
You are an expert research assistant with deep knowledge across multiple domains. Your task is to identify the most relevant academic paper from a list of search results based strictly on the query provided below.
{query}
You have access to the following list of academic papers, each with a index number, title, and summary:
{search_results}

Your task is to evaluate the relevance of each paper to the query and select the one that best addresses the topic.
Please provide the index number of the most relevant paper. No explanations or additional information are needed, just the index number.
"""

# 计算相似度，取top k的文档
def get_top_k_search_results(search_result_list, rewrite_vector,search_np_vectors,top_k=10):
    if len(search_result_list) > top_k:
        # 超过top_k条，调用top K算法
        similarities = cosine_similarity(rewrite_vector.reshape(1, -1), search_np_vectors)
        top_k_indices = similarities[0].argsort()[-top_k:][::-1]
        return [search_result_list[i] for i in top_k_indices]
    else:
        return search_result_list

def arxiv_search(rewrite_query, top_k=20):
    search_result_list = []
    print('[arxiv_search]search_query = ', rewrite_query)
    try:
        search = arxiv.Search(
            query=rewrite_query,
            max_results=top_k,
            sort_by=arxiv.SortCriterion.Relevance
        )
        for result in search.results():
            search_result_list.append({
                'url': result.entry_id,
                'title': result.title,
                'content': result.summary
            })
    except Exception as e:
        print(f"[arxiv_search]Error: {e}")
    return search_result_list


# arxiv论文下载到本地
def download_pdf(url, save_path='downloaded_paper.pdf'):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print(f"Failed to download PDF. Status code: {response.status_code}")
            return None
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully and saved to {save_path}")
        return save_path
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None
# download_url = arxiv_list[5].replace('abs','pdf')
# download_pdf(download_url)


def download_pdf_with_curl(url, refer_url, output_path='downloaded_report.pdf'):
    """
    使用curl命令下载PDF文件

    Args:
        url: PDF文件的URL
        output_path: 保存路径

    Returns:
        output_path: 保存路径
    """
    try:
        import subprocess

        print(f"使用curl命令下载PDF: {url}")

        # 构建curl命令
        if refer_url is not None:
            cmd = [
                "curl",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "-e", refer_url,
                "-o", output_path,
                url
            ]
        else:
            cmd = [
                "curl",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "-o", output_path,
                url
            ]

        # 执行curl命令
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查命令是否成功执行
        if result.returncode == 0:
            # 检查下载的文件是否为PDF
            with open(output_path, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    print(f"成功下载PDF文件: {output_path}")
                    return output_path
                else:
                    print(f"下载的文件不是PDF格式: {output_path}")
                    return None
        else:
            print(f"curl命令执行失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"使用curl命令下载PDF时出错: {e}")
        return None


import re

def extract_sections_robust_enhanced(markdown_text, target_sections, debug=False):
    # === 同义词关键词（只需核心词）===
    keywords = {
        'abstract': ['abstract', 'summary'],
        'introduction': ['introduction', 'intro'],
        'related work': ['related work','related works', 'prior work', 'literature review', 
                        'background', 'previous work'],
        'conclusion': ['conclusion', 'conclusions', 'concluding remarks', 'conclu']
    }

    sections = {sec: "" for sec in target_sections}
    current_section = None
    current_content = []
    first_section_found = False

    def normalize_text(text):
        text = re.sub(r'\s+', ' ', text)  # 统一空格
        return text.strip().lower()

    def contains_any_keyword(title, keyword_list):
        title_norm = normalize_text(title)
        for kw in keyword_list:
            if kw in title_norm:
                return True
        return False

    def match_section(raw_title):
        # 去除编号：1 , 1. , 2) , 3.1 等
        clean_title = re.sub(r'^\s*\d+[\.\)]?\s*', '', raw_title)
        clean_title = re.sub(r'^[IVXLCDM]+[\.\)]?\s*', '', clean_title)  # Roman
        clean_title = normalize_text(clean_title)

        matched = None
        for sec, keys in keywords.items():
            if contains_any_keyword(clean_title, keys):
                matched = sec
                break
        if debug and matched:
            print(f"✅ 匹配到章节: '{raw_title}' → '{matched}'")
        return matched

    def is_bold_heading(line):
        line_stripped = line.strip()
        bold_match = re.match(r'^\s*\*\*(.+?)\*\*\s*$', line_stripped)
        if bold_match:
            inner = bold_match.group(1).strip()
            return True, inner
        return False, None

    def is_hash_heading(line):
        line_stripped = line.strip()
        hash_match = re.match(r'^#{1,6}\s+(.+)$', line_stripped)
        if hash_match:
            return True, hash_match.group(1).strip()
        return False, None

    # 预处理
    if hasattr(markdown_text, 'text'):
        markdown_text = markdown_text.text
    markdown_text = markdown_text.replace('\r\n', '\n').replace('\r', '\n')
    lines = markdown_text.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        is_title = False
        raw_title = None

        # 检查加粗标题（你的主要格式）
        is_bold, bold_title = is_bold_heading(line)
        if is_bold:
            raw_title = bold_title
            is_title = True

        # 检查 # 标题
        if not is_title:
            is_hash, hash_title = is_hash_heading(line)
            if is_hash:
                raw_title = hash_title
                is_title = True

        if is_title and raw_title:
            matched_section = match_section(raw_title)

            if matched_section in target_sections:
                # 保存上一节
                if current_section is not None:
                    sections[current_section] = '\n'.join(current_content).strip()
                    if debug:
                        print(f"💾 保存章节: {current_section}")
                # 开始新节
                current_section = matched_section
                current_content = []
                first_section_found = True
                if debug:
                    print(f"➡️ 进入章节: {current_section}")
            else:
                # 非目标章节，结束收集
                if current_section is not None:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = None
                current_content = None
            continue

        # 收集内容
        if current_section is not None and current_content is not None:
            current_content.append(line)
        elif not first_section_found and line_stripped:
            # 在第一个章节前的内容（可能是 abstract）
            pass  # 我们不再提前收集，而是靠后续的 **Abstract** 正确提取

    # 保存最后一节
    if current_section is not None and current_content is not None:
        sections[current_section] = '\n'.join(current_content).strip()
        if debug:
            print(f"💾 保存最后一节: {current_section}")

    return sections

# target_sections = ['abstract', 'introduction', 'related work', 'conclusion']
# sections = extract_sections_robust_enhanced(md_text, target_sections,debug=False)
# for title, content in sections.items():
#     print(f"\n--- {title.upper()} ---\n")
#     print(content)


def downlaod_and_read_arxiv_paper(query,title,url):
    print(f'[downlaod_and_read_arxiv_paper]《{title}》download_url = ',url)
    download_url = url.replace('abs','pdf')
    pdf_path = download_pdf(download_url,save_path=download_url.split('/')[-1].replace('.','_')+'.pdf')
    if pdf_path is None:
        return None
    try:
        # 返回markdown文本
        md_text = pdf4llm.to_markdown(pdf_path)
        # 解析出章节信息
        target_sections = ['abstract', 'introduction', 'related work', 'conclusion']
        sections = extract_sections_robust_enhanced(md_text, target_sections,debug=False) # dict的形式
        # 检查sections的每个key->value长度是否超过50，否则就删掉这个key
        for key,values in list(sections.items()):
            if len(values) < 50:
                del sections[key]
        # 利用资料回答问题
        sub_answer_prompt = search_answer_prompt_template_en.format(
            query=query,
            relevant_docs='\n\n'.join([f"### {k}\n{v}" for k,v in sections.items()])
        )
        sub_answer_resp = qwen_flash.invoke(sub_answer_prompt)
        # 删除下载的pdf文件
        os.remove(pdf_path)
        print(f"[downlaod_and_read_arxiv_paper]Successfully read and deleted PDF: {pdf_path}")
        return sub_answer_resp.content
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ''


def simple_qa_en_arxiv(query,max_search_num=10):
    print('[simple_qa]original query = ',query)
    search_rewrite_prompt = arxiv_search_rewrite_template_en.format(
        date=datetime.now().strftime("%Y-%m-%d"),
        query=query
    )

    ##  step1. 问题改写
    rewrite_result = deepseek_v3.invoke(search_rewrite_prompt)
    print('[simple_qa]rewrite query = ',rewrite_result.content)
    
    try:
        json_match = re.search(r'```json\n(.*?)\n```', rewrite_result.content, re.DOTALL)
        json_str = json_match.group(1)
        search_query = json.loads(json_str)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        search_query = {'is_change': True, 'query_rewrite': query} # 兜底
    print(f"[simple_qa]rewrite search_query = {search_query['query_rewrite']}")

    ## step2. 进行搜索
    search_result_list = arxiv_search(search_query['query_rewrite'],top_k=20) # 取20条
    #search_result_list是{ 'url': item['url'], 'title': item['title'], 'content': item['content'] }格式，其中content是arxiv生成的summary
    if len(search_result_list) == 0:
        print("[simple_qa]No search results found.[arxiv_search]error!")
        return "没有找到相关的搜索结果，请尝试更换问题或重试。"

    ## step3. 获取最相关文档的总结信息
    if len(search_result_list) > max_search_num:  # 如果搜索结果超过10条，选出top 10最相关的
        # 分别获取rewrite_result和search_result_list的向量，调用get_text_embedding函数
        rewrite_vector = get_text_embedding(search_query['query_rewrite'])
        search_vectors = [get_text_embedding(item['title']+' '+item['content']) for item in search_result_list]
        if rewrite_result is None or search_vectors is None:
            print("[simple_qa]Error: Failed to get embeddings for rewrite query or search results.")
            return "无法获取相关的搜索结果，请稍后再试。"
        # search_vectors变成numpy数组
        search_np_vectors = np.array(search_vectors) # N个1024维度向量
        relevant_search_results = get_top_k_search_results(search_result_list, rewrite_vector, search_np_vectors, top_k=max_search_num)
    else:
        relevant_search_results = search_result_list
    print(f"[simple_qa]relevant_search_results\n {relevant_search_results}")

    ## step4. 和问题最相关的一篇论文，进行下载以及阅读
    chunk = []
    for i in range(len(relevant_search_results)):
        doc = relevant_search_results[i]
        chunk.append(f"Index [{i}]： title：{doc['title']}，cotent：{doc['content']}\n")
    find_most_relevant_paper_prompt_filled = find_most_relevant_paper_prompt.format(
        query=query,
        search_results="\n".join(chunk)
    )
    # 最相关的仔细阅读内容
    try: 
        most_relevant_paper_result = deepseek_v3.invoke(find_most_relevant_paper_prompt_filled)
        print('[simple_qa]most_relevant_paper_result = ', most_relevant_paper_result.content)
        most_relevant_index = int(re.search(r'\d+', most_relevant_paper_result.content).group())
        print(f"[simple_qa]most_relevant_index = {most_relevant_index}")
        # 只保留最相关的一篇论文
        most_relevant_index = max(0, min(most_relevant_index, len(relevant_search_results)-1)) # 防止越界
        most_relevant_paper = relevant_search_results[most_relevant_index]
        # 下载并且阅读该论文的内容，深入理解
        paper_content = downlaod_and_read_arxiv_paper(query,most_relevant_paper['title'],most_relevant_paper['url'])
    except Exception as e:
        print(f"[simple_qa]Error invoking model to find most relevant paper: {e}")
        return "无法确定最相关的论文，请稍后再试。"
    
    ## step5. 回答问题
    chunk = []
    cnt = 1
    for i in range(len(relevant_search_results)):
        if i == most_relevant_index and paper_content is not None:
            continue
        doc = relevant_search_results[i]
        chunk.append(f"Index [{cnt}]： title：{doc['title']}，cotent：{doc['content']}\n")
        cnt += 1
    if paper_content is not None:
        chunk.append(f"Index [{cnt}]： title：{most_relevant_paper['title']}，content：{paper_content}\n")

    search_answer_prompt = search_answer_prompt_template_en.format(
        query=query,
        relevant_docs="\n".join(chunk)
    )
    try:
        llm_answer = deepseek_r1.invoke(search_answer_prompt)
    except Exception as e:
        print(f"[simple_qa]Error invoking model: {e}")
        return "回答问题时发生错误，请稍后再试。"
    print('[simple_qa]llm_answer = ', llm_answer.content)
    return llm_answer.content



import re
from time import sleep
def generate_subtasks(llm_response):
    # 提取子任务
    subtasks = re.findall(r'#(\d+)#\s*(.+)', llm_response.strip())
    # 按顺序排序并去重
    subtasks = sorted(subtasks, key=lambda x: int(x[0]))
    unique_tasks = {}
    for idx, task in subtasks:
        if task not in unique_tasks:
            unique_tasks[task] = None
    # 返回任务列表
    return list(unique_tasks.keys())

def tokenize_mixed(text):
    # 如果包含中文字符，用 jieba 分词；否则按空格 split
    if re.search(r'[\u4e00-\u9fa5]', text):
        return [w for w in jieba.cut(text) if w.strip()]
    else:
        return text.lower().split()
    
def get_similar_topk_indices(query, anchor_texts, top_texts=20):
    tokenized_corpus = [tokenize_mixed(text) for text in anchor_texts]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = tokenize_mixed(query)
    top_texts = bm25.get_top_n(tokenized_query, anchor_texts, n=top_texts)
    topk_indices = [anchor_texts.index(text) for text in top_texts]
    return topk_indices



async def get_webpage_content(url,if_text_only=True):
    content_filter = PruningContentFilter(
        threshold=0.48,
        threshold_type="fixed",
        min_word_threshold=0
    )
    # Config makedown generator
    md_generator = DefaultMarkdownGenerator(
        content_filter=content_filter
    )
    if if_text_only:
        run_config = CrawlerRunConfig(
            # 20 seconds page timeout
            page_timeout=20000,

            # Filtering
            word_count_threshold=10,
            excluded_tags=["nav", "footer", "aside", "header", "script", "style", "iframe", "meta"],
            exclude_external_links=True,
            exclude_internal_links=True,
            exclude_social_media_links=True,
            exclude_external_images=True,
            only_text=True,

            # Markdown generation
            markdown_generator=md_generator,

            # Cache
            cache_mode=CacheMode.BYPASS
        )
    else:
        run_config = CrawlerRunConfig(
            page_timeout=20000,

            # 保留链接相关过滤
            word_count_threshold=10,
            excluded_tags=["nav", "footer", "aside", "header", "script", "style", "iframe", "meta"],

            # 👇 修改这些为 False 来保留链接
            exclude_external_links=False,
            exclude_internal_links=False,
            exclude_social_media_links=True,

            # ❌ 关闭 only_text 模式，否则仍会过滤掉链接
            only_text=False,  # 必须设为 False 才能保留链接和结构

            # Markdown generation
            markdown_generator=md_generator,
            # Cache
            cache_mode=CacheMode.BYPASS
        )
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )

        webpage_text = result.markdown.fit_markdown # 不一定需要fit

        # Clean up the text
        cleaned_text = webpage_text.replace("undefined", "")
        cleaned_text = re.sub(r'(\n\s*){3,}', '\n\n', cleaned_text)
        cleaned_text = re.sub(r'[\r\t]', '', cleaned_text)
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        cleaned_text = re.sub(r'^\s+|\s+$', '', cleaned_text, flags=re.MULTILINE)
        return result,cleaned_text.strip()

    except Exception as e:
        print(f"Error: {e}")
        return None
    

async def extract_all_links(url):
    async with async_playwright() as p:
        # 启动浏览器（headless=False 可以看到浏览器，调试用；正式用 headless=True）
        browser = await p.chromium.launch(headless=True)  # 可改为 False 查看过程
        page = await browser.new_page()
        
        # 设置 User-Agent（更像真实浏览器）
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        
        print(f"🔍 正在访问: {url}")
        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")  # 等待页面加载完成
        except Exception as e:
            print(f"❌ 页面加载失败: {e}")
            await browser.close()
            return []

        print("✅ 页面加载完成，正在提取所有链接...")
        
        # 使用 JavaScript 提取所有 <a href> 链接，并转换为绝对路径
        links = await page.evaluate('''() => {
            const anchors = Array.from(document.querySelectorAll('a[href]'));
            return anchors.map(a => {
                try {
                    // 浏览器自动解析为绝对 URL
                    const url = new URL(a.href, window.location.origin);
                    return {
                        url: url.href,
                        text: a.innerText.trim().replace(/\\s+/g, ' '),  // 清理多余空格
                        title: a.title || '',
                        class: a.className || '',
                        parentClass: a.parentElement?.className || ''
                    };
                } catch (e) {
                    return null;  // 忽略非法 URL
                }
            }).filter(Boolean);  // 去掉 null
        }''')

        await browser.close()
        print(f"✅ 共提取到 {len(links)} 个链接")
        return links


DOWNLOAD_DIR = Path("./")

# 文件类型映射：扩展名 -> 类型
EXTENSION_MAP = {
    '.pdf': 'pdf',
    '.docx': 'docx',
    '.doc': 'doc',
    '.xlsx': 'excel',
    '.xls': 'excel',
    '.csv': 'csv',
    '.txt': 'txt',
    '.json': 'json',
    '.md': 'txt'
}

# Content-Type 映射
CONTENT_TYPE_MAP = {
    'application/pdf': 'pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.ms-excel': 'excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'excel',
    'text/csv': 'csv',
    'text/plain': 'txt',
    'application/json': 'json',
    'text/markdown': 'txt'
}

# User-Agent（避免被反爬）
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

# ----------------------------
# 工具函数
# ----------------------------
def get_file_type_from_url(url: str) -> str:
    """从 URL 路径判断文件类型"""
    parsed = urlparse(url)
    path = parsed.path.lower().strip()
    ext = os.path.splitext(path)[1]
    return EXTENSION_MAP.get(ext)


def get_file_type_from_content_type(url: str) -> Optional[str]:
    """通过 HEAD 请求获取 Content-Type 判断文件类型"""
    try:
        response = requests.head(url, allow_redirects=True, headers=HEADERS, timeout=10)
        content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()
        return CONTENT_TYPE_MAP.get(content_type)
    except Exception as e:
        print(f"HEAD request failed for {url}: {e}")
        return None


def download_file(url: str, filename: str = None) -> Optional[Path]:
    """下载文件到本地"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # 自动推断文件名
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename or '.' not in filename:
                filename = "downloaded_file"

        file_path = DOWNLOAD_DIR / filename
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        print(f"Download failed for {url}: {e}")
        return None


# ----------------------------
# 各类文件提取函数
# ----------------------------
def extract_pdf_markdown(url: str, referer: str = None) -> Tuple[str, str]:
    """使用 pdf4llm 提取 PDF 内容为 Markdown 和 Text"""
    file_path = download_file(url)
    # 如果下载失败，尝试用 curl 下载
    if not file_path:
        file_path = download_pdf_with_curl(url, refer_url=referer, output_path="downloaded_report.pdf")
    if not file_path:
        return "", ""

    try:
        # 使用 pdf4llm 转 Markdown（保留结构）
        md_text = pdf4llm.to_markdown(str(file_path))

        # 清理文本（去除多余空行等）
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', md_text)
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        cleaned_text = cleaned_text.strip()

        return cleaned_text, cleaned_text  # Markdown 和 Text 一样
    except Exception as e:
        print(f"Failed to extract PDF {url}: {e}")
        return "", ""


def extract_excel_markdown(url: str) -> Tuple[str, str]:
    """提取 Excel 文件内容为 Markdown 表格 + 纯文本"""
    file_path = download_file(url)
    if not file_path:
        return "", ""

    try:
        df = pd.read_excel(file_path)
        md_table = df.to_markdown(index=False) if hasattr(df, 'to_markdown') else str(df)
        text = df.to_string(index=False)

        return md_table, text
    except Exception as e:
        print(f"Failed to read Excel {url}: {e}")
        return "", ""


def extract_csv_markdown(url: str) -> Tuple[str, str]:
    """提取 CSV 文件内容为 Markdown 表格 + 纯文本"""
    file_path = download_file(url)
    if not file_path:
        return "", ""

    try:
        df = pd.read_csv(file_path)
        md_table = df.to_markdown(index=False) if hasattr(df, 'to_markdown') else str(df)
        text = df.to_string(index=False)

        return md_table, text
    except Exception as e:
        print(f"Failed to read CSV {url}: {e}")
        return "", ""


def extract_txt_markdown(url: str) -> Tuple[str, str]:
    """提取 TXT 文件内容"""
    file_path = download_file(url)
    if not file_path:
        return "", ""

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        # 简单清理
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()

        return text, text
    except Exception as e:
        print(f"Failed to read TXT {url}: {e}")
        return "", ""


# ----------------------------
# 主函数：智能提取内容
# ----------------------------
async def get_content_from_url(
    url: str,
    referer: str = None,
    if_text_only: bool = True
) -> Tuple[Optional[dict], str, str]:
    """
    智能判断 URL 类型并提取内容
    返回: (crawl_result, markdown_text, plain_text)
    """
    url = url.strip()
    if referer and not url.startswith('http'):
        url = requests.compat.urljoin(referer, url)
    print(f"Processing URL: {url}")

    # 判断文件类型
    file_type = get_file_type_from_url(url)
    if not file_type:
        file_type = get_file_type_from_content_type(url)
        if not file_type:
            print("Unknown file type, treating as HTML page.")
            file_type = "html"

    print(f"Detected file type: {file_type}")

    # 分发处理
    if file_type == "html":
        # ✅ 直接 await！不要用 loop.run_until_complete
        src_res, text = await get_webpage_content(url, if_text_only=if_text_only)
        return src_res,text  # 注意：你原函数返回3个值，但只给了2个

    elif file_type == "pdf":
        # ✅ CPU 密集型任务用 run_in_executor
        loop = asyncio.get_event_loop()
        md, text = await loop.run_in_executor(None, extract_pdf_markdown, url, referer)
        return md, md

    elif file_type == "excel":
        loop = asyncio.get_event_loop()
        md, text = await loop.run_in_executor(None, extract_excel_markdown, url)
        return md, md

    elif file_type == "csv":
        loop = asyncio.get_event_loop()
        md, text = await loop.run_in_executor(None, extract_csv_markdown, url)
        return md, md

    elif file_type == "txt":
        loop = asyncio.get_event_loop()
        md, text = await loop.run_in_executor(None, extract_txt_markdown, url)
        return md, md

    else:
        print(f"Unsupported file type: {file_type}")
        return None, "", ""



async def get_relevant_links(user_query, url, links=None):
    if links is None:
        links = await extract_all_links(url)
    url_links = [x['text']+' ' +x['title'] +' ' + x['url'].split('/')[-1] for x in links]
    similar_internal_indices = get_similar_topk_indices(user_query, url_links, top_texts=50)
    all_candidates = [links[i] for i in similar_internal_indices]
    
    find_most_relevant_url_prompt = find_most_relevant_url_prompt_template.format(
        query=user_query,
        urls="\n".join([f"{idx} - {item['text']}, URL: {item['url'].split('/')[-1]}" for idx, item in enumerate(all_candidates)])
    )
    most_relevant_url_response = qwen_flash.invoke(find_most_relevant_url_prompt)
    # 处理返回的结果，是一个逗号分隔的字符串，如果有的话，取出数字
    print(most_relevant_url_response.content)
    most_relevant_indices = []
    if most_relevant_url_response.content:
        parts = most_relevant_url_response.content.split(',')
        for part in parts:
            part = part.strip()
            if part.isdigit():
                idx = int(part)
                if 0 <= idx < len(all_candidates):
                    most_relevant_indices.append(idx)
    if len(most_relevant_indices) == 0:
        print("No relevant URL found.")
        return None
    most_relevant_url_list = [all_candidates[i] for i in most_relevant_indices]
    # print("Most relevant URLs:")
    # for item in most_relevant_url_list:
    #     print(f"🔗 {item['text']} -> {item['url']}")
    return most_relevant_url_list



# 点击链接，获取内容，dfs的形式，最多可以2层，refer_url是上一级的url
# 进入网页详细search and click

async def dfs_click_url_financial(user_query, current_url, refer_url, current_depth, max_depth, visited_urls, context=""):
    if current_depth > max_depth or current_url in visited_urls:
        return 'no', None

    visited_urls.add(current_url)
    print(f"dfs Depth {current_depth}: Visiting {current_url}")

    # ✅ 直接 await 异步函数
    md_container, text_content = await get_content_from_url(current_url, referer=refer_url, if_text_only=False)

    check_answer_prompt = full_answer_generation_template_en.format(
        task=user_query,
        references=str(text_content[:8000])
    )
    check_answer_response = qwen_flash.invoke(check_answer_prompt)
    print(check_answer_response.content)

    try:
        json_result = json.loads(check_answer_response.content.strip().replace("```json", "").replace("```", "").strip('`'))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        json_result = {"finished": "no", "content": check_answer_response.content}

    print(json_result)

    if json_result.get('finished', 'no') == 'yes':
        print("Final Answer:")
        print(json_result.get('content', ''))
        return 'yes', json_result.get('content', '')
    else:
        if json_result.get('content', ''):
            if len(json_result.get('content', '')) > 5:
                context += json_result.get('content', '')

        # ✅ await 异步函数
        links_in_page = await extract_all_links(current_url)
        relevant_links = []
        if links_in_page:
            relevant_links = await get_relevant_links(user_query, current_url,links_in_page)

        if not relevant_links:
            return 'no', context

        for link in relevant_links:
            # ✅ 递归调用也是 async，必须 await
            status, tmp_res = await dfs_click_url_financial(
                user_query, link['url'], current_url, current_depth + 1, 
                max_depth, visited_urls, context
            )
            if status == 'yes':
                return 'yes', tmp_res
            elif tmp_res:
                context += tmp_res

        return 'no', context



async def dfs_click_url(user_query, current_url, refer_url, current_depth, max_depth, visited_urls, context=""):
    if current_depth > max_depth or current_url in visited_urls:
        return 'no', None

    visited_urls.add(current_url)
    print(f"dfs Depth {current_depth}: Visiting {current_url}")

    # ✅ 直接 await 异步函数
    md_container, text_content = await get_content_from_url(current_url, referer=refer_url, if_text_only=False)

    check_answer_prompt = full_answer_generation_template_en.format(
        task=user_query,
        references=str(text_content[:5000])
    )
    check_answer_response = qwen_flash.invoke(check_answer_prompt)
    print(check_answer_response.content)

    try:
        json_result = json.loads(check_answer_response.content.strip().replace("```json", "").replace("```", "").strip('`'))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        json_result = {"finished": "no", "content": check_answer_response.content}

    print(json_result)

    if json_result.get('finished', 'no') == 'yes':
        print("Final Answer:")
        print(json_result.get('content', ''))
        return 'yes', json_result.get('content', '')
    else:
        if json_result.get('content', ''):
            if len(json_result.get('content', '')) > 5:
                context += json_result.get('content', '')

        # ✅ await 异步函数
        links_in_page = await extract_all_links(current_url)
        relevant_links = []
        if links_in_page:
            relevant_links = await get_relevant_links(user_query, current_url)

        if not relevant_links:
            return 'no', context

        for link in relevant_links:
            # ✅ 递归调用也是 async，必须 await
            status, tmp_res = await dfs_click_url(
                user_query, link['url'], current_url, current_depth + 1, 
                max_depth, visited_urls, context
            )
            if status == 'yes':
                return 'yes', tmp_res
            elif tmp_res:
                context += tmp_res

        return 'no', context


####### 百度搜索的
# 计算相似度，取top k的文档
def get_top_k_search_results(search_result_list, rewrite_vector,search_np_vectors,top_k=10):
    if len(search_result_list) > top_k:
        # 超过top_k条，调用top K算法
        similarities = cosine_similarity(rewrite_vector.reshape(1, -1), search_np_vectors)
        top_k_indices = similarities[0].argsort()[-top_k:][::-1]
        return [search_result_list[i] for i in top_k_indices]
    else:
        return search_result_list


def baidu_search(rewrite_query,top_k=20):
    search_result_list = []
    print('[baidu_search]search_query = ',rewrite_query)
    url = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"
    headers = {
            "Authorization": "Bearer " + BAIDU_KEY,
            "Content-Type": "application/json"
    }

    data = {
        "resource_type_filter": [{"type": "web", "top_k": top_k}], # 返回前多少条消息
    "search_recency_filter": "semiyear"
    }

    data["messages"] = [
        {
            "content": rewrite_query,  # 改写后的问题
            "role": "user"
        }
    ]
    response = requests.post(url, headers=headers, json=data)
    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功，处理返回的数据
        print(f"[baidu_search]Response: {response.json()}")
    else:
        # 请求失败，打印错误信息
        print(f"[baidu_search]!Error: {response.status_code}, Response: {response.text}")
        return []

    returned_search_results = response.json()

    try:
        print('[baidu_search]搜索到相关文档{}个'.format(len(returned_search_results['references'])))
        for item in returned_search_results['references']:
            search_result_list.append({
                'url': item['url'],
                'title': item['title'],
                'content': item['content']
            })
    except Exception as e:
        print(f"[baidu_search]Error parsing search results: {e}")
    return search_result_list


async def download_and_read_html(query, url):
    # ✅ 直接 await
    web_page_markdown, web_page_text = await get_webpage_content(url, if_text_only=True)
    
    # 回答问题
    answer_prompt_filled = search_answer_prompt_template_en.format(
        query=query,
        relevant_docs=web_page_text
    )
    try: 
        answer_result = deepseek_v3.invoke(answer_prompt_filled)
        print('[download_and_read_html]answer_result = ', answer_result.content)
        return answer_result.content
    except Exception as e:
        print(f"[download_and_read_html]Error invoking model to answer question: {e}")
        return "回答问题时发生错误，请稍后再试。"


async def simple_qa_en_baidu_financial(query,max_search_num=10):
    need_search = True
    print('[simple_qa]original query = ',query)
    search_rewrite_prompt = search_rewrite_template_financial.format(
        date=datetime.now().strftime("%Y-%m-%d"),
        query=query
    )

    ##  step1. 问题改写
    rewrite_result = deepseek_v3.invoke(search_rewrite_prompt)
    print('[simple_qa]rewrite query = ',rewrite_result.content)
    
    try:
        json_match = re.search(r'```json\n(.*?)\n```', rewrite_result.content, re.DOTALL)
        json_str = json_match.group(1)
        search_query = json.loads(json_str)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        search_query = {'is_change': True, 'query_rewrite': query} # 兜底
    print(f"[simple_qa]rewrite search_query = {search_query['query_rewrite']}")

    ## step2. 进行搜索或者从本地数据库中获取信息
    search_result_list = baidu_search(search_query['query_rewrite'],top_k=20)
    #search_result_list是{ 'url': item['url'], 'title': item['title'], 'content': item['content'] }格式
    if len(search_result_list) == 0:
        print("[simple_qa]No search results found.[baidu_search]error!")
        return "没有找到相关的搜索结果，请尝试更换问题或重试。"

    ## step3. 获取最相关文档
    if need_search and len(search_result_list) > max_search_num:  # 如果搜索结果超过10条，选出top 10最相关的
        # 分别获取rewrite_result和search_result_list的向量，调用get_text_embedding函数
        rewrite_vector = get_text_embedding(search_query['query_rewrite'])
        search_vectors = [get_text_embedding(item['title']+' '+item['content']) for item in search_result_list]
        if rewrite_result is None or search_vectors is None:
            print("[simple_qa]Error: Failed to get embeddings for rewrite query or search results.")
            return "无法获取相关的搜索结果，请稍后再试。"
        # search_vectors变成numpy数组
        search_np_vectors = np.array(search_vectors) # N个1024维度向量
        relevant_search_results = get_top_k_search_results(search_result_list, rewrite_vector, search_np_vectors, top_k=max_search_num)
    else:
        relevant_search_results = search_result_list

    print(f"[simple_qa]relevant_search_results\n {relevant_search_results}")

    ## step4 寻找最相关的2份网页，仔细阅读内容
    chunk = []
    for i in range(len(relevant_search_results)):
        doc = relevant_search_results[i]
        chunk.append(f"Document {i+1}： title：{doc['title']}，cotent：{doc['content']}\n")
    find_most_relevant_paper_prompt_filled = find_most_relevant_html_prompt_template_financial.format(
        query=query,
        search_results="\n".join(chunk)
    )
    # 最相关的2份网页，进入网页仔细阅读内容，其他的只使用snippet
    try: 
        most_relevant_html_result = deepseek_v3.invoke(find_most_relevant_paper_prompt_filled)
        print('[simple_qa]most_relevant_html_result = ', most_relevant_html_result.content)
        # 解析返回的index
        most_relevant_indices = []
        if most_relevant_html_result.content:
            parts = most_relevant_html_result.content.split(',')
            for part in parts:
                part = part.strip()
                if part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(relevant_search_results):
                        most_relevant_indices.append(idx)
        print(f"[simple_qa]most_relevant_index = {most_relevant_indices}")
        most_relevant_html_list = [relevant_search_results[i] for i in most_relevant_indices]
        # 下载并且进入该网页，理解该网页的内容
        html_content_list = [] # 回答的答案
        for i in range(len(most_relevant_html_list)):
            doc = most_relevant_html_list[i]
            visited = set() # 记录已经访问过的url
            status, sc_answer = await dfs_click_url_financial(query, doc['url'], doc['url'], 1, 2, visited)
            html_content_list.append(sc_answer)
    except Exception as e:
        print(f"[simple_qa]Error invoking model to find most relevant paper: {e}")
        return "无法确定最相关的网页内容，请稍后再试。"
    
    ## step5. 回答问题
    chunk = []
    cnt = 1
    for i in range(len(relevant_search_results)):
        if i in most_relevant_indices and len(html_content_list)>0:
            continue
        doc = relevant_search_results[i]
        chunk.append(f"Index [{cnt}]： title：{doc['title']}，cotent：{doc['content']}\n")
        cnt += 1
    for i in range(len(html_content_list)):
        html_content = html_content_list[i]
        chunk.append(f"Index [{cnt}]： content：{html_content}\n")
        cnt += 1

    search_answer_prompt = search_answer_prompt_template_en.format(
        query=query,
        relevant_docs="\n".join(chunk)
    )
    try:
        llm_answer = deepseek_v3.invoke(search_answer_prompt)
    except Exception as e:
        print(f"[simple_qa]Error invoking model: {e}")
        return "回答问题时发生错误，请稍后再试。"
    print('[simple_qa]llm_answer = ', llm_answer.content)
    return llm_answer.content




# 支持简单的问答系统
async def simple_qa_en_baidu(query,max_search_num=10):
    need_search = True
    print('[simple_qa]original query = ',query)
    search_rewrite_prompt = search_rewrite_template_en.format(
        date=datetime.now().strftime("%Y-%m-%d"),
        query=query
    )

    ##  step1. 问题改写
    rewrite_result = deepseek_v3.invoke(search_rewrite_prompt)
    print('[simple_qa]rewrite query = ',rewrite_result.content)
    
    try:
        json_match = re.search(r'```json\n(.*?)\n```', rewrite_result.content, re.DOTALL)
        json_str = json_match.group(1)
        search_query = json.loads(json_str)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        search_query = {'is_change': True, 'query_rewrite': query} # 兜底
    print(f"[simple_qa]rewrite search_query = {search_query['query_rewrite']}")

    ## step2. 进行搜索或者从本地数据库中获取信息
    search_result_list = baidu_search(search_query['query_rewrite'],top_k=20)
    #search_result_list是{ 'url': item['url'], 'title': item['title'], 'content': item['content'] }格式
    if len(search_result_list) == 0:
        print("[simple_qa]No search results found.[baidu_search]error!")
        return "没有找到相关的搜索结果，请尝试更换问题或重试。"

    ## step3. 获取最相关文档
    if need_search and len(search_result_list) > max_search_num:  # 如果搜索结果超过10条，选出top 10最相关的
        # 分别获取rewrite_result和search_result_list的向量，调用get_text_embedding函数
        rewrite_vector = get_text_embedding(search_query['query_rewrite'])
        search_vectors = [get_text_embedding(item['title']+' '+item['content']) for item in search_result_list]
        if rewrite_result is None or search_vectors is None:
            print("[simple_qa]Error: Failed to get embeddings for rewrite query or search results.")
            return "无法获取相关的搜索结果，请稍后再试。"
        # search_vectors变成numpy数组
        search_np_vectors = np.array(search_vectors) # N个1024维度向量
        relevant_search_results = get_top_k_search_results(search_result_list, rewrite_vector, search_np_vectors, top_k=max_search_num)
    else:
        relevant_search_results = search_result_list

    print(f"[simple_qa]relevant_search_results\n {relevant_search_results}")

    ## step4 寻找最相关的2份网页，仔细阅读内容
    chunk = []
    for i in range(len(relevant_search_results)):
        doc = relevant_search_results[i]
        chunk.append(f"Document {i+1}： title：{doc['title']}，cotent：{doc['content']}\n")
    find_most_relevant_paper_prompt_filled = find_most_relevant_html_prompt_template.format(
        query=query,
        search_results="\n".join(chunk)
    )
    # 最相关的2份网页，进入网页仔细阅读内容，其他的只使用snippet
    try: 
        most_relevant_html_result = deepseek_v3.invoke(find_most_relevant_paper_prompt_filled)
        print('[simple_qa]most_relevant_html_result = ', most_relevant_html_result.content)
        # 解析返回的index
        most_relevant_indices = []
        if most_relevant_html_result.content:
            parts = most_relevant_html_result.content.split(',')
            for part in parts:
                part = part.strip()
                if part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(relevant_search_results):
                        most_relevant_indices.append(idx)
        print(f"[simple_qa]most_relevant_index = {most_relevant_indices}")
        most_relevant_html_list = [relevant_search_results[i] for i in most_relevant_indices]
        # 下载并且进入该网页，理解该网页的内容
        html_content_list = [] # 回答的答案
        for i in range(len(most_relevant_html_list)):
            doc = most_relevant_html_list[i]
            visited = set() # 记录已经访问过的url
            status, sc_answer = await dfs_click_url(query, doc['url'], doc['url'], 1, 2, visited)
            html_content_list.append(sc_answer)
    except Exception as e:
        print(f"[simple_qa]Error invoking model to find most relevant paper: {e}")
        return "无法确定最相关的网页内容，请稍后再试。"
    
    ## step5. 回答问题
    chunk = []
    cnt = 1
    for i in range(len(relevant_search_results)):
        if i in most_relevant_indices and len(html_content_list)>0:
            continue
        doc = relevant_search_results[i]
        chunk.append(f"Index [{cnt}]： title：{doc['title']}，cotent：{doc['content']}\n")
        cnt += 1
    for i in range(len(html_content_list)):
        html_content = html_content_list[i]
        chunk.append(f"Index [{cnt}]： content：{html_content}\n")
        cnt += 1

    search_answer_prompt = search_answer_prompt_template_en.format(
        query=query,
        relevant_docs="\n".join(chunk)
    )
    try:
        llm_answer = deepseek_v3.invoke(search_answer_prompt)
    except Exception as e:
        print(f"[simple_qa]Error invoking model: {e}")
        return "回答问题时发生错误，请稍后再试。"
    print('[simple_qa]llm_answer = ', llm_answer.content)
    return llm_answer.content



# 搜索金融信息
async def financial_search(question):
    # step1 任务改写
    task_rewrite_prompt = task_rewrite_template_financial.format(date=datetime.now().strftime("%Y-%m-%d"), task=question)
    task_rewrite_response = deepseek_v3.invoke(task_rewrite_prompt)
    print('改写后的问题：\n', task_rewrite_response.content)

    rewrite_query = task_rewrite_response.content

    # step2 子任务拆分
    sub_task_divide_prompt = sub_task_divide_template_financial.format(task=rewrite_query)

    sub_task_divide_response = qwen_flash.invoke(sub_task_divide_prompt)
    print("子任务拆解结果：\n", sub_task_divide_response.content)
    try:
        subtasks = generate_subtasks(sub_task_divide_response.content)
        print("子任务列表：\n", subtasks)
    except Exception as e:
        print("子任务生成失败：\n", e)
        # 这种情况下原始任务将被保留
        subtasks = [rewrite_query]
        if_success = 'no'
        
    # step3 子任务回答
    subtask_answer_list = []
    need_search = 0
    for subtask in subtasks:
        question_router_template = question_router_template_financial.format(subtask=subtask)
        question_router_response = qwen_flash.invoke(question_router_template)
        print('当前子问题为：\n', subtask)
        print('[问题路由]判断当前问题是否需要调用搜索引擎')
        if 'yes' in (question_router_response.content.strip()).lower():
            need_search = 1
            print(f"子任务 '{subtask}' 需要调用baidu搜索引擎获取实时信息。")
        else:
            need_search = 0
            print(f"子任务 '{subtask}' 可以直接回答，无需调用搜索引擎。")

        # 判断模型内部知识是否够用，不够调用搜索引擎
        if need_search==1:
            # 调用搜索引擎获取实时信息
            print('开始调用baidu搜索引擎获取实时信息...')
            try:
                search_answer = await simple_qa_en_baidu_financial(subtask,max_search_num=10)
                print(f"子任务 '{subtask}' 的搜索引擎回答为：\n", search_answer)
                subtask_answer_list.append(search_answer)
            except Exception as e:
                print(f"子任务 '{subtask}' 的搜索引擎调用失败：\n", e)
                subtask_answer_list.append("search_failed")
                if_success = 'no'
        else: # 直接回答
            try:
                direct_prompt = direct_answer_template_financial.format(subtask=subtask)
                direct_answer = deepseek_v3.invoke(direct_prompt)
                print(f"子任务 '{subtask}' 的直接回答为：\n", direct_answer)
                subtask_answer_list.append(direct_answer.content)
            except Exception as e:
                print(f"子任务 '{subtask}' 的直接回答调用失败：\n", e)
                subtask_answer_list.append("direct_answer_failed")
                if_success = 'no'

    # step4 汇总回答
    reference_list = []
    idx = 0
    for subtask in subtasks:
        ref_one = f"问题{idx+1}: {subtask}"
        ref_one += f"\n回答: {subtask_answer_list[idx].strip()}\n"
        reference_list.append(ref_one)
        idx += 1

    full_answer_generation_prompt = full_answer_generation_template_financial.format(
        task=question,
        references="\n".join(reference_list)
    )
    print("生成最终答案的提示语：\n", full_answer_generation_prompt)

    full_answer = qwen_flash.invoke(full_answer_generation_prompt)
    if full_answer:
        json_result = {}
        try:
            json_result = json.loads(full_answer.content.strip().replace("```json", "").replace("```", "").strip('`'))
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            json_result = {"finished": "no", "content": full_answer.content}
    print(f"生成的最终答案：\n{json_result['content']}")
    return json_result['content']


async def multi_step_qa_en(question):
    # step1 任务改写
    task_rewrite_prompt = task_rewrite_template_en.format(date=datetime.now().strftime("%Y-%m-%d"), task=question)
    task_rewrite_response = deepseek_v3.invoke(task_rewrite_prompt)
    print('改写后的问题：\n', task_rewrite_response.content)

    rewrite_query = task_rewrite_response.content

    # step2 子任务拆分
    sub_task_divide_prompt = sub_task_divide_template_en.format(task=rewrite_query)

    sub_task_divide_response = qwen_flash.invoke(sub_task_divide_prompt)
    print("子任务拆解结果：\n", sub_task_divide_response.content)
    try:
        subtasks = generate_subtasks(sub_task_divide_response.content)
        print("子任务列表：\n", subtasks)
    except Exception as e:
        print("子任务生成失败：\n", e)
        # 这种情况下原始任务将被保留
        subtasks = [rewrite_query]
        if_success = 'no'
        
    # step3 子任务回答
    subtask_answer_list = []
    need_search = 0
    for subtask in subtasks:
        question_router_template = question_router_template_en.format(subtask=subtask)
        question_router_response = qwen_flash.invoke(question_router_template)
        print('当前子问题为：\n', subtask)
        print('[问题路由]判断当前问题是否需要调用搜索引擎')
        if 'search' in (question_router_response.content.strip()).lower():
            need_search = 1
            print(f"子任务 '{subtask}' 需要调用baidu搜索引擎获取实时信息。")
        elif 'arxiv' in (question_router_response.content.strip()).lower():
            need_search = 2
            print(f"子任务 '{subtask}' 需要调用arxiv获取学术信息。")
        else:
            need_search = 0
            print(f"子任务 '{subtask}' 可以直接回答，无需调用搜索引擎。")

        # 判断模型内部知识是否够用，不够调用搜索引擎
        if need_search==1:
            # 调用搜索引擎获取实时信息
            print('开始调用baidu搜索引擎获取实时信息...')
            try:
                search_answer = await simple_qa_en_baidu(subtask,max_search_num=10)
                print(f"子任务 '{subtask}' 的搜索引擎回答为：\n", search_answer)
                subtask_answer_list.append(search_answer)
            except Exception as e:
                print(f"子任务 '{subtask}' 的搜索引擎调用失败：\n", e)
                subtask_answer_list.append("search_failed")
                if_success = 'no'
        elif need_search==2:
            print('开始调用arxiv获取学术信息...')
            # arXiv搜索需要慢一些
            sleep(1)
            try:
                # 下面是同步函数
                loop = asyncio.get_event_loop()
                # 直接调用同步函数
                arxiv_answer = await loop.run_in_executor(None, simple_qa_en_arxiv, subtask,10)
                #arxiv_answer = simple_qa_en_arxiv(subtask,max_search_num=10)
                print(f"子任务 '{subtask}' 的arxiv回答为：\n", arxiv_answer)
                subtask_answer_list.append(arxiv_answer)
            except Exception as e:
                print(f"子任务 '{subtask}' 的arxiv调用失败：\n", e)
                subtask_answer_list.append("arxiv_failed")
                if_success = 'no'

        else: # 直接回答
            try:
                direct_prompt = direct_answer_template_en.format(subtask=subtask)
                direct_answer = deepseek_v3.invoke(direct_prompt)
                print(f"子任务 '{subtask}' 的直接回答为：\n", direct_answer)
                subtask_answer_list.append(direct_answer.content)
            except Exception as e:
                print(f"子任务 '{subtask}' 的直接回答调用失败：\n", e)
                subtask_answer_list.append("direct_answer_failed")
                if_success = 'no'

    # step4 汇总回答
    reference_list = []
    idx = 0
    for subtask in subtasks:
        ref_one = f"问题{idx+1}: {subtask}"
        ref_one += f"\n回答: {subtask_answer_list[idx].strip()}\n"
        reference_list.append(ref_one)
        idx += 1

    full_answer_generation_prompt = full_answer_generation_template_en.format(
        task=question,
        references="\n".join(reference_list)
    )
    print("生成最终答案的提示语：\n", full_answer_generation_prompt)

    full_answer = qwen_flash.invoke(full_answer_generation_prompt)
    if full_answer:
        json_result = {}
        try:
            json_result = json.loads(full_answer.content.strip().replace("```json", "").replace("```", "").strip('`'))
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            json_result = {"finished": "no", "content": full_answer.content}
    print(f"生成的最终答案：\n{json_result['content']}")
    return json_result['content']



# 判断内容是否可以直接回答，还是需要尝试点击链接查看内容的prompt（搜索引擎可能可能搜到之后top10的里面，可以选择最有可能top_k包含相关信息的链接，进入链接去看信息）
if __name__ == "__main__":
    async def main1():
        max_click_num = 2 # 最多dfs的深度是3层
        user_query = "I want to know when is the submission deadline for CVPR 2025."
        refer_url = "https://cvpr.thecvf.com/Conferences/2025" # 起始的链接

        # 获取网页文本内容
        md_container, text_content = await get_content_from_url(refer_url,if_text_only=False)
        retrieved_text = ""

        # 如果网页内容已经包含答案，就不需要点击链接了，否则就需要点击链接
        check_answer_prompt = full_answer_generation_template_en.format(
            task=user_query,
            references=str(text_content[:3000])
        )

        check_answer_response = qwen_flash.invoke(check_answer_prompt)
        print(check_answer_response.content)


        json_result = {}
        try:
            json_result = json.loads(check_answer_response.content.strip().replace("```json", "").replace("```", "").strip('`'))
            retrieved_text += json_result.get('content','')
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            json_result = {"finished": "no", "content": check_answer_response.content}
            retrieved_text += check_answer_response.content
        print(json_result)

        most_relevant_url_list = await get_relevant_links(user_query,refer_url)

        final_answer = ""
        visited = set() # 全局变量，存储已经访问过的url，避免重复访问
        for item in most_relevant_url_list:
            status, answer = dfs_click_url(user_query, item['url'], refer_url, 1, max_click_num, visited)
            if status == 'yes':
                final_answer = answer
                break
            elif answer:
                retrieved_text += '\n' + str(answer)
            # 看一下answer里面是否包含最终答案，如果包含的话，就直接返回，不用再调用了，先尝试回答
            full_answer_generattion_prompt = full_answer_generation_template_en.format(
                task=user_query,
                references=retrieved_text
            )
            final_response = qwen_flash.invoke(full_answer_generattion_prompt)
            if final_response:
                print(final_response.content)
                json_result = {}
                try:
                    json_result = json.loads(final_response.content.strip().replace("```json", "").replace("```", "").strip('`'))
                except Exception as e:
                    print(f"Error parsing JSON: {e}")
                    json_result = {"finished": "no", "content": final_response.content}
                print(json_result)
                retrieved_text += '\n' + json_result.get('content','')
                if json_result.get('finished','no') == 'yes':
                    print("Final Answer:")
                    print(json_result.get('content',''))
                    final_answer = json_result.get('content','')
                    break
        print(final_answer)
    #asyncio.run(main1())


    # query = 'Latest research on web agent.'
    # output_response = simple_qa_en_arxiv(query)
    # print('\n最终回答：\n',output_response)

    # # 定义一个异步的主函数
    # async def main2():
    #     query = 'Tell me about the latest research on web agent.'
    #     answer = await simple_qa_en_baidu(query, max_search_num=5)
    #     print('\n最终回答：\n', answer)
    # asyncio.run(main2())
    
    # async def main3():
    #     question = 'Tell me the latest web agent research products such as DeepResearch provided by OpenAI, Grok and Tongyi.'
    #     answer = await multi_step_qa_en(question)
    #     print('\n最终回答：\n', answer)
    # asyncio.run(main3())

    async def main4():
        question = '今年暑期外卖大战之后，外卖上，饿了么市场份额高还是美团市场份额高？'
        answer = await multi_step_qa_en(question)
        print('\n最终回答：\n', answer)
    asyncio.run(main4())

    
        
