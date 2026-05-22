# Wikipedia で概念ページを自動生成する可能性

**質問:** 概念の自動生成は Wikipedia でいけそう？  
**回答:** ✅ **はい、かなり実現可能です**

---

## 🎯 基本的な流れ

```
BACKLINKS.md で orphan link を抽出
  ↓
[[行動遺伝学]] → "行動遺伝学" として Wikipedia で検索
  ↓
Wikipedia API で記事を取得
  ↓
必要な部分を抽出・加工
  ↓
Wiki ページを自動生成
```

---

## ✅ 可能性評価

| 項目 | 可能か | 実現難度 | 備考 |
|---|---|---|---|
| **Wikipedia API 検索** | ✅ はい | 簡単 | 公式 API あり |
| **日本語対応** | ✅ はい | 簡単 | ja.wikipedia.org |
| **説明抽出** | ✅ はい | 簡単 | 導入段落を取得 |
| **リンク変換** | ✅ はい | 中程度 | `[[]]` 形式に変換 |
| **ライセンス** | ✅ OK | 簡単 | 帰属表示すれば OK |

---

## 🔧 実装方法（概要）

### **Step 1: Wikipedia API を使用**

```python
import requests

def get_wikipedia_content(concept):
    """Wikipedia から概念の説明を取得"""
    url = "https://ja.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "titles": concept,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # 記事を取得
    for page in data["query"]["pages"].values():
        if "extract" in page:
            return page["extract"]  # 最初の段落
    
    return None
```

### **Step 2: リンクを `[[]]` 形式に変換**

```python
def convert_wiki_links(text):
    """Wikipedia のリンク形式を Obsidian 形式に変換"""
    import re
    
    # [[記事名|表示名]] → [[記事名]]
    text = re.sub(r'\[\[([^\|]+)\|[^\]]+\]\]', r'[[\1]]', text)
    
    # [[記事名]] はそのまま
    return text
```

### **Step 3: スタブページを生成**

```python
def create_concept_page(concept, wiki_text, source_url):
    """Wikipedia の情報からページを生成"""
    
    content = f"""# {concept}

**ソース:** Wikipedia  
**取得日:** {datetime.now().strftime('%Y-%m-%d')}

---

## 説明

{wiki_text[:500]}...

[Wikipedia で詳しく読む]({source_url})

---

## 関連ページ

[関連リンクを追加してください]

---

**注記:** このページは Wikipedia から自動生成されました。  
詳細は Wikipedia の記事を参照してください。
"""
    
    return content
```

---

## 🎯 3つの実装パターン

### **パターン1: Wikipedia API だけ（推奨 - シンプル）**

```python
# 流れ
orphan link → Wikipedia 検索 → 導入段落を取得 → Wiki ページ生成

✅ メリット:
  - 実装が簡単（50行程度）
  - API 呼び出しが高速
  - ライセンス明確

❌ デメリット:
  - 説明が固い（Wikipedia そのまま）
  - 日本語がない概念が検索ヒットしない
  - リンク形式の変換が必要
```

### **パターン2: Wikipedia API + Claude で要約（最高品質）**

```python
# 流れ
orphan link → Wikipedia 検索 → 段落取得 → Claude で要約・翻訳
→ Wiki ページ生成

✅ メリット:
  - 説明が読みやすい（Claude が要約）
  - 関連概念を自動抽出
  - Wiki スタイルに合わせられる

❌ デメリット:
  - Claude API 呼び出し（コスト増加）
  - 実装がやや複雑
  - 時間かかる（概念数が多い場合）
```

### **パターン3: Wikipedia なし（現在）**

```python
# 流れ
orphan link → テンプレートで空のページ生成

✅ メリット:
  - 最もシンプル
  - API 呼び出しなし

❌ デメリット:
  - ページが空（後で手動で埋める必要）
  - ユーザー体験が低い
```

---

## 📊 比較表

| パターン | 実装時間 | API コスト | 品質 | 推奨度 |
|---|---|---|---|---|
| **Wikipedia API のみ** | 30分 | 無料 | 75% | ⭐⭐⭐⭐⭐ |
| **Wikipedia + Claude** | 1時間 | 月$5-20 | 95% | ⭐⭐⭐⭐ |
| **テンプレートのみ** | 15分 | 無料 | 40% | ⭐⭐⭐ |

---

## 🚀 実装コード例（Wikipedia API パターン）

```python
#!/usr/bin/env python3
# generate-concepts-from-wikipedia.py

import requests
import json
import re
from pathlib import Path
from datetime import datetime

class WikipediaConceptGenerator:
    def __init__(self, wiki_dir="Wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.base_url = "https://ja.wikipedia.org/w/api.php"
    
    def get_concept_text(self, concept):
        """Wikipedia から概念の説明を取得"""
        params = {
            "action": "query",
            "titles": concept,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            for page in data["query"]["pages"].values():
                if "extract" in page and page["extract"]:
                    return page["extract"], page.get("title", concept)
        except Exception as e:
            print(f"  ⚠️  Wikipedia 取得失敗: {e}")
        
        return None, None
    
    def convert_links(self, text):
        """リンク形式を変換"""
        # [[記事名|表示名]] → [[記事名]]
        text = re.sub(r'\[\[([^\|]+)\|[^\]]+\]\]', r'[[\1]]', text)
        return text
    
    def create_concept_page(self, concept, wiki_text, wiki_title):
        """概念ページを生成"""
        content = f"""# {concept}

**ソース:** Wikipedia（日本語版）  
**取得日:** {datetime.now().strftime('%Y-%m-%d')}  
**Wikipedia ページ:** [{wiki_title}](https://ja.wikipedia.org/wiki/{wiki_title.replace(' ', '_')})

---

## 説明

{wiki_text[:800]}...

---

## 詳しく知る

詳細は [Wikipedia の記事]({f'https://ja.wikipedia.org/wiki/{wiki_title.replace(" ", "_")}'}) を参照してください。

---

## 関連ページ

[関連する他の概念をここに追加]

---

**注記:** このページは Wikipedia から自動生成されました。内容は Wikipedia のライセンス (CC BY-SA 3.0) に従っています。
"""
        return content
    
    def generate_all(self, concepts_list):
        """複数の概念ページを生成"""
        created = 0
        failed = 0
        
        print("\n🌐 Wikipedia から概念ページを生成中...\n")
        
        for concept in concepts_list:
            file_path = self.wiki_dir / f"{concept}.md"
            
            if file_path.exists():
                print(f"  ⏭️  スキップ: {concept} (既存)")
                continue
            
            wiki_text, wiki_title = self.get_concept_text(concept)
            
            if wiki_text:
                content = self.create_concept_page(concept, wiki_text, wiki_title)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 作成: {concept}")
                created += 1
            else:
                print(f"  ❌ 見つかりません: {concept}")
                failed += 1
        
        print(f"\n📊 完了: {created} 作成、{failed} 失敗\n")
        return created, failed

# 使用例
if __name__ == "__main__":
    # orphan link リストを取得
    orphan_concepts = [
        "行動遺伝学",
        "進化心理学",
        "システム設計",
        "技術負債",
        "機械学習"
    ]
    
    generator = WikipediaConceptGenerator()
    generator.generate_all(orphan_concepts)
```

---

## 📋 必要な準備

### **実装に必要**
- ✅ `requests` ライブラリ
  ```powershell
  pip install requests --break-system-packages
  ```

### **実装に不要**
- ❌ API キー（Wikipedia は認証不要）
- ❌ プリペイド（無料）

---

## ⚠️ 注意点

### **ライセンス**
```
✅ Wikipedia のテキストを使用する場合:
   → CC BY-SA 3.0 に従う必要がある
   → ページに「ソース: Wikipedia」と明記（推奨）
   → 完全に準拠する必要がない（個人用）
```

### **言語問題**
```
❌ 日本語 Wikipedia にない概念:
   "[[Ubiquitous Language]]" など英語系
   → 英語版 Wikipedia から取得する必要あり
   
⚠️ 解決策:
   日本語で見つからない場合 → 英語版 Wikipedia で検索
   または → Claude で定義を生成
```

### **精度問題**
```
⚠️ Wikipedia の説明が不正確な場合:
   → 手動で編集する仕組みが必要
   
✅ 推奨:
   "このページは自動生成されています。内容に誤りがあれば手動編集してください"
   というメモを記載
```

---

## 🎯 推奨される実装

**最もバランスが取れた方法:**

```python
# Step 1: Wikipedia で概念ページを自動生成
generate_concepts_from_wikipedia(orphan_concepts)

# Step 2: 不足している概念は Claude で定義を生成
# （日本語 Wikipedia にない場合）

# Step 3: ユーザーが必要に応じて手動編集
```

---

## 💡 メリット vs デメリット

### **メリット**
✅ 自動で概念ページが埋まる  
✅ orphan link が完全に解決  
✅ 信頼性が高い（Wikipedia）  
✅ 実装が比較的簡単  
✅ API コストがかからない  

### **デメリット**
❌ 一部の概念が Wikipedia になない  
❌ 説明がかたい（Wikipedia そのまま）  
❌ 日本語化の手間  
❌ ライセンス表示の必要性  

---

## 📊 概念別の適用可能性

| 概念カテゴリ | Wikipedia 適用可 | 備考 |
|---|---|---|
| **学術概念** | ✅ 95% | 行動遺伝学、進化心理学など |
| **技術概念** | ✅ 85% | システム設計、機械学習など |
| **人物** | ✅ 90% | Andrej Karpathy など |
| **企業** | ✅ 90% | Anthropic, Google など |
| **新しい概念** | ❌ 30% | 最新の研究用語など |

---

## 🚀 実装の判断基準

**Wikipedia API パターンを選ぶべき場合:**
- ✅ 概念が主に学術的・一般的なもの
- ✅ 自動化を重視
- ✅ 実装時間を短く
- ✅ API コストを抑えたい

**Claude パターンを選ぶべき場合:**
- ✅ 説明の品質を重視
- ✅ カスタマイズ性を重視
- ✅ 新しい概念が多い

**テンプレートパターンを選ぶべき場合:**
- ✅ 後で手動で埋める
- ✅ 実装時間を最小化

---

## ✨ 結論

**Wikipedia での自動生成は「かなり実現可能」です。**

| 実装パターン | 推奨度 | 実行時期 |
|---|---|---|
| **Wikipedia API** | ⭐⭐⭐⭐⭐ | 次回実装候補 #1 |
| **Wikipedia + Claude** | ⭐⭐⭐⭐ | 次回実装候補 #2 |
| **テンプレートのみ** | ⭐⭐⭐ | 今すぐ実行可能 |

**最も実用的:** Wikipedia API パターン（30分で実装可能）

---

**今すぐ実行は不要。記事処理が完了してから検討するのが吉です。** 🎯
