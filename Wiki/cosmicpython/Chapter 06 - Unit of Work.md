# Chapter 06 — Unit of Work Pattern

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_06_uow.asciidoc)  
**← [[cosmicpython/Chapter 05 - High Gear Low Gear|Ch.05]]** | **次 → [[cosmicpython/Chapter 07 - Aggregate|Ch.07]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

データベーストランザクションをドメイン寄りに抽象化する **Unit of Work（UoW）パターン** を導入。  
Repository と組み合わせて、アトミックな操作を表現するコンテキストマネージャを構築する。

---

## キーコンセプト

- **Unit of Work** — 一連の操作をひとつの作業単位として管理するパターン
- `with uow:` コンテキストマネージャで commit / rollback を自動化
- Service Layer への注入による疎結合の実現

---

## コードパターン

```python
class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
