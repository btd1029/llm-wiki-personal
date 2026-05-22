#!/usr/bin/env python3
import requests
import json

try:
    payload = {
        'model': 'qwen2.5:7b',
        'prompt': 'AIについて簡潔に説明してください。',
        'stream': False
    }
    print("Ollama /api/generate をテスト中...")
    r = requests.post('http://localhost:11434/api/generate', json=payload, timeout=60)
    print(f'Status Code: {r.status_code}')

    if r.status_code == 200:
        result = r.json()
        print(f'\n✅ 成功！\n')
        print(f'Response:\n{result.get("response", "")}')
    else:
        print(f'\n❌ エラー: {r.status_code}')
        print(f'Response: {r.text[:200]}')

except Exception as e:
    print(f'❌ 接続エラー: {e}')
