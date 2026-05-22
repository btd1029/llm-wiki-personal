# API キーを環境変数に設定するコマンド

## 前提条件
新しい API キーをすでに取得していることが前提です。  
https://console.anthropic.com/account/keys から新しいキーを生成してください。

---

## 方法 1: PowerShell（推奨）

**管理者として PowerShell を開いて、以下を実行:**

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-YOUR_KEY_HERE", "User")
```

`sk-ant-api03-YOUR_KEY_HERE` の部分をあなたの新しいAPIキーに置き換えてください。

**例:**
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-abc123xyz789def", "User")
```

### 確認コマンド

新しい PowerShell ウィンドウを開いて実行:

```powershell
$env:ANTHROPIC_API_KEY
```

出力: `sk-ant-api03-abc123xyz789def` (あなたのキー)

---

## 方法 2: Windows コマンドプロンプト

**管理者として cmd.exe を開いて実行:**

```cmd
setx ANTHROPIC_API_KEY "sk-ant-api03-YOUR_KEY_HERE"
```

**例:**
```cmd
setx ANTHROPIC_API_KEY "sk-ant-api03-abc123xyz789def"
```

出力: `成功: 指定されたレジストリ キーが保存されました`

### 確認コマンド

新しいコマンドプロンプトを開いて:

```cmd
echo %ANTHROPIC_API_KEY%
```

---

## 方法 3: 手動で環境変数を設定（UI）

1. Windows キー + X → **システム**
2. 右側の **詳細情報** をクリック
3. **環境変数** をクリック
4. **新規** をクリック
5. 変数名: `ANTHROPIC_API_KEY`
6. 変数値: `sk-ant-api03-...` (あなたのキー)
7. **OK** を 3 回クリック
8. PC を再起動

---

## 設定後のテスト

```powershell
cd C:\Users\bitet\llm-wiki-personal
python personal-ingest.py --source raw/test-article-with-url.md
```

期待される出力:
```
✅ ファイルを読み込み中...
✅ Claude で要約を生成中...
✅ Wiki エントリを生成中...
✅ Wiki に保存中...

✅ 成功！
```

---

## トラブルシューティング

### 「API key not found」エラーが出る場合

**解決策:**
1. PowerShell/cmd を完全に閉じる
2. **新しい** PowerShell ウィンドウを開く
3. 確認コマンドを実行: `echo $env:ANTHROPIC_API_KEY`
4. キーが表示されない場合は、設定コマンドを再実行

### スペースが含まれている場合

キーを引用符で囲んでください（上の例では既に引用符があります）:
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-your-key-with-spaces", "User")
```

### 古いキーを削除したい場合

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "", "User")
```

---

## セキュリティに関する注意

⚠️ **重要:**
- API キーをスクリプトやファイルに書き込まない
- Git にコミットしない
- 他人と共有しない
- 環境変数に設定したら、コマンドラインの履歴から削除する

```powershell
# 履歴をクリア（オプション）
Clear-History
```

---

**キーが設定されたら、wiki システムの全機能が動作します！🚀**
