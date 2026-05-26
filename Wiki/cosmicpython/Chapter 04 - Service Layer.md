# Chapter 04 — Our First Use Case: Flask API and Service Layer

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_04_service_layer.asciidoc)  
**← [[cosmicpython/Chapter 03 - Abstractions|Ch.03]]** | **次 → [[cosmicpython/Chapter 05 - High Gear Low Gear|Ch.05]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

Flask エンドポイントとドメインロジックの間に **Service Layer** を挟み、  
ユースケースをオーケストレーションする薄いレイヤーを構築する。

---

## キーコンセプト

- **Service Layer** — HTTPやDBの詳細を知らず、ユースケースだけを表現する
- ドメインサービス vs アプリケーションサービスの違い
- E2Eテスト → Service Layerテスト → ドメインテストのピラミッド

---

## コードパターン

```python
def allocate(orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not any(b.sku == sku for b in batches):
            raise InvalidSku(f"Invalid sku {sku}")
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
