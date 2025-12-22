# AI Pulse Briefing Generator：微信每日推送集成方案

## 1. 架构概述：Serverless 自动化工作流

为了实现每日定时、稳定地将 AI 简报推送到微信，我们采用 **Serverless 架构**。这种架构具有免运维、按需付费、高可靠性等优点，非常适合作为面试展示的工程化方案。

**核心工作流 (Workflow):**

1.  **定时触发 (Scheduler):** 每日固定时间（例如早上 8:00），由云服务商的定时任务触发器启动。
2.  **简报生成 (Generator):** Serverless Function 运行 `generate_briefing.py` 脚本，完成数据检索、过滤、排名和 Markdown 撰写。
3.  **内容推送 (Notifier):** Function 将生成的 Markdown 内容通过 **Webhook** 发送到一个支持微信通知的第三方服务。
4.  **微信接收 (Receiver):** 第三方服务将内容格式化后，推送到用户的微信。

## 2. 技术选型与组件 (Component Selection)

| 组件 | 角色 | 推荐技术选型 | 备注 |
| :--- | :--- | :--- | :--- |
| **定时器** | 每日定时启动工作流 | AWS CloudWatch Events / Lambda Scheduler, 阿里云函数计算定时触发器, **腾讯云 SCF 定时触发器** | 推荐使用腾讯云 SCF，与微信生态更接近。 |
| **简报生成器** | 运行核心 Python 逻辑 | **Python Serverless Function (SCF/Lambda)** | 运行 `generate_briefing.py`，需要配置 Python 依赖（如 `requests`）。 |
| **推送服务** | 接收 Webhook 并推送到微信 | **Server酱 (ServerChan)** 或 **企业微信应用** | Server酱配置简单，适合个人 Demo；企业微信应用更专业，适合企业级展示。 |
| **核心代码** | 封装生成和推送逻辑 | Python (`requests` 库) | 负责调用 LLM（模拟）和发送 HTTP POST 请求到推送服务的 Webhook URL。 |

## 3. 核心代码逻辑（伪代码）

以下是 Serverless Function 中 `handler` 函数的核心逻辑，它将 `generate_briefing.py` 的功能封装并增加了推送步骤。

```python
# 文件: wechat_notifier.py (部署在 Serverless Function 中)
import requests
import os
from generate_briefing import main_generator_logic # 假设已将生成逻辑模块化

# 配置 Webhook URL (从 Server酱 或 企业微信获取)
WECHAT_WEBHOOK_URL = os.environ.get("WECHAT_WEBHOOK_URL")

def lambda_handler(event, context):
    """
    Serverless Function 的入口函数
    """
    try:
        # 1. 运行简报生成逻辑
        # final_briefing_markdown 是 generate_briefing.py 运行后的最终输出
        final_briefing_markdown = main_generator_logic() 
        
        # 2. 准备推送数据
        # Server酱要求 title 和 desp (内容)
        payload = {
            "title": f"📅 AI Pulse - {datetime.now().strftime('%Y年%m月%d日')}",
            "desp": final_briefing_markdown # Markdown 内容
        }
        
        # 3. 发送 Webhook 通知
        response = requests.post(WECHAT_WEBHOOK_URL, data=payload)
        
        if response.status_code == 200:
            print("简报成功推送到微信服务。")
            return {
                'statusCode': 200,
                'body': 'Briefing pushed successfully.'
            }
        else:
            print(f"推送失败，状态码: {response.status_code}, 响应: {response.text}")
            raise Exception("Webhook push failed.")

    except Exception as e:
        print(f"工作流执行失败: {e}")
        return {
            'statusCode': 500,
            'body': f'Error: {e}'
        }

# ----------------------------------------------------------------
# 提示：在面试中，您可以强调 main_generator_logic() 内部的 Agentic Workflow
# ----------------------------------------------------------------
```

## 4. 演示亮点与面试价值

*   **自动化与调度 (Automation & Scheduling):** 展示您不仅能写出核心 AI 逻辑，还能将其部署到生产环境并实现自动化，体现工程化思维。
*   **系统集成 (System Integration):** 演示如何使用 Webhook 这种标准化的接口，将两个完全不同的系统（AI 生成器和微信通知）连接起来。
*   **Serverless 理念:** 强调使用 Serverless Function 可以实现零运维、高弹性、低成本的运行，体现对现代云计算架构的理解。
*   **解耦设计 (Decoupling):** 简报生成逻辑与推送逻辑分离，任何一方的变更都不会影响另一方，增强了系统的健壮性。
