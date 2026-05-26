# Chapter 12 — Command-Query Responsibility Segregation (CQRS)

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_12_cqrs.asciidoc)  
**← [[cosmicpython/Chapter 11 - External Events|Ch.11]]** | **次 → [[cosmicpython/Chapter 13 - Dependency Injection|Ch.13]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

読み取り（Query）と書き込み（Command）のモデルを分離する **CQRS** パターンを実装する。  
読み取り専用の「ビュー」を直接 SQL で書くことでパフォーマンスと単純さを両立する。

---

## キーコンセプト

- **CQRS** — コマンド（書き込み）とクエリ（読み取り）でモデルを分離
- Read Model（Query Side）は ORM/Repository を使わず直接 SQL でよい
- Write Model の複雑さをクエリ側に持ち込まない

---

## コードパターン

```python
# Read side: シンプルな SQL クエリ直書き
def allocations(orderid: str, uow: SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            "SELECT ol.sku, b.reference FROM allocations AS a"
            " JOIN order_lines AS ol ON a.orderlineid = ol.id"
            " JOIN batches AS b ON a.batchid = b.id"
            " WHERE ol.orderid = :orderid",
            dict(orderid=orderid),
        )
        return [{"sku": sku, "batchref": batchref} for sku, batchref in results]
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
