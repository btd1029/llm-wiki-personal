#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wikipedia から orphan concept ページを自動生成

BACKLINKS.md から ✗ が付いている概念を抽出して、
Wikipedia から説明を取得し、Wiki ページを自動生成します。
"""

import requests
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class WikipediaConceptGenerator:
    def __init__(self, wiki_dir="Wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.backlinks_file = self.wiki_dir / "BACKLINKS.md"
        self.base_url = "https://ja.wikipedia.org/w/api.php"
        self.concepts_generated = 0
        self.concepts_failed = 0

    def extract_orphan_concepts(self) -> set:
        """BACKLINKS.md から orphan link（✗ 付き）を抽出"""
        orphan_concepts = set()

        if not self.backlinks_file.exists():
            print("❌ BACKLINKS.md が見つかりません")
            return orphan_concepts

        with open(self.backlinks_file, 'r', encoding='utf-8') as f:
            for line in f:
                # ✗ [[概念名]] というパターンを抽出
                if '✗' in line and '[[' in line:
                    match = re.search(r'\[\[([^\]]+)\]\]', line)
                    if match:
                        concept = match.group(1)
                        orphan_concepts.add(concept)

        return orphan_concepts

    def get_wikipedia_content(self, concept: str) -> tuple:
        """Wikipedia から概念の説明を取得"""
        params = {
            "action": "query",
            "titles": concept,
            "prop": "extracts",
            "explaintext": True,
            "format": "json",
            "exintro": True  # 導入段落のみ
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            for page in data["query"]["pages"].values():
                # "missing" キーがなければページが存在する
                if "missing" not in page and "extract" in page:
                    extract = page["extract"].strip()
                    title = page.get("title", concept)

                    if extract:
                        return extract, title

        except Exception as e:
            print(f"  ⚠️  API エラー ({concept}): {e}")

        return None, None

    def convert_wiki_links(self, text: str) -> str:
        """Wikipedia リンク形式を Obsidian 形式に変換"""
        if not text:
            return ""

        # [[記事名|表示名]] → [[記事名]]
        text = re.sub(r'\[\[([^\|]+)\|[^\]]+\]\]', r'[[\1]]', text)

        # 外部リンク [表示名](URL) は保持
        return text

    def create_concept_page(self, concept: str, wiki_text: str, wiki_title: str) -> str:
        """Wikipedia の情報からページを生成"""

        # 説明の最初の2文程度に制限（500文字程度）
        lines = wiki_text.split('\n')
        description = '\n'.join(lines[:3]) if lines else wiki_text

        # Wikipedia URL を作成
        wiki_url = f"https://ja.wikipedia.org/wiki/{wiki_title.replace(' ', '_')}"

        content = f"""# {concept}

**ソース:** Wikipedia（日本語版）
**取得日:** {datetime.now().strftime('%Y-%m-%d')}

---

## 説明

{description}

---

## 詳しく知る

詳細は [Wikipedia の記事]({wiki_url}) を参照してください。

---

## 関連ページ

[関連する他の概念をここに追加してください]

---

**注記:** このページは Wikipedia から自動生成されました。
内容は [Wikipedia のライセンス (CC BY-SA 3.0)](https://ja.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License) に従っています。
詳細や追加情報は Wikipedia の記事を参照してください。
"""
        return content

    def save_concept_page(self, concept: str, content: str) -> bool:
        """概念ページを保存"""
        file_path = self.wiki_dir / f"{concept}.md"

        if file_path.exists():
            return False  # 既に存在する場合はスキップ

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  ❌ 保存エラー ({concept}): {e}")
            return False

    def run(self):
        """メイン処理"""
        print("\n" + "="*70)
        print("🌐 Wikipedia から Orphan Concept ページを自動生成")
        print("="*70)

        # Step 1: orphan concepts を抽出
        print("\n📋 Orphan concepts を抽出中...")
        orphan_concepts = self.extract_orphan_concepts()

        if not orphan_concepts:
            print("ℹ️  orphan concepts が見つかりません")
            return

        print(f"✅ {len(orphan_concepts)} 個の orphan concepts が見つかりました\n")

        # Step 2: Wikipedia から情報を取得して ページを生成
        print("🔄 Wikipedia から情報を取得中...\n")

        for i, concept in enumerate(sorted(orphan_concepts), 1):
            # プログレス表示
            print(f"[{i}/{len(orphan_concepts)}] {concept}...", end=" ")

            # Wikipedia から取得
            wiki_text, wiki_title = self.get_wikipedia_content(concept)

            if wiki_text:
                # ページを生成
                content = self.create_concept_page(concept, wiki_text, wiki_title)

                # 保存
                if self.save_concept_page(concept, content):
                    print("✅")
                    self.concepts_generated += 1
                else:
                    print("⏭️  (既存)")
            else:
                print("❌")
                self.concepts_failed += 1

        # Step 3: 結果を表示
        print("\n" + "="*70)
        print("📊 完了")
        print("="*70)
        print(f"✅ 生成: {self.concepts_generated} 個")
        print(f"❌ 失敗: {self.concepts_failed} 個")
        print(f"⏭️  スキップ: {len(orphan_concepts) - self.concepts_generated - self.concepts_failed} 個")
        print("="*70 + "\n")

        if self.concepts_generated > 0:
            print(f"💡 次のステップ:")
            print(f"   1. Obsidian で Wiki/ フォルダをリロード")
            print(f"   2. Graph View で新しいページを確認")
            print(f"   3. 必要に応じて説明を編集")
            print(f"   4. git add Wiki/ && git commit\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Wikipedia から orphan concept ページを自動生成"
    )
    parser.add_argument(
        "--wiki-dir",
        default="Wiki",
        help="Wiki ディレクトリ（デフォルト: Wiki）"
    )
    args = parser.parse_args()

    generator = WikipediaConceptGenerator(args.wiki_dir)
    generator.run()

if __name__ == "__main__":
    main()
