# すべての記事を処理するスクリプト

$rawFolder = "raw"
$processedCount = 0
$errorCount = 0

Write-Host "=================================================="
Write-Host "🚀 全記事の要約とリンク生成を開始"
Write-Host "=================================================="
Write-Host ""

# raw フォルダ内のすべての .md ファイルを処理
Get-ChildItem -Path $rawFolder -Filter "*.md" | ForEach-Object {
    $file = $_.FullName
    $fileName = $_.Name

    Write-Host "📄 処理中: $fileName"

    try {
        python personal-ingest.py --source $file
        $processedCount++
        Write-Host "   ✅ 完了`n"
    } catch {
        Write-Host "   ❌ エラー: $_`n"
        $errorCount++
    }
}

Write-Host "=================================================="
Write-Host "📊 完了"
Write-Host "=================================================="
Write-Host "✅ 成功: $processedCount"
Write-Host "❌ エラー: $errorCount"
Write-Host ""
Write-Host "生成されたファイル: Wiki/ フォルダを確認してください"
Write-Host "=================================================="
