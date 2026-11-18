# devin-cloud-train

Devin Cloud に関する定例会資料と業務自動化スクリプトをまとめるリポジトリです。

## TIFF 一括 PDF 変換

図面保管フォルダ配下の `.tif` / `.tiff` を再帰的に検索し、同じフォルダへ同名の `.pdf` として変換します。既存 PDF はスキップし、元 TIFF は削除しません。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tiff_to_pdf.py "C:\図面保管フォルダ" --csv "C:\図面保管フォルダ\tiff_to_pdf_results.csv"
```

主なオプション:

| オプション | 説明 |
| --- | --- |
| `--csv PATH` | 処理結果 CSV の出力先。既定は `tiff_to_pdf_results.csv` |
| `--log-file PATH` | 任意のログファイル出力先 |
| `--dry-run` | 変換せず対象一覧とスキップ判定だけを CSV に出力 |

変換した PDF は `pypdf` で開けることを確認してから保存します。TIFF に DPI 情報がない場合は 300 DPI として PDF ページサイズを決めます。

## 定例会資料

| 日付 | テーマ | 資料 |
| --- | --- | --- |
