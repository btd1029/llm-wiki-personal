# Effective Harnesses For Long Running Agents

**ファイルパス：** Wiki/Effective harnesses for long-running agents.md
**作成日：** 2026-05-22
**出典：** C:\Users\bitet\llm-wiki-personal\raw\Effective harnesses for long-running agents.md

---

## 概要

長時間稼働するAIエージェントが複数のコンテキストウィンドウにまたがって一貫した進捗を維持するための課題と解決策を提示した記事。Anthropicは「初期化エージェント」と「コーディングエージェント」の二段構成ハーネスを開発し、機能リストファイル・進捗ログ・gitコミット履歴を活用して各セッション間の情報伝達を実現した。インクリメンタルな進捗管理、ブラウザ自動化によるエンドツーエンドテスト、環境をクリーンな状態に保つプラクティスが、エージェントの主要な失敗モードを大幅に軽減することを示した。

---

## 主要な概念

- [[長時間稼働エージェント]]
- [[コンテキストウィンドウ管理]]
- [[マルチセッションエージェント設計]]
- [[インクリメンタル開発]]
- [[エージェントハーネス]]
- [[コンテキストコンパクション]]
- [[エージェントの失敗モード]]

---

## 前提となる知識

- [[LLMのコンテキストウィンドウ]]
- [[AIエージェントアーキテクチャ]]
- [[Git バージョン管理]]
- [[プロンプトエンジニアリング]]
- [[ブラウザ自動化（Puppeteer）]]

---

## 内容

---
title: "Effective harnesses for long-running agents"
source: "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"
author:
published:
created: 2026-05-18
description: "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems."
tags:
  - "clippings"
---
As AI agents become more capable, developers are increasingly asking them to take on complex tasks requiring work that spans hours, or even days. However, getting agents to make consistent progress across multiple context windows remains an open problem.

The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before. Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift. Because context windows are limited, and because most complex projects cannot be complet...

[続きはこちら](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

---

## 派生する応用分野

- [[自律的ソフトウェア開発]]
- [[科学研究の長期タスク自動化]]
- [[マルチエージェントシステム設計]]
- [[金融モデリングの自動化]]
- [[CI/CDパイプラインへのエージェント統合]]

---

## 関連する人物・企業

[[Anthropic]], [[Justin Young]], [[David Hershey]], [[Claude Agent SDK]]

---

## 個人メモ

[あなたの感想・思いつきをここに記録]

---

## 次のアクション

- [ ] 内容の詳細版を追加
- [ ] 他の記事とバックリンクを接続
- [ ] タグを追加
