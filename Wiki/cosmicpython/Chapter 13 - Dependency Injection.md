# Chapter 13 — Dependency Injection (and Bootstrapping)

**原文：** [GitHub で読む](https://github.com/cosmicpython/book/blob/master/chapter_13_dependency_injection.asciidoc)  
**← [[cosmicpython/Chapter 12 - CQRS|Ch.12]]** | **次 → [[cosmicpython/Epilogue|Epilogue]]**  
**← [[cosmicpython/index|目次に戻る]]**

---

## この章について

本書のアーキテクチャを完成させる **依存性注入（DI）** と **Bootstrap スクリプト** を導入。  
暗黙的な依存を明示的に配線することで、テスタビリティと柔軟性を最大化する。

---

## キーコンセプト

- **依存性注入** — 必要な依存を外から渡すことで、クラス/関数を再利用可能に
- **Bootstrap** — アプリ起動時に全依存を組み立てる単一の場所
- DI コンテナ vs 手動配線のトレードオフ

---

## コードパターン

```python
def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    send_mail: Callable = email.send,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
    if start_orm:
        orm.start_mappers()
    dependencies = {"uow": uow, "send_mail": send_mail, "publish": publish}
    injected_event_handlers = {
        event_type: [inject_dependencies(handler, dependencies) for handler in handlers]
        for event_type, handlers in handlers.EVENT_HANDLERS.items()
    }
    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
```

---

## キーポイント

- [ ] 読んでメモを追加する

---

## 自分のメモ

---

## 引っかかった点・疑問
