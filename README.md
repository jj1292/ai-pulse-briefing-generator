# AI Pulse Briefing Generator

> 用 Dify 编排“检索 → 去重 → 排序 → 摘要 → Markdown 输出”的每日 AI 信息简报。

AI Pulse 是一个面向 AI 从业者的信息筛选工作流。项目最初使用 Dify 搭建；仓库中的 Python 版本用于复现核心数据契约、验证筛选逻辑，并作为后续接入真实新闻源和 Dify DSL 的最小测试环境。

## 当前版本

`v0.1.0` 是重新整理后的第一个可迭代版本：

- 输入 JSON 新闻列表，基于真实输入完成去噪、去重和优先级排序；
- 输出结构稳定的中文 Markdown 简报；
- 无输入时使用明确标注的演示数据，不声称进行了实时搜索；
- 提供 Dify 工作流升级蓝图、单元测试和 GitHub Actions；
- 不需要第三方 Python 依赖，也不需要 API Key。

## 30 秒运行

```bash
python3 generate_briefing.py
```

运行完成后查看 `final_briefing.md`。默认结果来自演示数据，仅用于验证流程。

使用自己的搜索结果：

```bash
python3 generate_briefing.py \
  --input examples/news.json \
  --output outputs/briefing.md \
  --date 2026-07-22
```

输入必须是 JSON 数组，每条记录至少包含：

```json
{
  "title": "新闻标题",
  "snippet": "新闻摘要或正文片段",
  "url": "https://example.com/source",
  "date": "2026-07-22T08:00:00+08:00"
}
```

## Dify 工作流

推荐的首版节点：

```text
定时/手动触发 → 新闻检索 → 字段规范化 → 去重与规则过滤
             → LLM 重要性评分 → LLM 摘要 → 模板输出
```

节点输入输出、失败兜底和后续升级顺序见 [Dify 工作流说明](docs/dify-workflow.md)。原 Dify 应用的 DSL 尚未放入仓库，因此当前版本不会假装还原未提供的配置。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
```

## 项目边界

- 当前 Python 版本不是实时新闻搜索器；实时检索应由 Dify 工具节点、RSS 或搜索 API 提供。
- 当前排序是可解释的关键词基线，后续可替换为 Dify LLM 评分节点。
- 示例域名和数据仅用于演示，不能作为真实新闻来源。
- Dify、搜索服务和模型密钥只能配置在环境变量或 Secret 中，不提交到仓库。

## Roadmap

- [x] v0.1：项目门面、输入契约、可测试的本地基线
- [ ] v0.2：导入原 Dify DSL，完成真实搜索与 48 小时时效校验
- [ ] v0.3：来源可信度、事实核验、重复事件聚合
- [ ] v0.4：定时发布与微信/邮件推送
- [ ] v1.0：可配置订阅主题、评测集和稳定性监控

欢迎通过 Issue 提交希望关注的 AI 主题、信息源或输出渠道。

## License

[MIT](LICENSE)
