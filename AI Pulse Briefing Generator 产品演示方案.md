# AI Pulse Briefing Generator 产品演示方案

## 1. 产品概述 (Product Overview)

**产品名称:** AI Pulse Briefing Generator (脉冲简报生成器)
**目标:** 自动化生成高信噪比的每日 AI 科技新闻简报，模拟资深 AI 科技编辑的工作流程。
**核心价值:** 快速、精准地从海量信息中提取最有价值的 AI 行业动态（模型发布、重大融资、政策监管、开源突破），并以专业、简洁的格式呈现。

## 2. 技术架构 (Technical Architecture)

该 Demo 采用典型的 **RAG (Retrieval-Augmented Generation) + Agentic Workflow** 架构，核心逻辑由一个 Python 脚本 `generate_briefing.py` 实现，并通过多次调用 LLM API 来模拟复杂的决策和内容生成过程。

| 模块 | 职责 | 关键技术/模拟工具 |
| :--- | :--- | :--- |
| **1. 数据检索 (Retrieval)** | 根据关键词和时间限制，从互联网获取原始新闻数据。 | 搜索引擎 API (如 Google Search API, 模拟本环境中的 `search` 工具) |
| **2. 噪音过滤与排名 (Filtering & Ranking)** | 过滤低价值信息（如软文、旧闻），并根据新闻类型（模型、融资、政策等）进行重要性排序。 | **LLM Call 1 (Filtering):** 使用结构化输出（JSON）指令，对每条 Snippet 进行二分类（保留/剔除）。<br>**LLM Call 2 (Ranking):** 使用 Few-shot Prompting 或 Chain-of-Thought 提示词，对保留的新闻进行 1-10 的评分和排序。 |
| **3. 内容生成 (Generation)** | 将原始新闻和排名结果，转化为“一句话摘要”和最终的 Markdown 格式。 | **LLM Call 3 (Drafting):** 接收排名靠前的新闻，生成 50 字以内的中文摘要。<br>**LLM Call 4 (Formatting):** 整合所有内容，严格按照预设的 Markdown 模板输出。 |
| **4. 部署与展示 (Deployment)** | 提供一个简单的运行环境和清晰的演示流程。 | Python 3.11 环境，一个 `generate_briefing.py` 脚本，一个 `README.md`。 |

## 3. 核心 AI 逻辑（Prompt Engineering 示例）

在面试中，您可以重点展示 **LLM Call 1 (Filtering)** 和 **LLM Call 3 (Drafting)** 的 Prompt 设计，以体现您对 LLM 能力的精细控制。

### 示例 Prompt 1: 噪音过滤 (Filtering)

**角色:** 你是一位资深的 AI 科技编辑，你的任务是从原始搜索结果中，识别并剔除低价值、纯营销或重复的“噪音”新闻。
**输入:** 一组新闻 Snippet 列表（包含标题、摘要、URL）。
**指令:**
1. 剔除发布时间超过 48 小时的旧闻。
2. 剔除纯粹的营销软文（如“某某公司发布了不重要的微小更新”）。
3. 剔除与 AI 核心技术（模型、芯片、政策、重大融资）无关的内容。
4. **输出必须是 JSON 格式**，包含一个 `filtered_news` 数组，每个元素包含 `title` 和 `reason`（简述保留或剔除的原因）。

### 示例 Prompt 2: 摘要生成与格式化 (Drafting & Formatting)

**角色:** 你是一位专业的简报撰稿人，你的任务是将筛选后的新闻转化为高信噪比的中文简报。
**输入:** 8-10 条已筛选和排名的重要新闻列表（包含标题、URL）。
**指令:**
1. 严格按照提供的 Markdown 模板结构（头条关注、行业快讯）进行填充。
2. 为每条新闻撰写一个 **50 字以内** 的中文“一句话摘要”。
3. 确保所有 URL 链接都正确嵌入到 Markdown 格式中。
4. **输出只包含最终的 Markdown 文本**，不包含任何解释性文字。

## 4. 演示亮点 (Demo Highlights)

*   **Agentic Workflow:** 展示如何将一个复杂任务拆解为多个 LLM 步骤（搜索 -> 过滤 -> 排名 -> 撰写），体现流程控制能力。
*   **结构化输出 (JSON):** 演示如何使用 Prompt Engineering 强制 LLM 输出可解析的 JSON 格式，确保程序稳定性。
*   **高信噪比:** 强调通过 LLM 过滤和排名，解决了传统爬虫或关键词搜索带来的信息过载问题。
*   **可扩展性:** 讨论如何将 Search API 替换为更专业的数据库（如 Bloomberg Terminal API）或集成 RAG 知识库。
