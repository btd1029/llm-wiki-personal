# Chapter 02 — Repository Pattern

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_02_repository.asciidoc)  
**← [[cosmicpython/Chapter 01 - Domain Model|Ch.01]]** | **次 → [[cosmicpython/Chapter 03 - Abstractions|Ch.03]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

ドメインモデルをストレージの詳細から切り離す **Repository パターン** を導入する。  
SQLAlchemy を使いながら、ドメインがDBを「知らない」状態を実現する方法を学ぶ。

---

## キーコンセプト

- **Repository パターン** — ストレージへのアクセスをコレクション風インターフェースに抽象化
- **ORM を逆から使う** — Model が ORM に依存するのでなく、ORM が Model にマッピングする
- **Ports and Adapters（六角形アーキテクチャ）** の最初の例

---

## コードパターン

```python
class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
