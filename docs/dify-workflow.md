# Dify 工作流升级蓝图

这份文档定义 AI Pulse `v0.1.0` 的工作流意图，方便后续导入原 Dify DSL 后逐项对照。它不是原应用 DSL 的替代品。

## 目标

每天从指定来源收集 AI 动态，过滤低价值和重复事件，保留可追溯来源，最终生成结构稳定的中文 Markdown 简报。

## 节点与数据契约

| 节点 | 输入 | 处理 | 输出 | 失败处理 |
| --- | --- | --- | --- | --- |
| 1. 触发器 | 主题、时间窗、条数 | 手动或定时启动 | `query_config` | 保留手动重跑入口 |
| 2. 新闻检索 | `query_config` | 调用搜索/RSS 工具 | `raw_news[]` | 单来源失败不终止全部流程 |
| 3. 规范化 | `raw_news[]` | 映射标题、片段、URL、时间 | `normalized_news[]` | 缺标题/URL的数据丢弃并计数 |
| 4. 去重过滤 | `normalized_news[]` | URL、标题及事件级去重 | `filtered_news[]` | 全部为空时输出“今日无重大更新” |
| 5. 重要性评分 | `filtered_news[]` | 按技术影响、可信度、时效评分 | `ranked_news[]` | LLM 失败时回退到规则排序 |
| 6. 摘要 | `ranked_news[]` | 只根据输入片段压缩，不补写事实 | `summarized_news[]` | 无法确认的内容标记待核验 |
| 7. 模板输出 | `summarized_news[]` | 渲染 Markdown | `briefing_markdown` | 模板校验失败则不推送 |
| 8. 推送 | `briefing_markdown` | 微信、邮件或知识库写入 | `delivery_status` | 记录失败原因并允许重试 |

跨节点最低字段：

```json
{
  "title": "string",
  "snippet": "string",
  "url": "https://...",
  "date": "ISO-8601",
  "source": "string"
}
```

## Dify 变量建议

| 变量 | 示例 | 说明 |
| --- | --- | --- |
| `topics` | `AI Agent, multimodal, medical AI` | 用户订阅主题 |
| `lookback_hours` | `48` | 最大新闻时间窗 |
| `max_candidates` | `30` | 进入过滤节点的最大候选数 |
| `max_items` | `10` | 最终简报条数 |
| `language` | `zh-CN` | 输出语言 |
| `min_source_score` | `3` | 来源可信度下限 |

## LLM 节点约束

1. 评分与摘要分开，便于失败重试和成本观察。
2. 摘要只能使用检索结果中的事实，不允许补充无来源数字。
3. 每条结果必须保留原始 URL；没有 URL 的内容不得发布。
4. 输出使用结构化 JSON，模板节点负责 Markdown 排版。
5. 搜索结果不足时减少条数，禁止为凑满 8—10 条而编造。

## v0.2 接入原 Dify 应用时需要补齐

- 导出并脱敏 Dify DSL，放到 `dify/` 目录；
- 对照本页确认节点名、输入输出字段和异常分支；
- 记录实际搜索插件、模型和版本，但不提交密钥；
- 增加 10—20 条固定输入的回归测试，检查去重、排序和幻觉；
- 用一次真实运行结果验证来源 URL、时间窗和最终推送。
