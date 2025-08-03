"""
count_urls.py

正規化された商品URLリストを集計し、ランキング形式のDataFrameを返すモジュール。

この構造は以下の責任を持つ：
1. 正規化済みの商品URLリストを集計（collections.Counter）
2. pandas.DataFrameに変換し、出現回数で降順ソート
3. 処理過程・カウント結果・DataFrame構成をログで出力（デバッグ用）
"""

from collections import Counter
import pandas as pd

def count_normalized_urls(url_list: list[str], log=None) -> pd.DataFrame:
    """
    正規化済みURLリストを集計して、出現回数順のDataFrameを返す

    Parameters:
        url_list (list[str]): normalize_url() 済みのURL群
        log (function, optional): ログ出力関数

    Returns:
        pd.DataFrame: 商品ID / 登場回数 のDataFrame（降順）
    """

    if log:
        log("🟡 count_normalized_urls() 開始")
        log(f"📥 入力URL数: {len(url_list)}")
        if len(url_list) <= 10:
            log(f"🧾 URL一覧: {url_list}")
        else:
            log(f"🧾 URLサンプル（先頭5件）: {url_list[:5]} ...")

    # --- URLごとの出現回数をカウント ---
    counter = Counter(url_list)
    if log:
        log(f"📊 ユニークURL数（商品数）: {len(counter)}")

    # --- pandas DataFrameに変換 ---
    df = pd.DataFrame(counter.items(), columns=["商品ID", "登場回数"])
    if log:
        log("🧱 DataFrame 生成完了")
        log(f"🔢 最初の3行:\n{df.head(3).to_string(index=False)}")

    # --- 登場回数で降順に並べる ---
    df = df.sort_values("登場回数", ascending=False).reset_index(drop=True)
    if log:
        log("✅ ソート＆リセット完了")
        log(f"📄 出力行数: {len(df)}")

    return df
