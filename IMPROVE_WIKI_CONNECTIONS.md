# Wiki の記事同士の結びつきを強化する方法

**現状:** 記事は生成されているが、相互リンクが弱い  
**目標:** 関連記事が自動で繋がり、バックリンクが充実

---

## 🎯 考えられる処置（優先順位順）

### **1️⃣ Claude プロンプトを改善（最も効果的）**

**現在の問題:**
```
現在: [[概念1]], [[概念2]] などが抽出されるが、
     多くの概念ページが存在しない（orphan link）
     → リンク切れが多い
```

**解決策: Claude プロンプトを強化**

`personal-ingest.py` の prompt を改善：

```python
# 現在のプロンプト（弱い）
prompt = f"""
1. 簡潔な要約（2-3文）
2. 主要な概念（3-5個）
3. 関連するトピック（3-5個）
4. ソースURL
"""

# 改善版（強い）
prompt = f"""
1. 簡潔な要約（2-3文）
2. 主要な概念（5-7個、他の記事と繋がりそうなもの優先）
3. この記事の前提となる知識
4. この記事から派生する知識
5. 関連する他の分野
6. ソースURL

以下のような概念を含めてください:
- 理論的な概念（行動遺伝学、進化心理学など）
- 実践的スキル（AI coding、システム設計など）
- 著者・人物名
- 関連企業・組織
- 関連論文・研究
"""
```

**効果:** ⭐⭐⭐⭐⭐ （最大）  
**実装難度:** 簡単  
**所要時間:** 5分

---

### **2️⃣ 存在しない概念ページを自動生成**

**現在の問題:**
```
BACKLINKS.md で ✗ 印が付いている概念ページが作られていない
例：[[行動遺伝学]]、[[進化心理学]] など
```

**解決策: 自動スタブページ生成スクリプト**

```python
#!/usr/bin/env python3
# generate-missing-concepts.py

from pathlib import Path
import re

wiki_dir = Path("Wiki")
backlinks_file = wiki_dir / "BACKLINKS.md"

# BACKLINKS.md から ✗ の概念を抽出
missing_concepts = set()
with open(backlinks_file, 'r', encoding='utf-8') as f:
    for line in f:
        if '✗' in line and '[[' in line:
            match = re.search(r'\[\[([^\]]+)\]\]', line)
            if match:
                missing_concepts.add(match.group(1))

# スタブページを生成
for concept in missing_concepts:
    file_path = wiki_dir / f"{concept}.md"
    
    if not file_path.exists():
        content = f"""# {concept}

**ステータス:** スタブページ（自動生成）  
**作成日:** {datetime.now().strftime('%Y-%m-%d')}

---

## 定義

[このページの説明を追加してください]

---

## 関連ページ

[[概念1]], [[概念2]]

---

## 参考資料

- リンクを追加

"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {concept}.md")
```

**実行:**
```powershell
python generate-missing-concepts.py
```

**効果:** ⭐⭐⭐⭐ （リンク切れ解消）  
**実装難度:** 中程度  
**所要時間:** 30分

---

### **3️⃣ 記事間の関連性を自動検出**

**現在の問題:**
```
記事Aと記事Bが共通の概念を持っていても、
リンクが張られていない
```

**解決策: セマンティック関連性スクリプト**

```python
#!/usr/bin/env python3
# link-related-articles.py

from pathlib import Path
import re
from collections import defaultdict

wiki_dir = Path("Wiki")

# すべての記事から概念を抽出
article_concepts = {}
for md_file in wiki_dir.glob("*.md"):
    if md_file.name.startswith(("INDEX", "BACKLINKS", "MAINTENANCE")):
        continue
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # [[概念]] を抽出
    concepts = set(re.findall(r'\[\[([^\]]+)\]\]', content))
    article_concepts[md_file.stem] = concepts

# 共通概念が多い記事ペアを見つける
similarity = defaultdict(list)
articles = list(article_concepts.keys())

for i, article1 in enumerate(articles):
    for article2 in articles[i+1:]:
        common = article_concepts[article1] & article_concepts[article2]
        if len(common) >= 2:  # 2個以上の共通概念
            similarity[article1].append({
                'article': article2,
                'common_concepts': common,
                'score': len(common)
            })
            similarity[article2].append({
                'article': article1,
                'common_concepts': common,
                'score': len(common)
            })

# 結果をファイルに出力
with open(wiki_dir / "RELATED_ARTICLES.md", 'w', encoding='utf-8') as f:
    f.write("# 関連記事マップ\n\n")
    
    for article in sorted(similarity.keys()):
        f.write(f"## {article}\n\n")
        
        # スコア順にソート
        related = sorted(similarity[article], key=lambda x: x['score'], reverse=True)
        
        for rel in related:
            f.write(f"- **{rel['article']}** (共通概念: {len(rel['common_concepts'])})\n")
            f.write(f"  - 共通: {', '.join(rel['common_concepts'])}\n")
        
        f.write("\n")
```

**実行:**
```powershell
python link-related-articles.py
```

**効果:** ⭐⭐⭐⭐ （関連記事の自動検出）  
**実装難度:** 中程度  
**所要時間:** 45分

---

### **4️⃣ Obsidian Graph View を活用**

**現在の問題:**
```
バックリンクが表示されているが、
ビジュアライゼーションがない
```

**解決策: Obsidian の Graph View を使う**

```
Obsidian で:
1. グラフアイコン（左下）をクリック
2. または: Ctrl+G
3. "Open graph view"

すると:
- すべての記事がノードとして表示
- リンクがエッジとして表示
- 知識グラフが可視化される
```

**改善:**
```
Obsidian 設定 → グラフ表示設定
- ノードサイズを変更
- 色分けを設定（タグ別など）
- フォーカス距離を調整
```

**効果:** ⭐⭐⭐ （可視化・理解が進む）  
**実装難度:** 非常に簡単  
**所要時間:** 2分

---

### **5️⃣ タグシステムを追加**

**現在の問題:**
```
[[概念]] では粗い
カテゴリ分けできていない
```

**解決策: Markdown フロントマターにタグを追加**

personal-ingest.py を改善:

```python
template = f"""---
title: {title}
tags:
  - [[行動遺伝学]]
  - [[心理学]]
  - [[教育]]
created: {datetime.now().strftime('%Y-%m-%d')}
source_url: {source_url}
---

# {title}

...記事内容...
"""
```

Obsidian で:
```
検索: tag:#行動遺伝学
→ その tag を持つすべての記事を表示
```

**効果:** ⭐⭐⭐ （検索・グループ化が強化）  
**実装難度:** 簡単  
**所要時間:** 15分

---

### **6️⃣ 双方向リンク機能を強化**

**現在の問題:**
```
記事A → [[概念]]
だが、概念 → 記事A の逆リンクが自動化されていない
```

**解決策: Obsidian の Backlink パネルを活用**

```
各ページを開いて、右パネルの "Backlinks" を見る
→ そのページにリンクしているページが表示される

さらに:
1. 「リンクを追加」ボタンで手動リンク追加可能
2. グラフ表示で視覚的に確認
3. "Open local graph" で周辺ネットワークを表示
```

**効果:** ⭐⭐⭐ （関連性の発見）  
**実装難度:** 非常に簡単  
**所要時間:** 2分

---

## 🔄 推奨される実装順序

### **Phase 1: 即座に実行（今日）**
1. ✅ Obsidian Graph View を開く
   - 現在の繋がりを可視化して確認

2. ✅ 各ページの Backlinks パネルを確認
   - 既存のリンク構造を理解

### **Phase 2: スクリプト作成（今週）**
1. 📝 Claude プロンプトを改善
   - `personal-ingest.py` の prompt を強化
   - より関連性の高い概念を抽出

2. 📝 `generate-missing-concepts.py` を作成
   - orphan link を解消
   - スタブページを自動生成

3. 📝 `link-related-articles.py` を作成
   - 記事間の関連性を自動検出
   - RELATED_ARTICLES.md を生成

### **Phase 3: 最適化（来週以降）**
- タグシステムを導入
- より高度なセマンティック解析
- Claude で記事間の関連性を評価

---

## 💡 最も効果的な改善

**順位1️⃣: Claude プロンプト改善** ⭐⭐⭐⭐⭐
- 最小の努力で最大の効果
- 新しい記事すべてに適用される
- 根本的な解決

**順位2️⃣: 存在しない概念ページ自動生成** ⭐⭐⭐⭐
- orphan link を即座に解消
- ページ数が大幅に増加
- 知識グラフが充実

**順位3️⃣: 記事間の関連性自動検出** ⭐⭐⭐⭐
- 隠れた繋がりを発見
- Graph View が格段に良くなる
- セレンディピティ効果

---

## 📊 改善の見える化

### Before（現状）
```
記事1: [[概念A]], [[概念B]]
記事2: [[概念C]], [[概念D]]
記事3: [[概念E]]

❌ 概念ページが存在しない（orphan）
❌ 記事1と記事2の関連性が見えない
❌ Graph が疎である
```

### After（改善後）
```
記事1: [[概念A]], [[概念B]], [[関連する他分野]]
記事2: [[概念C]], [[概念D]], [[関連する他分野]]
記事3: [[概念E]]

✅ すべての概念ページが存在
✅ 概念ページが記事1,2をバックリンク
✅ RELATED_ARTICLES.md で記事1↔記事2の関連性を表示
✅ Graph が密である
```

---

## 🚀 すぐできること

### **今すぐ試す:**

1. **Obsidian Graph View を開く**
   ```
   Ctrl + G
   ```

2. **BACKLINKS.md を確認**
   ```
   Wiki/BACKLINKS.md を開く
   → ✗ が多い部分が改善対象
   ```

3. **各記事の Backlinks パネルを確認**
   ```
   記事を開く → 右パネル → Backlinks
   ```

---

## 📝 実装例

### プロンプト改善版（すぐ使える）

```python
prompt = f"""以下のテキストを読んで、日本語で以下を提供してください：

1. 簡潔な要約（2-3文）
2. 主要な概念（7-10個、他の記事と繋がる可能性を重視）
3. この記事の前提となる知識（他の分野から学べることなど）
4. この記事から派生する応用分野
5. 関連する著者・人物・企業
6. ソースURL

概念の例（含めるべき種類）:
- 理論：[[行動遺伝学]]、[[進化心理学]]
- 実践：[[システム設計]]、[[テスト駆動開発]]
- スキル：[[深いモジュール]]、[[ユビキタス言語]]
- 概念：[[認知的複雑さ]]、[[技術負債]]
- 人物：[[Andrej Karpathy]]、[[Matt Pocock]]
- 組織：[[Anthropic]]、[[Google]]

---
{content}
---

JSON形式で以下のように返してください：
{{
    "summary": "要約",
    "concepts": ["[[概念1]]", "[[概念2]]", ...],
    "prerequisites": ["[[前提知識1]]", "[[前提知識2]]"],
    "applications": ["[[応用分野1]]", "[[応用分野2]]"],
    "related_people": ["[[人物1]]", "[[人物2]]"],
    "source_url": "url または null"
}}"""
```

---

## ✨ 期待される効果

| 処置 | 効果 | 難度 | 時間 |
|---|---|---|---|
| Prompt 改善 | ⭐⭐⭐⭐⭐ | 簡単 | 5分 |
| スタブ生成 | ⭐⭐⭐⭐ | 中 | 30分 |
| 関連性検出 | ⭐⭐⭐⭐ | 中 | 45分 |
| Graph View | ⭐⭐⭐ | 簡単 | 2分 |
| タグ追加 | ⭐⭐⭐ | 簡単 | 15分 |

---

**推奨:** まずはプロンプト改善から始めるのが最も効率的です！
