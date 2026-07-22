# AI Intelligence Radar

> 从一手 AI 动态中提炼可追溯的判断，再沉淀成自己的长期知识库。

AI Intelligence Radar 是 AI Pulse Briefing Generator 的第二阶段。项目最初使用 Dify 搭建；现在从“一次性每日简报”升级为“来源注册 → 信号筛选 → 情报卡片 → 趋势判断 → Obsidian 知识库”的个人认知系统。

## 当前版本：v0.2.0

- 建立 OpenAI/Codex、Anthropic/Claude、Google/Gemini 的 T1 官方来源注册表；
- 为 X 官方账号和 Reddit AI 社区预留合规授权入口；
- 用统一 Schema 保存出处、时间、公司、主题、证据和影响判断；
- 把规范化信号导出为 Obsidian Markdown 知识卡片；
- 只有两条以上独立信号才进入趋势候选，避免把单条新闻当趋势；
- 保留 v0.1 的本地简报生成器。

完整产品边界见 [v0.2 PRD](docs/PRD-AI-Intelligence-Radar-v0.2.md)。

## 工作流

```text
官方发布 / GitHub / X / Reddit
              ↓
来源分级 → 规范化 → 去重 → 重要性判断
              ↓
      情报卡片 → 趋势雷达 → Obsidian
```

来源等级：

- T1：公司官方 Release Notes、Newsroom、官方代码仓库；
- T2：官方或核心团队 X 一手账号；
- T3：Reddit 等社区信号，只用于发现问题和情绪，不直接当作事实。

## 运行 v0.2 示例

验证来源注册表：

```bash
python3 source_registry.py --config config/sources.json
```

生成知识卡片和趋势雷达：

```bash
python3 build_knowledge_base.py \
  --input examples/intelligence_signals.json \
  --output /tmp/ai-intelligence-radar \
  --date 2026-07-22
```

生成结果：

```text
/tmp/ai-intelligence-radar/
├── signals/2026-07-22/*.md
└── trends/2026-07-22-trend-radar.md
```

要直接写入 Obsidian，只需把 `--output` 换成自己的 Vault 项目目录；仓库不会硬编码个人路径。

## 规范化信号

每条信号至少包含：

```json
{
  "title": "产品更新标题",
  "canonical_url": "https://example.com/source",
  "source_name": "Official release notes",
  "source_tier": 1,
  "platform": "official",
  "company": "OpenAI",
  "published_at": "2026-07-22T08:00:00+08:00",
  "summary": "发生了什么",
  "why_it_matters": "为什么会改变判断",
  "evidence": ["一条可回到原文核验的短证据"],
  "topics": ["coding-agents"]
}
```

完整定义见 [Intelligence Signal Schema](schemas/intelligence-signal.schema.json)。

## X 与 Reddit

两类来源默认标为 `requires_auth`：

- X Recent Search 需要开发者项目和 `X_BEARER_TOKEN`；
- Reddit 使用 OAuth，需要 `REDDIT_CLIENT_ID`、`REDDIT_CLIENT_SECRET` 和明确的 User-Agent；
- 所有凭证只能放在本地环境变量或 Secret，禁止提交到仓库；
- Reddit 只保留链接、必要元数据和衍生判断，不批量保存完整用户内容。

当前来源和授权要求见 [config/sources.json](config/sources.json)。

## v0.1 简报模式

原简报生成器继续可用：

```bash
python3 generate_briefing.py \
  --input examples/news.json \
  --output /tmp/final_briefing.md \
  --date 2026-07-22
```

## 测试

```bash
python3 -m unittest discover -s tests -v
python3 source_registry.py --config config/sources.json
```

## 项目边界

- 当前版本完成“输入到知识库”的闭环，不声称已启用 X/Reddit 实时采集。
- Dify 负责后续定时采集和 LLM 结构化，Python 负责可测试的知识导出。
- 知识卡片保存摘要、证据和个人判断，不复制整篇受版权保护内容。
- 社区热度必须与 T1 官方来源或可复现实验交叉验证。
- 原 Dify DSL 尚未进入仓库，后续导入时需要逐节点对账。

## Roadmap

- [x] v0.1：可运行简报、输入契约、测试与 GitHub Actions
- [x] v0.2：来源注册表、情报 Schema、Obsidian 卡片与趋势雷达
- [ ] v0.3：官方采集器、X API、Reddit OAuth、48 小时时效与事件去重
- [ ] v0.4：导入 Dify DSL、定时运行、证据校验与自动写入
- [ ] v1.0：周/月复盘、来源质量评分、主题订阅和评测指标

## License

[MIT](LICENSE)
