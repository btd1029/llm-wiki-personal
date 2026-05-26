# Chapter 10 — Commands and Command Handler

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_10_commands.asciidoc)  
**← [[cosmicpython/Chapter 09 - All Messagebus|Ch.09]]** | **次 → [[cosmicpython/Chapter 11 - External Events|Ch.11]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

**Command** と **Event** を明確に区別する。  
Command は「何かをしてほしいという意図」、Event は「何かが起きた事実」という違いを理解する。

---

## キーコンセプト

- **Command** — 意図・指示（例: `AllocateCommand`）、失敗が許される
- **Event** — 過去の事実（例: `Allocated`）、複数ハンドラーが扱える
- Command/Event 分離によるシステムの意図の明確化

---

## コードパターン

```python
@dataclass
class Allocate(Command):
    orderid: str
    sku: str
    qty: int

@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
