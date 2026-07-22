import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from generate_briefing import draft_briefing, filter_and_rank, load_news, main_generator_logic


class BriefingGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.news = [
            {
                "title": "开源模型发布",
                "snippet": "团队发布模型权重与评测结果。",
                "url": "https://example.com/model",
                "date": "2026-07-22T08:00:00+08:00",
            },
            {
                "title": "开源模型发布",
                "snippet": "重复事件。",
                "url": "https://example.net/model-copy",
                "date": "2026-07-22T07:00:00+08:00",
            },
            {
                "title": "A new coffee shop opened",
                "snippet": "A lifestyle story.",
                "url": "https://example.com/coffee",
                "date": "2026-07-22T09:00:00+08:00",
            },
        ]

    def test_filters_noise_and_duplicate_titles(self):
        result = filter_and_rank(self.news)
        self.assertEqual(result["received"], 3)
        self.assertEqual(result["selected"], 1)
        self.assertEqual(result["top_stories"][0]["title"], "开源模型发布")

    def test_markdown_keeps_source_and_date(self):
        ranked = filter_and_rank(self.news)
        markdown = draft_briefing(ranked, date(2026, 7, 22))
        self.assertIn("AI Pulse - 2026年07月22日", markdown)
        self.assertIn("https://example.com/model", markdown)

    def test_empty_input_is_honest(self):
        markdown, stats = main_generator_logic([], date(2026, 7, 22))
        self.assertEqual(stats["selected"], 0)
        self.assertIn("没有符合筛选条件", markdown)

    def test_load_news_validates_required_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "news.json"
            path.write_text(json.dumps([{"title": "missing fields"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_news(path)


if __name__ == "__main__":
    unittest.main()
