"""AI Pulse Briefing Generator local, dependency-free demo.

The production idea was originally built with Dify. This module keeps the
filter -> rank -> render contract reproducible without pretending to perform
live search or LLM calls. Pass exported/search results as JSON to try your own
data; without ``--input`` the script uses clearly labelled demo records.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


DEMO_NEWS = [
    {
        "title": "开源多模态模型发布新的推理版本",
        "snippet": "团队发布新的多模态推理版本，并公开模型权重、评测结果与部署说明。",
        "url": "https://example.com/open-model-release",
        "date": (datetime.now() - timedelta(hours=4)).isoformat(),
    },
    {
        "title": "AI 芯片厂商公布新一代推理架构",
        "snippet": "新架构聚焦推理吞吐、能效和集群部署，厂商同步公布了技术路线图。",
        "url": "https://example.com/ai-chip-roadmap",
        "date": (datetime.now() - timedelta(hours=8)).isoformat(),
    },
    {
        "title": "监管机构发布生成式 AI 治理指南",
        "snippet": "指南进一步明确模型透明度、数据治理和高风险场景责任边界。",
        "url": "https://example.com/ai-policy-guide",
        "date": (datetime.now() - timedelta(hours=12)).isoformat(),
    },
    {
        "title": "开发者社区推出新的 Agent 工具链",
        "snippet": "开源工具链新增可观测、评测和工作流编排能力，降低 Agent 调试成本。",
        "url": "https://example.com/agent-toolkit",
        "date": (datetime.now() - timedelta(hours=18)).isoformat(),
    },
    {
        "title": "AI 创业公司完成新一轮融资",
        "snippet": "公司计划将资金投入行业模型研发、产品验证与开发者生态建设。",
        "url": "https://example.com/ai-funding",
        "date": (datetime.now() - timedelta(hours=20)).isoformat(),
    },
    {
        "title": "A new coffee shop opened near an AI conference",
        "snippet": "A local lifestyle story with no material AI product or research update.",
        "url": "https://example.com/coffee-shop",
        "date": (datetime.now() - timedelta(hours=1)).isoformat(),
    },
]

LOW_VALUE_TERMS = ("coffee shop", "咖啡店", "优惠券", "促销")
PRIORITY_TERMS = {
    "model": 4,
    "模型": 4,
    "芯片": 4,
    "chip": 4,
    "政策": 3,
    "监管": 3,
    "开源": 3,
    "open source": 3,
    "agent": 2,
    "融资": 2,
    "funding": 2,
    "评测": 1,
}


def load_news(path: Path) -> list[dict[str, Any]]:
    """Load a JSON array and validate the minimum cross-node contract."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Input JSON must be an array of news objects.")

    required = {"title", "snippet", "url"}
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or not required.issubset(item):
            missing = sorted(required - set(item if isinstance(item, dict) else {}))
            raise ValueError(f"News item {index} is invalid; missing: {missing}")
    return data


def _normalized_title(value: str) -> str:
    return re.sub(r"\W+", "", value, flags=re.UNICODE).lower()


def _importance_score(item: dict[str, Any]) -> int:
    text = f"{item.get('title', '')} {item.get('snippet', '')}".lower()
    return sum(weight for term, weight in PRIORITY_TERMS.items() if term in text)


def _summary(snippet: str, limit: int = 80) -> str:
    cleaned = " ".join(snippet.split())
    return cleaned if len(cleaned) <= limit else f"{cleaned[: limit - 1]}…"


def filter_and_rank(raw_news: Iterable[dict[str, Any]], limit: int = 10) -> dict[str, Any]:
    """Remove obvious noise/duplicates and rank the actual input records."""
    seen_titles: set[str] = set()
    seen_urls: set[str] = set()
    candidates: list[dict[str, Any]] = []
    received = 0

    for item in raw_news:
        received += 1
        title = str(item["title"]).strip()
        snippet = str(item["snippet"]).strip()
        url = str(item["url"]).strip()
        searchable = f"{title} {snippet}".lower()
        normalized_title = _normalized_title(title)

        if not title or not snippet or not url:
            continue
        if any(term in searchable for term in LOW_VALUE_TERMS):
            continue
        if normalized_title in seen_titles or url in seen_urls:
            continue

        seen_titles.add(normalized_title)
        seen_urls.add(url)
        candidates.append(
            {
                "title": title,
                "summary": _summary(snippet),
                "url": url,
                "date": str(item.get("date", "")),
                "score": _importance_score(item),
            }
        )

    candidates.sort(key=lambda item: (item["score"], item["date"]), reverse=True)
    ranked = [{**item, "rank": index} for index, item in enumerate(candidates[:limit], start=1)]
    return {
        "received": received,
        "selected": len(ranked),
        "top_stories": ranked[:3],
        "quick_bites": ranked[3:],
    }


def draft_briefing(ranked_data: dict[str, Any], report_date: date | None = None) -> str:
    """Render ranked news into the public Markdown contract."""
    display_date = (report_date or date.today()).strftime("%Y年%m月%d日")
    lines = [f"## 📅 AI Pulse - {display_date}", "", "### 🚀 头条关注 (Top Stories)", ""]

    if not ranked_data["top_stories"]:
        lines.extend(["今天没有符合筛选条件的重要动态。", ""])
    else:
        for item in ranked_data["top_stories"]:
            lines.extend(
                [
                    f"{item['rank']}. **{item['title']}**",
                    f"   * 📝 **摘要**: {item['summary']}",
                    f"   * 🔗 **来源**: [点击阅读原文]({item['url']})",
                    "",
                ]
            )

    lines.extend(["### 🛠️ 行业快讯 (Quick Bites)", ""])
    if ranked_data["quick_bites"]:
        for item in ranked_data["quick_bites"]:
            lines.append(
                f"* [{item['rank']}] **{item['title']}**: {item['summary']} "
                f"[🔗 来源]({item['url']})"
            )
    else:
        lines.append("* 暂无更多符合条件的行业快讯。")

    lines.extend(
        [
            "",
            "---",
            "💡 **Deep Dive**: 想了解更多？请回复新闻序号，我将为你进一步拆解。",
        ]
    )
    return "\n".join(lines) + "\n"


def main_generator_logic(
    news: Iterable[dict[str, Any]] | None = None,
    report_date: date | None = None,
) -> tuple[str, dict[str, Any]]:
    """Reusable entry point for a Dify HTTP/tool node or another adapter."""
    ranked = filter_and_rank(news if news is not None else DEMO_NEWS)
    return draft_briefing(ranked, report_date), ranked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an AI Pulse Markdown briefing.")
    parser.add_argument("--input", type=Path, help="JSON array from a search/Dify workflow.")
    parser.add_argument("--output", type=Path, default=Path("final_briefing.md"))
    parser.add_argument("--date", help="Report date in YYYY-MM-DD format.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    news = load_news(args.input) if args.input else DEMO_NEWS
    report_date = date.fromisoformat(args.date) if args.date else None
    briefing, stats = main_generator_logic(news, report_date)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(briefing, encoding="utf-8")

    mode = f"input={args.input}" if args.input else "demo data (no live search)"
    print(f"AI Pulse v0.1.0 | {mode}")
    print(f"received={stats['received']} selected={stats['selected']}")
    print(f"saved={args.output}")


if __name__ == "__main__":
    main()
