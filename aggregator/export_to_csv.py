"""
export_to_csv.py

商品集計結果をCSVファイルとして保存するモジュール

このモジュールは以下の責任を持つ：
- 出力先「csv/」ディレクトリを自律的に管理
- ファイル名にタイムスタンプ（now）を使用して一意化
- CSV保存前の内容確認とファイル出力の成功/失敗を詳細ログに記録
"""

from pathlib import Path
import pandas as pd

def export_csv(df: pd.DataFrame, now: str, log) -> None:
    """
    集計済みDataFrameをCSVファイルに保存し、ログに記録する

    Parameters:
        df (pd.DataFrame): 集計結果データ（列: 商品名 / 登場回数 / 商品ID）
        now (str): タイムスタンプ（ファイル識別用）
        log (function): ログ出力用関数
    """

    log("🟡 export_csv() 開始")

    # --- 保存ディレクトリ（csv/）の準備 ---
    csv_dir = Path("csv")
    if not csv_dir.exists():
        csv_dir.mkdir(parents=True, exist_ok=True)
        log(f"📂 ディレクトリ 'csv/' を新規作成")
    else:
        log(f"📂 ディレクトリ 'csv/' は既に存在")

    # --- ファイル名の生成 ---
    filename = f"商品ランキング_{now}.csv"
    csv_path = csv_dir / filename
    log(f"📌 出力ファイル名: {csv_path}")

    # --- 出力前にDataFrame内容を確認 ---
    log(f"📋 出力対象データ件数: {len(df)} 行")
    if len(df) == 0:
        log("⚠️ DataFrameが空です。空のCSVが出力されます。")
    else:
        preview = df.head(3).to_string(index=False)
        log(f"📄 プレビュー（先頭3件）:\n{preview}")

    # --- CSVファイルの出力処理 ---
    try:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        log(f"✅ CSV出力完了: {csv_path}")
    except Exception as e:
        log(f"❌ CSV出力中にエラーが発生しました: {type(e).__name__} ▶ {e}")
        raise
