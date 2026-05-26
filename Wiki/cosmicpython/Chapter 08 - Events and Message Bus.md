# Chapter 08 — Events and the Message Bus

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_08_events_and_message_bus.asciidoc)  
**← [[cosmicpython/Chapter 07 - Aggregate|Ch.07]]** | **次 → [[cosmicpython/Chapter 09 - All Messagebus|Ch.09]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

Part 2 の開幕。ドメインイベントと **Message Bus** を導入し、  
副作用（メール送信など）をドメインロジックから切り離す方法を学ぶ。

---

## キーコンセプト

- **Domain Event** — 「何かが起きた」という過去の事実を表すオブジェクト
- **Message Bus** — イベントを受け取り、対応するハンドラーを呼び出すディスパッチャ
- イベントによる副作用の疎結合化

---

## コードパターン

```python
@dataclass
class OutOfStock(Event):
    sku: str

class MessageBus:
    def handle(self, event: Event):
        for handler in HANDLERS[type(event)]:
            handler(event)
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
