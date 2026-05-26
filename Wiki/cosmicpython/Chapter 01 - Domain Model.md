# Chapter 01 — Domain Modelling

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_01_domain_model.asciidoc)  
**← [[cosmicpython/Introduction|Introduction]]** | **次 → [[cosmicpython/Chapter 02 - Repository|Ch.02]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

ビジネスロジックを純粋なPythonオブジェクトとして表現する「ドメインモデル」を構築する。  
フレームワークや DB に依存しない Entity・Value Object・ビジネスルールの実装を学ぶ。

---

## キーコンセプト

- **Entity** — 同一性（identity）を持つオブジェクト（例: `Batch`）
- **Value Object** — 属性だけで定義され、同一性を持たないオブジェクト（例: `OrderLine`）
- **Domain Service** — どのオブジェクトにも属さないロジック

---

## コードパターン

```python
# Value Object の例（不変・等値比較は属性ベース）
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

# Entity の例（同一性は参照ベース）
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.eta = eta
        self._allocations: Set[OrderLine] = set()
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
