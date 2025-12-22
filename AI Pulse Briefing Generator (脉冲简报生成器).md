# AI Pulse Briefing Generator (脉冲简报生成器)

## 🌟 项目概述

本项目是一个 **Agentic AI Workflow** DEMO，它模拟了资深 AI 科技编辑的工作流程，自动生成一份高信噪比的每日 AI 科技新闻简报。

**核心价值:** 展示如何将一个复杂的、需要多步骤决策的非结构化任务（新闻编辑）转化为一个稳定、可重复的自动化流程。

## ⚙️ 技术架构与工作流

本项目采用 **RAG (Retrieval-Augmented Generation) + Agentic Workflow** 架构，将任务拆解为以下关键步骤，每个步骤都模拟了对 LLM 的一次精细化调用：

| 步骤 | 模拟的 LLM/工具调用 | 目的 | 演示亮点 |
| :--- | :--- | :--- | :--- |
| **1. 数据检索 (Retrieval)** | `search` 工具调用 | 收集过去 24 小时内全球 AI 行业新闻片段。 | 关键词工程、时间限定。 |
| **2. 噪音过滤 (Filtering)** | **LLM Call 1 (Filtering)** | 剔除纯营销、低价值或重复的旧闻。 | **结构化输出 (JSON)**，展示对 LLM 输出格式的严格控制。 |
| **3. 排名与摘要 (Ranking & Summarizing)** | **LLM Call 2 (Ranking)** | 根据新闻类型（模型、芯片、融资、政策）进行重要性排序，并生成初稿摘要。 | **Few-shot Prompting** 或 **Chain-of-Thought** 提示词，模拟复杂决策。 |
| **4. 最终撰写 (Drafting)** | **LLM Call 3 (Formatting)** | 严格按照预设的 Markdown 模板，生成最终简报。 | **Prompt Engineering** 确保最终交付物的专业格式。 |

## 🚀 如何运行演示

本项目核心逻辑封装在 `generate_briefing.py` 脚本中。


### 1. 运行脚本

在终端中执行以下命令：

```bash
python3 generate_briefing.py
```

### 2. 观察输出

脚本将按顺序打印出每个步骤的执行情况，包括：
*   数据检索的关键词和结果数量。
*   噪音过滤和排名过程的模拟决策。
*   最终生成的 Markdown 简报内容。

### 3. 查看结果文件

最终生成的简报将保存到当前目录下的 `final_briefing.md` 文件中。

```bash
cat final_briefing.md
```

