#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import io
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RawFolderHandler(FileSystemEventHandler):
    def __init__(self, api_key):
        self.api_key = api_key
        self.processed = set()

    def on_created(self, event):
        if event.is_directory:
            return

        # ファイルが確実に書き込み完了するまで待機
        time.sleep(2)

        file_path = event.src_path

        # .md ファイルのみ処理
        if not file_path.endswith('.md'):
            return

        # 同じファイルを2回処理しないようにチェック
        if file_path in self.processed:
            return

        self.processed.add(file_path)

        print(f"\n✨ 新しいファイルを検出しました: {Path(file_path).name}")
        print(f"🔄 要約を生成中...\n")

        # ingest スクリプトを実行
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['ANTHROPIC_API_KEY'] = self.api_key

            result = subprocess.run(
                [sys.executable, 'personal-ingest.py', '--source', file_path],
                env=env,
                cwd=Path(__file__).parent
            )

            if result.returncode == 0:
                print(f"✅ 完了！Wiki に追加されました\n")
            else:
                print(f"❌ エラーが発生しました\n")

        except Exception as e:
            print(f"❌ 実行エラー: {e}\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="raw フォルダを監視して自動で要約生成")
    parser.add_argument("--api-key", required=True, help="Anthropic API キー")
    args = parser.parse_args()

    raw_path = Path("raw")
    if not raw_path.exists():
        print(f"❌ {raw_path} フォルダが見つかりません")
        return 1

    print(f"""
╔═════════════════════════════════════════════════════════════╗
║  🚀 LLM Wiki Auto Ingest が起動しました                    ║
║                                                             ║
║  📁 監視フォルダ: raw/                                     ║
║  🎯 動作: 新しいファイルが追加されたら自動で要約生成        ║
║                                                             ║
║  Web Clipper で記事を追加すると自動で処理されます。        ║
║  このウィンドウを開いたままにしておいてください。          ║
║                                                             ║
║  終了: Ctrl + C                                            ║
╚═════════════════════════════════════════════════════════════╝
    """)

    event_handler = RawFolderHandler(args.api_key)
    observer = Observer()
    observer.schedule(event_handler, str(raw_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  監視を停止しました")
        observer.stop()

    observer.join()
    return 0

if __name__ == "__main__":
    sys.exit(main())
