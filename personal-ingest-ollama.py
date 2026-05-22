#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import io
import json
import requests
from pathlib import Path
from datetime import datetime

# UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class PersonalWikiIngester:
    def __init__(self, source_file: str, output_dir: str = "Wiki", ollama_model: str = "qwen2.5"):
        self.source_file = Path(source_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = ollama_model

        if not self.source_file.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {source_file}")

    def read_source(self) -> str:
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_summary_and_keywords(self, content: str) -> dict:
        """Ollama のローカルLLMで要約とキーワードを生成"""
        print("     🤖 Ollama に要約を依頼中...")

        prompt = f"""以下のテキストを読んで、以下を日本語で提供してください：

1. 簡潔な要約（2-3文）
2. 主要な概念（3-5個、[[こういう形]]）
3. 関連するトピック（3-5個、例：[[AI]], [[機械学習]]）

---
{content}
---

JSON形式で以下のように返してください：
{{
    "summary": "要約",
    "concepts": ["[[概念1]]", "[[概念2]]"],
    "related_topics": ["[[トピック1]]", "[[トピック2]]"]
}}"""

        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API エラー: {response.status_code}")

            response_data = response.json()
            response_text = response_data.get("response", "")

            # JSON を抽出
            if "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                raise Exception("JSON形式の応答が見つかりません")

        except requests.exceptions.ConnectionError:
            print(f"     ⚠️  Ollama サーバーに接続できません")
            print(f"        コマンドを実行してください: ollama serve")
            return {
                "summary": "[要約をここに追加してください]",
                "concepts": ["[[概念1]]", "[[概念2]]"],
                "related_topics": ["[[トピック1]]"]
            }
        except Exception as e:
            print(f"     ⚠️  JSON パース失敗: {e}")
            return {
                "summary": "[要約をここに追加してください]",
                "concepts": ["[[概念1]]", "[[概念2]]"],
                "related_topics": ["[[トピック1]]"]
            }

    def create_wiki_entry(self, content: str, metadata: dict) -> str:
        """Wiki エントリを生成"""
        title = self.source_file.stem.replace('-', ' ').title()
        summary = metadata.get('summary', '[要約]')
        concepts = metadata.get('concepts', [])
        related = metadata.get('related_topics', [])

        concepts_str = '\n'.join([f"- {c}" for c in concepts]) if concepts else "- [[概念1]]\n- [[概念2]]"
        related_str = ', '.join(related) if related else "[[トピック1]], [[トピック2]]"

        template = f"""# {title}

**ファイルパス：** Wiki/{self.source_file.stem}.md
**作成日：** {datetime.now().strftime('%Y-%m-%d')}
**処理エンジン：** Ollama ({self.ollama_model})
**出典：** {self.source_file}

---

## 概要

{summary}

---

## 主要な概念

{concepts_str}

---

## 内容

{content[:1000]}...

[続きはこちら]

---

## 関連トピック

{related_str}

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

        # ステップ2: Ollama で要約生成
        print("  2️⃣  Ollama で要約を生成中...")
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
    parser = argparse.ArgumentParser(description="個人用 LLM Wiki Ingest スクリプト（Ollama ローカル版）")
    parser.add_argument("--source", required=True, help="raw/ のソースファイル")
    parser.add_argument("--output", default="Wiki", help="出力ディレクトリ")
    parser.add_argument("--model", default="qwen2.5", help="Ollama モデル名")
    args = parser.parse_args()

    try:
        ingester = PersonalWikiIngester(args.source, args.output, args.model)
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
