import json
from datetime import datetime, timedelta

# 模拟搜索结果数据，使用上一步骤中收集到的新闻片段
MOCK_SEARCH_RESULTS = [
    {
        "title": "摩尔线程首次公开全功能GPU技术路线图",
        "snippet": "摩尔线程举行首届MUSA开发者大会，首次公开全功能GPU技术路线图，包括新一代GPU架构“花港”、夸娥万卡智算集群、AI算力本MTT AI BOOK等。",
        "url": "https://www.stcn.com/article/detail/3550271.html",
        "date": (datetime.now() - timedelta(hours=5)).isoformat()
    },
    {
        "title": "Nvidia's Profit Jumps 65% to $31.9 Billion. Is It Enough for Wall St.?",
        "snippet": "The company, which makes the computer chips essential to the artificial intelligence boom, reported a massive profit jump.",
        "url": "https://www.nytimes.com/spotlight/artificial-intelligence",
        "date": (datetime.now() - timedelta(hours=10)).isoformat()
    },
    {
        "title": "Google Releases Gemini 3 Flash with 81.2% MMMU-Pro Score",
        "snippet": "Google launched Gemini 3 Flash, achieving a state-of-the-art 81.2% score on MMMU Pro (multimodal understanding benchmark) while being faster and cheaper.",
        "url": "https://www.msn.com/en-us/lifestyle/shopping/gemini-3-flash-arrives-as-google-s-fastest-ai-yet-now-default-across-search-and-apps/ar-AA1SxwxS?ocid=MicrosoftNewsApp-Win10",
        "date": (datetime.now() - timedelta(hours=23)).isoformat()
    },
    {
        "title": "As US battles China on AI, some companies choose Chinese",
        "snippet": "The January launch of Chinese company DeepSeek's high-performance, low-cost and open source 'R1' large language model (LLM) defied the perception that the best AI tech had to be from US.",
        "url": "https://www.gulfshorebusiness.com/news/national/as-us-battles-china-on-ai-some-companies-choose-chinese/article_1805b2ce-1e4c-55bc-bbf8-53f6b0a19600.html",
        "date": (datetime.now() - timedelta(hours=7)).isoformat()
    },
    {
        "title": "A new coffee shop opened in Silicon Valley",
        "snippet": "A great place for tech workers to meet and discuss the latest trends.",
        "url": "https://localnews.com/coffee",
        "date": (datetime.now() - timedelta(hours=1)).isoformat()
    },
    {
        "title": "Extremists are using AI voice cloning to supercharge propaganda",
        "snippet": "Researchers warn generative tools are helping militant groups grow their influence through AI voice cloning.",
        "url": "https://www.theguardian.com/technology/artificialintelligenceai",
        "date": (datetime.now() - timedelta(hours=15)).isoformat()
    },
]

def search_news(keywords: list, time_limit: str) -> list:
    """
    步骤 1: 模拟数据检索 (Retrieval)
    在实际产品中，这里会调用搜索引擎 API (如 Google Search API)
    """
    print(f"--- 步骤 1: 数据检索 ---")
    print(f"关键词: {keywords}, 时间限制: {time_limit}")
    # 模拟 API 调用延迟
    # time.sleep(1) 
    print(f"成功检索到 {len(MOCK_SEARCH_RESULTS)} 条新闻片段。")
    return MOCK_SEARCH_RESULTS

def filter_and_rank(raw_news: list) -> dict:
    """
    步骤 2: 模拟噪音过滤与排名 (Filtering & Ranking)
    在实际产品中，这里会调用 LLM API (LLM Call 1 & 2)，使用结构化 Prompt 进行过滤和评分。
    """
    print(f"\n--- 步骤 2: 噪音过滤与排名 (LLM Agentic Workflow) ---")
    
    # 模拟 LLM Call 1: 过滤低价值新闻 (如咖啡店新闻)
    filtered_news = [
        news for news in raw_news 
        if "coffee shop" not in news["title"] and "coffee shop" not in news["snippet"]
    ]
    print(f"LLM Call 1 (Filtering): 剔除 {len(raw_news) - len(filtered_news)} 条低价值新闻。")
    
    # 模拟 LLM Call 2: 根据重要性（模型、芯片、融资等）进行排名和摘要
    # 实际中，LLM会输出一个包含 'rank' 和 'summary' 的 JSON 列表
    ranked_data = [
        {
            "rank": 1, "title": "摩尔线程首次公开全功能GPU技术路线图",
            "summary": "国产GPU厂商摩尔线程发布新一代全功能GPU架构“花港”及AI芯片“华山”，算力密度提升50%，旨在支持万卡级智算集群。",
            "url": "https://www.stcn.com/article/detail/3550271.html",
            "type": "Top"
        },
        {
            "rank": 2, "title": "英伟达Q4利润飙升65%至319亿美元，AI芯片需求持续强劲",
            "summary": "英伟达（Nvidia）公布强劲财报，第四季度利润同比大增65%至319亿美元，显示AI芯片市场仍处于高速增长期。",
            "url": "https://www.nytimes.com/spotlight/artificial-intelligence",
            "type": "Top"
        },
        {
            "rank": 3, "title": "谷歌发布Gemini 3 Flash，速度更快、成本更低，性能超越Pro版",
            "summary": "谷歌推出轻量级模型Gemini 3 Flash，声称其在多项基准测试中表现优于Pro版，且具有更高的效率和更低的运行成本。",
            "url": "https://www.msn.com/en-us/lifestyle/shopping/gemini-3-flash-arrives-as-google-s-fastest-ai-yet-now-default-across-search-and-apps/ar-AA1SxwxS?ocid=MicrosoftNewsApp-Win10",
            "type": "Top"
        },
        {
            "rank": 4, "title": "DeepSeek R1等中国开源模型获美国企业青睐",
            "summary": "中国DeepSeek R1等高性能、低成本开源大模型正被美国公司采用，打破了AI技术仅源于美国的传统认知。",
            "url": "https://www.gulfshorebusiness.com/news/national/as-us-battles-china-on-ai-some-companies-choose-chinese/article_1805b2ce-1e4c-55bc-bbf8-53f6b0a19600.html",
            "type": "Quick"
        },
        {
            "rank": 5, "title": "AI语音克隆技术被极端组织用于宣传",
            "summary": "研究人员警告，生成式AI工具，特别是语音克隆技术，正被极端分子利用来制作宣传内容，助长其影响力。",
            "url": "https://www.theguardian.com/technology/artificialintelligenceai",
            "type": "Quick"
        },
    ]
    print(f"LLM Call 2 (Ranking & Summarizing): 确定 {len(ranked_data)} 条头条新闻和快讯。")
    
    return {"top_stories": ranked_data[:3], "quick_bites": ranked_data[3:]}

def draft_briefing(ranked_data: dict) -> str:
    """
    步骤 3: 模拟撰写简报 (Drafting)
    在实际产品中，这里会调用 LLM API (LLM Call 3 & 4)，使用严格的 Markdown 格式 Prompt 进行最终输出。
    """
    print(f"\n--- 步骤 3: 内容生成与格式化 (LLM Call 3 & 4) ---")
    
    today_date = datetime.now().strftime("%Y年%m月%d日")
    
    markdown_output = f"## 📅 AI Pulse - {today_date}\n\n"
    markdown_output += "### 🚀 头条关注 (Top Stories)\n"
    
    for i, item in enumerate(ranked_data["top_stories"], 1):
        markdown_output += f"\n{i}. **{item['title']}**\n"
        markdown_output += f"   * 📝 **摘要**: {item['summary']}\n"
        markdown_output += f"   * 🔗 **来源**: [点击阅读原文]({item['url']})\n"
        
    markdown_output += "\n### 🛠️ 行业快讯 (Quick Bites)\n"
    
    for i, item in enumerate(ranked_data["quick_bites"], 4):
        markdown_output += f"* [{i}] **{item['title']}**: {item['summary']} [🔗 来源]({item['url']})\n"
        
    markdown_output += "\n---\n"
    markdown_output += "💡 **Deep Dive**: 想了解更多？请直接回复新闻序号（例如：\"展开讲讲 1\"），我将为您深度解读。"
    
    print("成功生成最终 Markdown 简报。")
    return markdown_output

def main():
    """
    AI Pulse Briefing Generator 核心工作流
    """
    print("--- AI Pulse Briefing Generator 启动 ---")
    
    # 1. 数据检索
    raw_news = search_news(["Artificial Intelligence news", "LLM technology updates"], "last 24 hours")
    
    # 2. 噪音过滤与排名
    ranked_data = filter_and_rank(raw_news)
    
    # 3. 内容生成
    final_briefing = draft_briefing(ranked_data)
    
    print("\n" + "="*50)
    print("最终简报内容:")
    print(final_briefing)
    print("="*50)
    
    # 4. 保存最终结果
    with open("final_briefing.md", "w", encoding="utf-8") as f:
        f.write(final_briefing)
    print("\n简报已保存至 final_briefing.md 文件。")

if __name__ == "__main__":
    main()
