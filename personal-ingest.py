#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import io
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic

# UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class PersonalWikiIngester:
    def __init__(self, source_file: str, output_dir: str = "Wiki"):
        self.source_file = Path(source_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.client = Anthropic()
        
        if not self.source_file.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {source_file}")

    def read_source(self) -> str:
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_summary_and_keywords(self, content: str) -> dict:
        """Claude API で要約とキーワードを生成"""
        print("     🤖 Claude に要約を依頼中...")

        prompt = f"""以下のテキストを読んで、以下を日本語で提供してください：

1. 簡潔な要約（2-3文）
2. 主要な概念（5-7個、[[こういう形]]、他の記事と繋がりそうなもの優先）
3. この記事の前提となる知識（3-5個、[[知識1]]のように記述）
4. この記事から派生する応用分野（3-5個、[[応用1]]のように記述）
5. 関連する人物・著者・企業（2-5個、例：[[Andrej Karpathy]], [[Anthropic]]）
6. ソースURL（記事の元のURLがあれば、なければnullを返す）

概念の例（含めるべき種類）:
- 理論：[[行動遺伝学]]、[[進化心理学]]、[[機械学習]]
- 実践：[[システム設計]]、[[テスト駆動開発]]、[[code review]]
- スキル：[[深いモジュール]]、[[ユビキタス言語]]
- 概念：[[認知的複雑さ]]、[[技術負債]]、[[デザインパターン]]

---
{content}
---

JSON形式で以下のように返してください：
{{
    "summary": "要約",
    "concepts": ["[[概念1]]", "[[概念2]]"],
    "prerequisites": ["[[前提知識1]]", "[[前提知識2]]"],
    "applications": ["[[応用分野1]]", "[[応用分野2]]"],
    "related_people": ["[[人物1]]", "[[企業1]]"],
    "source_url": "https://example.com/article" または null
}}"""

        message = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            import json
            response_text = message.content[0].text
            # JSON を抽出（マークダウンブロックから）
            if "`json" in response_text:
                json_str = response_text.split("`json")[1].split("`")[0]
            elif "`" in response_text:
                json_str = response_text.split("`")[1].split("`")[0]
            else:
                json_str = response_text

            result = json.loads(json_str)
            return result
        except Exception as e:
            print(f"     ⚠️  JSON パース失敗: {e}")
            return {
                "summary": "[要約をここに追加してください]",
                "concepts": ["[[概念1]]", "[[概念2]]"],
                "prerequisites": ["[[前提知識1]]"],
                "applications": ["[[応用分野1]]"],
                "related_people": ["[[人物1]]"],
                "source_url": None
            }

    def create_wiki_entry(self, content: str, metadata: dict) -> str:
        """Wiki エントリを生成"""
        title = self.source_file.stem.replace('-', ' ').title()
        summary = metadata.get('summary', '[要約]')
        concepts = metadata.get('concepts', [])
        prerequisites = metadata.get('prerequisites', [])
        applications = metadata.get('applications', [])
        related_people = metadata.get('related_people', [])
        source_url = metadata.get('source_url')

        concepts_str = '\n'.join([f"- {c}" for c in concepts]) if concepts else "- [[概念1]]\n- [[概念2]]"
        prerequisites_str = '\n'.join([f"- {c}" for c in prerequisites]) if prerequisites else "- [[前提知識1]]"
        applications_str = '\n'.join([f"- {c}" for c in applications]) if applications else "- [[応用分野1]]"
        related_people_str = ', '.join(related_people) if related_people else "[[人物1]]"

        # リンク作成（URLがあればリンク、なければテキストのみ）
        if source_url:
            read_more = f"[続きはこちら]({source_url})"
        else:
            read_more = "[続きはこちら]"

        template = f"""# {title}

**ファイルパス：** Wiki/{self.source_file.stem}.md
**作成日：** {datetime.now().strftime('%Y-%m-%d')}
**出典：** {self.source_file}

---

## 概要

{summary}

---

## 主要な概念

{concepts_str}

---

## 前提となる知識

{prerequisites_str}

---

## 内容

{content[:1000]}...

{read_more}

---

## 派生する応用分野

{applications_str}

---

## 関連する人物・企業

{related_people_str}

---

## 個人メモ

[あなたの感想・思いつきをここに記録]

---

## 次のアクション

- [ ] 内容の詳細版を追加
- [ ] 他の記事とバックリンクを接続
- [ ] タグを追加
"""
        return template

    def save_entry(self, content: str) -> str:
        output_file = self.output_dir / f"{self.source_file.stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(output_file)

    def run(self) -> dict:
        print(f"\n📖 {self.source_file} を処理中...\n")
        
        # ステップ1: ファイル読み込み
        print("  1️⃣  ファイルを読み込み中...")
        try:
            content = self.read_source()
            print(f"     ✅ {len(content)} 字を読み込みました")
        except Exception as e:
            print(f"     ❌ エラー: {e}")
            return {"status": "FAILED", "error": str(e)}

        # ステップ2: Claude で要約生成
        print("  2️⃣  Claude で要約を生成中...")
        try:
            metadata = self.generate_summary_and_keywords(content)
            print(f"     ✅ 要約とキーワードを生成しました")
        except Exception as e:
            print(f"     ❌ エラー: {e}")
            metadata = {"summary": "[要約]", "concepts": [], "related_topics": []}

        # ステップ3: Wiki エントリを生成
        print("  3️⃣  Wiki エントリを生成中...")
        try:
            entry = self.create_wiki_entry(content, metadata)
            print(f"     ✅ エントリを生成しました")
        except Exception as e:
            print(f"     ❌ エラー: {e}")
            return {"status": "FAILED", "error": str(e)}

        # ステップ4: Wiki に保存
        print("  4️⃣  Wiki に保存中...")
        try:
            output_path = self.save_entry(entry)
            print(f"     ✅ 保存しました: {output_path}")
        except Exception as e:
            print(f"     ❌ エラー: {e}")
            return {"status": "FAILED", "error": str(e)}

        return {
            "status": "SUCCESS",
            "source": str(self.source_file),
            "output": output_path,
            "timestamp": datetime.now().isoformat(),
        }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="個人用 LLM Wiki Ingest スクリプト（Claude API版）")
    parser.add_argument("--source", required=True, help="raw/ のソースファイル")
    parser.add_argument("--output", default="Wiki", help="出力ディレクトリ")
    args = parser.parse_args()

    try:
        ingester = PersonalWikiIngester(args.source, args.output)
        result = ingester.run()
        
        if result["status"] == "SUCCESS":
            print(f"\n{'='*60}")
            print(f"✅ 成功！\n")
            print(f"📄 作成されたファイル：")
            print(f"   {result['output']}\n")
            print(f"💡 次のステップ：")
            print(f"   1. Obsidian で {result['output']} を開く")
            print(f"   2. 要約を確認・編集")
            print(f"   3. [[関連記事]] でバックリンクを追加")
            print(f"   4. git add Wiki/ && git commit\n")
            print(f"{'='*60}\n")
            return 0
        else:
            print(f"\n❌ エラーが発生しました: {result['error']}\n")
            return 1
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
