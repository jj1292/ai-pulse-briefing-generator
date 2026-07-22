# Dify 工作流升级蓝图

本文定义 AI Intelligence Radar `v0.2.0` 的工作流意图。原 Dify DSL 尚未提供，因此这里先冻结跨节点数据契约，后续导入 DSL 时逐项对账。

## 目标

从官方发布、官方仓库、X 一手账号和 Reddit 社区中收集 AI 信号，区分事实与社区反馈，生成少量高价值情报卡片，并长期写入 Obsidian。

## 节点与数据契约

| 节点 | 输入 | 处理 | 输出 | 失败处理 |
| --- | --- | --- | --- | --- |
| 1. 触发器 | 主题、时间窗、来源组 | 手动或定时启动 | `query_config` | 保留手动重跑入口 |
| 2. 来源路由 | `config/sources.json` | 按采集方式和授权状态分流 | `source_tasks[]` | 未授权来源跳过并记录 |
| 3. 采集 | `source_tasks[]` | 官方网页、Atom、X API、Reddit OAuth | `raw_signals[]` | 单来源失败不终止全部流程 |
| 4. 规范化 | `raw_signals[]` | 映射公司、时间、URL、来源等级 | `normalized_signals[]` | 缺 URL/时间的数据不发布 |
| 5. 去重 | `normalized_signals[]` | URL、标题、事件三级去重 | `unique_signals[]` | 保存去重计数 |
| 6. 判断 | `unique_signals[]` | 摘要、重要性、为什么重要、主题 | `intelligence_signals[]` | LLM 失败时保留待处理队列 |
| 7. 证据门 | `intelligence_signals[]` | 检查来源、时间、短证据和主张边界 | `verified_signals[]` | 证据不足降级为“待核验” |
| 8. 知识导出 | `verified_signals[]` | 生成卡片与趋势雷达 | Markdown 文件 | 失败时保留结构化 JSON |
| 9. 简报/推送 | 趋势雷达、高分卡片 | 生成每日摘要 | `briefing_markdown` | 推送失败不影响知识保存 |

跨节点契约以 `schemas/intelligence-signal.schema.json` 为准。

## Dify 变量建议

| 变量 | 示例 | 说明 |
| --- | --- | --- |
| `topics` | `coding agents, multimodal, AI product` | 订阅主题 |
| `lookback_hours` | `48` | 新闻和帖子时间窗 |
| `max_candidates` | `50` | 每次采集候选上限 |
| `max_cards` | `10` | 每日知识卡片上限 |
| `min_impact_score` | `3` | 进入知识库的影响门槛 |
| `language` | `zh-CN` | 卡片和简报语言 |

## 来源分级规则

- T1 官方来源可以作为事实底座，但仍需保留原始 URL 和发布时间。
- T2 X 一手账号用于捕捉发布前后补充信息，账号身份必须预先核验。
- T3 Reddit 用于发现真实问题、使用反馈和早期趋势，不能单独证明产品能力。
- 同一公司重复转发同一公告只算一个事件；跨公司出现相似能力才是更强趋势信号。

## LLM 节点约束

1. 摘要、影响判断和证据提取分字段输出。
2. 只能使用采集结果中的事实，不允许补写数字、发布日期或产品能力。
3. `why_it_matters` 必须说明对产品、技术、市场或个人判断的影响。
4. 社区观点必须标记为社区信号，禁止改写成官方结论。
5. 搜索结果不足时减少条数，禁止为了日报篇幅编造内容。

## v0.3 接入采集器时需要补齐

- 验证 X 官方账号句柄，配置 Developer Project 和 Secret；
- 注册 Reddit OAuth App，确认个人知识管理用途与数据保留边界；
- 实现官方 Atom、Release Notes、X Recent Search 和 Reddit Search 适配器；
- 增加 48 小时时效、分页、重试、速率限制和删除同步；
- 用 20—50 条固定样本评估覆盖率、重复率、误报和趋势误判。

## v0.4 导入原 Dify 应用时需要补齐

- 导出并脱敏 Dify DSL，放到 `dify/` 目录；
- 对照本页确认节点名、字段和异常分支；
- 记录实际模型、插件与版本，不提交密钥；
- 用真实运行结果验证来源 URL、时间窗、知识卡片和 Obsidian 写入。
