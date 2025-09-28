from constants import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


from playwright.sync_api import sync_playwright
import os

import os
from playwright.async_api import async_playwright

async def screenshot_with_playwright_async(html_file, selector, output_png):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()  # 自动适配，无需固定 viewport
        page = await context.new_page()

        try:
            abs_path = os.path.abspath(html_file)
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"文件不存在: {abs_path}")

            await page.goto(f"file://{abs_path}", wait_until="domcontentloaded")
            print("🎉 页面 DOM 已加载")

            # === 智能选择器逻辑 ===
            target_element = None
            used_selector = None

            # 情况 1：用户明确指定 selector 为 "canvas" 或包含 "canvas"
            if selector.strip().lower() in ["canvas", "canvas", "#mychart", ".chart", "body canvas"]:
                # 优先尝试 canvas
                target_element = await page.query_selector("canvas")
                if target_element:
                    used_selector = "canvas"
                    print("🖼️  检测到 canvas，优先使用")
                else:
                    print("❌ 指定使用 canvas，但未找到任何 <canvas> 元素")
                    raise Exception("未找到 <canvas> 元素")

            # 情况 2：用户指定了其他选择器（如 div、class 等）
            else:
                # 先尝试找 canvas
                canvas_element = await page.query_selector("canvas")
                if canvas_element:
                    target_element = canvas_element
                    used_selector = "canvas"
                    print("🖼️  检测到 <canvas>，优先截图 canvas")
                else:
                    # 没有 canvas，退回到用户指定的选择器
                    target_element = await page.query_selector(selector)
                    if target_element:
                        used_selector = selector
                        print(f"📦 未找到 canvas，使用备用选择器: {selector}")
                    else:
                        raise Exception(f"未找到元素: {selector}")

            if not target_element:
                raise Exception("未能找到任何可截图的元素")

            # ✅ 截图（自动裁剪到元素边界）
            await target_element.screenshot(path=output_png)
            print(f"✅ 截图成功: {output_png} (使用选择器: {used_selector})")

        except Exception as e:
            print(f"❌ 截图失败: {type(e).__name__}: {e}")
            raise
        finally:
            await browser.close()

async def screenshot_with_playwright_async_0(html_file, selector, output_png, viewport_width=1920, viewport_height=1080, scale_factor=2):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 可改为 False 看浏览器
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height},
            device_scale_factor=scale_factor,
            is_mobile=False
        )
        page = await context.new_page()

        try:
            abs_path = os.path.abspath(html_file)
            print(f"📁 加载文件: {abs_path}")
            
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"文件不存在: {abs_path}")

            # 关键修改：缩短等待条件 + 延长超时
            await page.goto(f"file://{abs_path}", timeout=20000, wait_until="domcontentloaded")
            print("🎉 页面 DOM 已加载")

            # 等待目标元素出现
            element = await page.wait_for_selector(selector, timeout=20000)
            print("🎯 元素已找到")

            await element.screenshot(path=output_png)
            print(f"✅ 截图成功: {output_png}")

        except Exception as e:
            print(f"❌ 失败: {type(e).__name__}: {e}")
            # 保存全页截图帮助调试
            # debug_png = output_png.replace(".png", "_debug_full.png")
            # await page.screenshot(path=debug_png)
            # print(f"📎 调试截图已保存: {debug_png}")
            raise
        finally:
            await browser.close()


def screenshot_with_playwright(html_file, selector, output_png, viewport_width=1920, viewport_height=1080, scale_factor=2):
    """
    使用 Playwright 截图指定元素，支持高清输出。
    
    :param html_file: 本地 HTML 文件路径
    :param selector: CSS 选择器，如 "#my-table", "table", ".figure"
    :param output_png: 输出 PNG 路径
    :param viewport_width: 视口宽度
    :param viewport_height: 视口高度
    :param scale_factor: 设备缩放因子（2=Retina，更清晰）
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height},
            device_scale_factor=scale_factor,  # 提高清晰度
            is_mobile=False
        )
        page = context.new_page()
        
        # 加载本地 HTML 文件
        abs_path = os.path.abspath(html_file)
        page.goto(f"file://{abs_path}")
        
        # 等待元素出现并截图
        try:
            element = page.wait_for_selector(selector, timeout=30000)
            # 截取元素区域
            element.screenshot(path=output_png)
            print(f"✅ 高清截图已保存: {output_png}")
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            # 调试：保存整个页面截图
            page.screenshot(path=output_png.replace(".png", "_full_debug.png"))
            raise
        finally:
            browser.close()

# def screenshot_element(html_file, element_tag, output_png):
#     """
#     截图并保存指定HTML元素的截图。
    
#     :param html_file: 要加载的本地HTML文件路径。
#     :param element_tag: 目标元素的标签名或CSS选择器。
#     :param output_png: 输出图片文件的路径。
#     """
#     chrome_options = Options()
#     # 设置为无头模式，即不打开浏览器窗口
#     chrome_options.add_argument("--headless")
#     # 确保窗口大小足够大以避免元素被裁剪
#     chrome_options.add_argument("--window-size=1920,10000")

#     # 使用webdriver-manager自动管理ChromeDriver
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     try:
#         # 加载本地HTML文件
#         abs_path = os.path.abspath(html_file)
#         driver.get(f"file://{abs_path}")
        
#         # 查找目标元素
#         # 如果是标签名，请直接使用 "tag name", "table"
#         # 如果是CSS选择器，请使用 "css selector", ".your-class-name"
#         element = driver.find_element("tag name", element_tag)
        
#         # 截取元素的截图
#         element.screenshot(output_png)
#         print(f"已保存元素截图: {output_png}")

#     finally:
#         driver.quit()


data_anylyse_prompt_template = """You're a Python data scientist. You are given a data analysis task to complete, and you will write Python code to solve it.

The input data and task are provided directly in the request. You do NOT have access to any CSV file or external dataset. All necessary data is included in the task description and should be defined directly in the code.

Rules you must follow:
- ALWAYS FORMAT YOUR RESPONSE IN MARKDOWN.
- RESPOND ONLY WITH A SINGLE PYTHON CODE BLOCK LIKE THIS:
  ```python
  [your code here]
  ```
- The code runs in a Jupyter notebook environment on E2B sandbox.
- Run all code in a single cell. Do not split into multiple cells.
- Define all data (e.g., lists, dictionaries, DataFrames) directly in the code. Do not use pd.read_csv, open, or file-based loading.
- Install packages only if necessary using !pip install package_name, but most common packages (pandas, numpy, matplotlib, scipy) are already preinstalled.
- For data analysis results (e.g., mean, correlation, regression coefficients), use print() to output them.
- EVERY print() statement MUST include a descriptive string explaining what is being printed. For example:
    print("Pearson correlation coefficient between X and Y:", corr_coef)
- DO NOT use print(result) alone — always describe the output.
- DO NOT generating plots becasue the environment does not support it. Instead, calculate and print key statistics or insights that would be derived from the plots.
- Ensure the code is self-contained, error-free, and completes the task.

Your task is to perform the following data analysis, the task and all necessary data are provided below:
{task}

Now please generate the Python code to perform the task:
"""

picture_gen_prompt_template = """You're a Python data scientist. You are given a data analysis task to complete, and you will write Python code to solve it.

The input data and task are provided directly in the request. You do NOT have access to any CSV file or external dataset. All necessary data is included in the task description and should be defined directly in the code.

Rules you must follow:
- ALWAYS FORMAT YOUR RESPONSE IN MARKDOWN.
- RESPOND ONLY WITH A SINGLE PYTHON CODE BLOCK LIKE THIS:
  ```python
  [your code here]
  ```
- The code runs in a Jupyter notebook environment on E2B sandbox.
- Run all code in a single cell. Do not split into multiple cells.
- You also have access to the filesystem and can read/write files. Display visualizations using matplotlib or any other visualization library directly in the notebook. Don't worry about saving the visualizations to a file.
- Install packages only if necessary using !pip install package_name, but most common packages (pandas, numpy, matplotlib, scipy) are already preinstalled.
- For data analysis results (e.g., mean, correlation, regression coefficients), use print() to output them.
- EVERY print() statement MUST include a descriptive string explaining what is being printed. For example:
    print("Pearson correlation coefficient between X and Y:", corr_coef)
- DO NOT use print(result) alone — always describe the output.
- Ensure the code is self-contained, error-free, and completes the task.

Your task is to perform the following task and all necessary data are provided below:
{task}

Now please generate the Python code to perform the task:
"""


code_check_template = """You are a code analysis tool. You are given a piece of Python code. You need to check if the code has any syntax errors or other issues that would prevent it from running successfully. If the code has no issues, respond with "GOOD". If there are issues, respond with "BAD".
Here is the code:{code}
"""

vlm_quality_check_prompt = """
You are a quality assurance specialist for data visualizations. Your task is to evaluate a generated image based on the original visualization request and general best practices. You must provide your evaluation in a **strictly structured JSON format** with no additional text or explanation.

### Original Visualization Task:
{task}

### Evaluation Criteria:
- **Clarity**: The chart should be clear, with text and data points easy to read.
- **Label Accuracy**: All axes, legends, and data series should have clear and accurate labels.
- **Appropriate Chart Type**: The chosen chart type must be suitable for the data and the task.
- **Data Accuracy**: The visualization must correctly represent the data (e.g., correct aggregation).
- **Color Use**: Colors should be appropriate and considerate of colorblind users.
- **Layout**: Elements should be properly spaced.
- **Title**: The chart should have a descriptive title.

### Output Format (MANDATORY):
You must respond **ONLY** with a valid JSON object. Do not include any other text, explanations, or markdown. The JSON object must have exactly the following structure:
```json
{{
  "result": "PASS" or "FAIL",
  "reason": "A very brief reason (1-2 sentences) if result is FAIL, otherwise 'Meets all requirements.'",
  "suggestions": "Specific, actionable suggestions for code improvement if result is FAIL, otherwise '[]'"
}}```
"""


# html_table_gen_template = """
# You are a helpful assistant that generates HTML tables with my given data.
# Generate a complete and self-contained HTML file that displays a clean, modern, and responsive data table. The table should be styled with internal CSS (inside a <style> tag in the <head>) to ensure it looks professional and is ready for screenshotting.

# Requirements:
# - Use semantic HTML: <table>, <thead>, <tbody>, <th>, <td>.
# - Include realistic sample data with at least 4 columns and 6 rows.
# - Apply modern styling: clean borders, alternating row colors, hover effects, proper padding, and a styled header (e.g., dark background with white text).
# - Make the table responsive (e.g., horizontal scroll on small screens or use of max-width).
# - Use a clean font (e.g., 'Segoe UI', Arial, sans-serif).
# - Center the table on the page with some margin.
# - Do NOT use external CSS files or frameworks (like Bootstrap). All CSS must be embedded inside <style>.
# - The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>).
# - No explanation, only output the HTML code.

# The task and the data is as follows:
# {task}

# Now generate the HTML code:
# """

html_table_gen_template = """
You are a helpful assistant that generates HTML tables with my given data.

Generate a complete and self-contained HTML file that displays a clean, modern, and responsive data table. The table should be styled with internal CSS (inside a <style> tag in the <head>) to ensure it looks professional and is ready for screenshotting.

Requirements:
- Use semantic HTML: <table>, <thead>, <tbody>, <th>, <td>.
- Include a clear and descriptive title **ABOVE** the table using <h2> (e.g., "商汤科技收入情况").
- DO NOT include the word "表：" or patterns like "表[table]：" in the title. Just use the natural name (e.g., "商汤科技收入情况", not "表：商汤科技收入情况").
- Include realistic sample data with at least 4 columns and 6 rows.
- Apply modern styling: clean borders, alternating row colors (zebra striping), hover effects, proper padding, and a styled header (e.g., dark background with white text).
- Make the table responsive by wrapping it in a container with max-width and overflow-x: auto if needed.
- Use a clean font (e.g., 'Segoe UI', Arial, sans-serif).
- Center the table and title on the page with appropriate margins.
- The ENTIRE PAGE BACKGROUND MUST BE PURE WHITE (#FFFFFF), and the body should have no margin or padding.
- The container around the table should be minimal and white, suitable for clean screenshots.
- DO NOT add any decorative elements, shadows, or colored backgrounds outside the table.
- Use internal CSS only (inside <style>). No external files or frameworks (like Bootstrap).
- The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>).
- Generate **only one table**. Do not create multiple tables or long scrolling content.
- No explanation, only output the HTML code.

The task and the data is as follows:
{task}

Now generate the HTML code:
"""


html_pic_gen_template = """
You are a helpful assistant that generates HTML charts from data.

Generate a complete and self-contained HTML file that renders a **single**, professional, clear, and insightful data visualization using Chart.js. The output must be a single HTML file that renders correctly in modern browsers and is optimized for high-quality screenshots.

Requirements:
- Use Chart.js via CDN: https://cdn.jsdelivr.net/npm/chart.js
- Create **exactly one chart** (bar, line, pie, etc.) that best fits the given data.
- Include a descriptive title above the chart (use <h2>)(e.g., "商汤科技收入情况").
- DO NOT include the word "图：" or patterns like "图[figure]：" in the title. Just use the natural name (e.g., "商汤科技收入情况", not "图：商汤科技收入情况").
- The chart must have labeled axes, a legend (if applicable), and a clean, modern appearance.
- Embed all styling with internal CSS (inside <style>) to ensure:
  - The **entire page background is pure white (#ffffff)**
  - No margin, padding, or borders on body
  - The chart is centered and has no extra elements
- Set the canvas to a fixed size: **800x400 pixels**
- Ensure the canvas background is white (set in Chart.js options)
- Include **realistic sample data** relevant to the task (e.g., monthly sales, categories)
- All code (HTML, CSS, JavaScript) must be in a single file — no external files
- The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>)
- **No explanations, comments, or extra text — only the complete HTML code**

Important:
- Generate **ONLY ONE CHART** — do not create multiple charts or long scrolling content
- Keep the output short, focused, and ideal for screenshotting

The task and the data is as follows:
{task}

Now generate the HTML code:
"""

# html_pic_gen_template = """
# You are a helpful assistant that generates HTML charts from data.

# Generate a complete and self-contained HTML file that renders a professional, clear, and insightful data visualization using Chart.js. The output must be a single HTML file that renders correctly in modern browsers and is optimized for high-quality screenshots.

# Requirements:
# - Use Chart.js (via CDN: https://cdn.jsdelivr.net/npm/chart.js) to create a bar chart or line chart.
# - Include a descriptive title above the chart.
# - The chart should have labeled axes, a legend (if applicable), and a clean, modern appearance.
# - Embed all styling with internal CSS (inside a <style> tag) to center the chart and set a pleasant layout.
# - Include realistic sample data (e.g., monthly sales, product categories).
# - Ensure the canvas has a fixed width and height (e.g., 800x400) for consistent screenshots.
# - All code (HTML, CSS, JavaScript) must be in a single file. No external files.
# - The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>).
# - No explanation, only output the HTML code.

# Your goal is to create a professional, insightful, and self-contained HTML document that makes the data easy to understand at a glance.

# The task and the data is as follows:
# {task}
# """


vlm_img_quality_check_prompt = """You are a quality assurance specialist for data visualizations. Your task is to evaluate a generated image based on the original visualization request and general best practices. You must provide your evaluation in a **strictly structured JSON format** with no additional text or explanation.

### Original Visualization Task:
{task}

### Evaluation Criteria:
- **Resolution & Sharpness**: The image must be clear, sharp, and not pixelated or blurry. Text and details should be easily readable.
- **Visual Element Sizing**: All visual elements must be appropriately sized for clarity:
    - **Fonts**: Axis labels, tick labels, legend text, and title must be large enough to read without zooming.
    - **Data Marks**: Bars in bar charts, points in scatter plots, lines in line charts, etc., must have sufficient thickness/width/size to be clearly visible and distinguishable. For example, bars should be wide enough to compare easily.
    - **Margins & Spacing**: Adequate margins and spacing between elements (e.g., between bars, around the plot) are necessary to prevent clutter.
- **Label Accuracy**: All axes, legends, and data series should have clear, accurate, and complete labels.
- **Appropriate Chart Type**: The chosen chart type must be suitable for the data and the task.
- **Data Accuracy**: The visualization must correctly represent the data (e.g., correct aggregation, proper scaling).
- **Color Use**: Colors should be appropriate, have good contrast, and be considerate of colorblind users. Avoid overly bright or clashing colors.
- **Layout & Composition**: The overall layout should be balanced and aesthetically pleasing. Key elements (title, axes, legend) should be well-placed and not obstruct the data.

### Output Format (MANDATORY):
You must respond **ONLY** with a valid JSON object. Do not include any other text, explanations, or markdown. The JSON object must have exactly the following structure:
```json
{{
  "result": "PASS" or "FAIL",
  "reason": "A very brief reason (1-2 sentences) if result is FAIL, otherwise 'Meets all requirements.'",
  "suggestions": "Specific, actionable suggestions for code improvement if result is FAIL, otherwise '[]'"
}}```"""


html_table_review_gen_template = """You are a helpful assistant that generates HTML tables with my given data.

Generate a complete and self-contained HTML file that displays a clean, modern, and responsive data table. The table should be styled with internal CSS (inside a <style> tag in the <head>) to ensure it looks professional and is ready for screenshotting.

Requirements:
- Use semantic HTML: <table>, <thead>, <tbody>, <th>, <td>.
- Include a clear and descriptive title **ABOVE** the table using <h2> (e.g., "商汤科技收入情况").
- DO NOT include the word "表：" or patterns like "表[table]：" in the title. Just use the natural name (e.g., "商汤科技收入情况", not "表：商汤科技收入情况").
- Include realistic sample data with at least 4 columns and 6 rows.
- Apply modern styling: clean borders, alternating row colors (zebra striping), hover effects, proper padding, and a styled header (e.g., dark background with white text).
- Make the table responsive by wrapping it in a container with max-width and overflow-x: auto if needed.
- Use a clean font (e.g., 'Segoe UI', Arial, sans-serif).
- Center the table and title on the page with appropriate margins.
- The ENTIRE PAGE BACKGROUND MUST BE PURE WHITE (#FFFFFF), and the body should have no margin or padding.
- The container around the table should be minimal and white, suitable for clean screenshots.
- DO NOT add any decorative elements, shadows, or colored backgrounds outside the table.
- Use internal CSS only (inside <style>). No external files or frameworks (like Bootstrap).
- The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>).
- Generate **only one table**. Do not create multiple tables or long scrolling content.
- No explanation, only output the HTML code.

The task and the data is as follows:
{task}

The previous code you generated is:
{pre_code}

You must review the VLM feedback of the screenshot of your generated HTML and update the code if necessary to better meet the requirements. No comments or explanations.
Visual Language Model (VLM) feedback of your generated HTML generated HTML:
{vlm_feedback}
"""

html_pic_review_gen_template = """
You are a helpful assistant that generates charts with my given data.

Generate a complete and self-contained HTML file that renders a professional, clear, and insightful data visualization using Chart.js. The output must be a single HTML file that renders correctly in modern browsers and is optimized for high-quality screenshots.

Requirements:
- Use Chart.js via CDN: https://cdn.jsdelivr.net/npm/chart.js
- Create **exactly one chart** (bar, line, pie, etc.) that best fits the given data.
- Include a descriptive title above the chart (use <h2>)(e.g., "商汤科技收入情况").
- DO NOT include the word "图：" or patterns like "图[figure]：" in the title. Just use the natural name (e.g., "商汤科技收入情况", not "图：商汤科技收入情况").
- The chart must have labeled axes, a legend (if applicable), and a clean, modern appearance.
- Embed all styling with internal CSS (inside <style>) to ensure:
  - The **entire page background is pure white (#ffffff)**
  - No margin, padding, or borders on body
  - The chart is centered and has no extra elements
- Set the canvas to a fixed size: **800x400 pixels**
- Ensure the canvas background is white (set in Chart.js options)
- Include **realistic sample data** relevant to the task (e.g., monthly sales, categories)
- All code (HTML, CSS, JavaScript) must be in a single file — no external files
- The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>)
- **No explanations, comments, or extra text — only the complete HTML code**

Your goal is to create a professional, insightful, and self-contained HTML document that makes the data easy to understand at a glance.
The task and the data is as follows:
{task}

The previous code you generated is:
{pre_code}

You must review the VLM feedback of the screenshot of your generated HTML and update the code if necessary to better meet the requirements. No comments or explanations.
Visual Language Model (VLM) feedback of your generated HTML:
{vlm_feedback}
"""

# html_pic_review_gen_template = """
# You are a helpful assistant that generates charts with my given data.

# Generate a complete and self-contained HTML file that renders a professional, clear, and insightful data visualization using Chart.js. The output must be a single HTML file that renders correctly in modern browsers and is optimized for high-quality screenshots.

# Requirements:
# - Use Chart.js (via CDN: https://cdn.jsdelivr.net/npm/chart.js) to create a bar chart or line chart.
# - Include a descriptive title above the chart.
# - The chart should have labeled axes, a legend (if applicable), and a clean, modern appearance.
# - Embed all styling with internal CSS (inside a <style> tag) to center the chart and set a pleasant layout.
# - Include realistic sample data (e.g., monthly sales, product categories).
# - Ensure the canvas has a fixed width and height (e.g., 800x400) for consistent screenshots.
# - All code (HTML, CSS, JavaScript) must be in a single file. No external files.
# - The output must be a full HTML document (include <!DOCTYPE html>, <html>, <head>, <body>).
# - No explanation, only output the HTML code.

# Your goal is to create a professional, insightful, and self-contained HTML document that makes the data easy to understand at a glance.
# The task and the data is as follows:
# {task}

# The previous code you generated is:
# {pre_code}

# You must review the VLM feedback of the screenshot of your generated HTML and update the code if necessary to better meet the requirements. No comments or explanations.
# Visual Language Model (VLM) feedback of your generated HTML generated HTML:
# {vlm_feedback}
# """

# 读取本地图片并转换为 base64
def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_string}"

##### 沙箱函数
## 沙箱函数
# def code_interpret(e2b_code_interpreter, code):
#     print("Running code interpreter...")
#     exec = e2b_code_interpreter.run_code(
#         code,
#         on_stderr=lambda stderr: print("[Code Interpreter]", stderr),
#         on_stdout=lambda stdout: print("[Code Interpreter]", stdout)
#     )

#     if exec.error:
#         print("[Code Interpreter ERROR]", exec.error)
#         return [-1, exec.error]
#     else:
#         return [0, exec.results]
    
def code_interpret(e2b_code_interpreter, code):
    print("Running code interpreter...")
    stdout_parts = []

    exec = e2b_code_interpreter.run_code(
        code,
        on_stderr=lambda stderr: print("[Code Interpreter STDERR]", stderr),
        on_stdout=lambda stdout: (
            print("[Code Interpreter STDOUT]", stdout),
            stdout_parts.append(str(stdout))  # ✅ 强制转为字符串
            # 或者更安全：.append(stdout.message) 如果是对象
        )
    )

    full_stdout = ''.join(stdout_parts)  # 现在没问题了

    if exec.error:
        return [-1, exec.error]
    else:
        return [0, full_stdout.strip()]

# def code_interpret(e2b_code_interpreter, code):
#     print("Running code interpreter...")
#     full_stdout = ""

#     exec = e2b_code_interpreter.run_code(
#         code,
#         on_stderr=lambda stderr: print("[Code Interpreter STDERR]", stderr),
#         on_stdout=lambda stdout: (print("[Code Interpreter STDOUT]", stdout), full_stdout.__iadd__(stdout))
#     )

#     if exec.error:
#         return [-1, exec.error]
#     else:
#         return [0,full_stdout.strip()]

    # if exec.error:
    #     return [-1, exec.error]
    # else:
    #     return [0, {
    #         "output": full_stdout.strip(),
    #         "results": exec.results  # 可能包含图像等
    #     }]

def upload_dataset(code_interpreter, local_path):
    print("Uploading dataset to Code Interpreter sandbox...")
    dataset_path = local_path

    if not os.path.exists(dataset_path):
        raise FileNotFoundError("Dataset file not found")

    try:
        with open(dataset_path, "rb") as f:
            remote_path = code_interpreter.files.write(dataset_path,f)

        if not remote_path:
            raise ValueError("Failed to upload dataset")

        print("Uploaded at", remote_path)
        return remote_path
    except Exception as error:
        print("Error during file upload:", error)
        raise error

def download_file(code_interpreter, remote_path, local_path):
    """
    从 E2B 沙箱下载文件到本地（兼容旧版 SDK）
    """
    try:
        content = code_interpreter.files.read(remote_path)  # 返回 str 或 bytes，取决于内容

        # 判断内容类型并选择写入模式
        if isinstance(content, bytes):
            # 如果是 bytes（如图片、PDF），用二进制写入
            with open(local_path, "wb") as f:
                f.write(content)
        else:
            # 如果是 str（如 CSV、TXT），用文本写入
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"文件下载成功: {local_path}")

    except Exception as e:
        print(f"下载失败: {e}")
        print(f"错误详情: {type(e).__name__}: {e}")


pattern = re.compile(
    r"```python\n(.*?)\n```", re.DOTALL
)  # Match everything in between ```python and ```
def match_code_blocks(llm_response):
    match = pattern.search(llm_response)
    if match:
        code = match.group(1)
        print(code)
        return code
    return ""

def chat_with_llm(e2b_code_interpreter, user_message, pre_code="",pre_error="", max_retries=1):
    print(f"\n{'='*50}\nUser message: {user_message}\n{'='*50}")
    if pre_code != "" and pre_error != "":
        new_user_message = f"""
        {user_message}
        
        The previous code you generated is:
        {pre_code}
        And it resulted in the following error:
        {pre_error}

        You need to carefully review the error message and fix the code accordingly. Give me the updated code. No comments or explanations.
        """
    else:
        new_user_message = user_message

    for attempt in range(max_retries + 1):
        messages = [
            {"role": "user", "content": new_user_message},
        ]
        if attempt>0:
            response_message = deepseek_v3.invoke(messages)
        else:
            response_message = qwen_plus.invoke(messages)
        print(f"Model response: {response_message.content}\n{'='*50}")
        python_code = match_code_blocks(response_message.content)
        if python_code != "":
            # 先进行语法校验
            code_check_result  = qwen_plus.invoke([{"role": "user", "content": code_check_template.format(code=python_code)}])
            if code_check_result.content == "GOOD":
                code_interpreter_results = code_interpret(e2b_code_interpreter, python_code)
                return code_interpreter_results,python_code
            else:
                print(f"Code syntax check failed, retrying... (attempt {attempt+1})")
        else:
            print(f"Failed to match any Python code in model's response {response_message}, retrying... (attempt {attempt+1})")
    print("All attempts failed.")
    return None, None



def chat_with_llm_after_vlm_check(e2b_code_interpreter, user_message,pre_code,vlm_feedback, max_retries=1):
    print(f"\n{'='*50}\nUser message: {user_message}\n{'='*50}")
    new_user_message = f"""
    {user_message}

    The previous code you generated is:
    {pre_code}

    Visual Language Model (VLM) feedback on the generated image:
    {vlm_feedback}

    Please review the VLM feedback and update the code if necessary to better meet the requirements. No comments or explanations.
    """

    for attempt in range(max_retries + 1):
        messages = [
            {"role": "user", "content": new_user_message},
        ]
        if attempt>0:
            response_message = deepseek_v3.invoke(messages)
        else:
            response_message = qwen_flash.invoke(messages)
        print(f"Model response: {response_message.content}\n{'='*50}")
        python_code = match_code_blocks(response_message.content)
        if python_code != "":
            # 先进行语法校验
            code_check_result  = qwen_flash.invoke([{"role": "user", "content": code_check_template.format(code=python_code)}])
            if code_check_result.content == "GOOD":
                code_interpreter_results = code_interpret(e2b_code_interpreter, python_code)
                return code_interpreter_results,python_code
            else:
                print(f"Code syntax check failed, retrying... (attempt {attempt+1})")
        else:
            print(f"Failed to match any Python code in model's response {response_message}, retrying... (attempt {attempt+1})")
    print("All attempts failed.")
    return []


def vlm_check_function(image_path,task):
    image_data = image_to_base64(image_path)
    vlm_response = client.chat.completions.create(
        model=qwen_vl_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": vlm_quality_check_prompt.format(task=task)},
                    {"type": "image_url", "image_url": {"url": image_data}},  # 使用 base64 数据
                ],
            }
        ],
        temperature=0
    )
    vlm_feedback = vlm_response.choices[0].message.content
    # 提取 JSON 字符串 (如果模型输出了 markdown 代码块)
    if vlm_feedback.startswith("```json") and vlm_feedback.endswith("```"):
        json_str = vlm_feedback[7:-3].strip() # 去掉 ```json 和 ```
    else:
        json_str = vlm_feedback.strip()

    try:
        evaluation = json.loads(json_str)
        if evaluation["result"] == "PASS":
            print("Visualization is approved!")
            # 可以进行后续操作
        else:
            print(f"Visualization failed: {evaluation['reason']}")
            print("Suggestions for improvement:")
            for suggestion in evaluation["suggestions"]:
                print(f"  - {suggestion}")
            vlm_feedback = f"Visualization failed: {evaluation['reason']}\nSuggestions for improvement:\n{evaluation['suggestions']}"
            # 将 evaluation 传递给 chat_with_llm_after_vlm_check 或类似函数进行代码修正
    except json.JSONDecodeError as e:
        print(f"Failed to parse VLM response as JSON: {e}")
    return vlm_feedback


def run_data_analysis(task, local_save_path, remote_save_path):
    with Sandbox.create(api_key=E2B_API_KEY) as code_interpreter:
        task_prompt = data_anylyse_prompt_template.format(task=task)

        code_results,python_code = chat_with_llm(
            code_interpreter,
            task_prompt
        )
        if code_results is not None and code_results[0]==0:  # 执行成功
            first_result = code_results[1][0]
            download_file(code_interpreter, remote_save_path, local_save_path) # 数据下载到本地
        else:
            print('代码执行失败，重试一次')
            code_results,python_code = chat_with_llm(
                code_interpreter,
                task_prompt,
                pre_code=python_code,
                pre_error=code_results[1].traceback,
                max_retries=2
            )
            if code_results is not None and code_results[0]==0:  # 执行成功
                first_result = code_results[1][0]
                download_file(code_interpreter, remote_save_path, local_save_path) # 数据下载到本地
            else:
                raise Exception("No code interpreter results")
