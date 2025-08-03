import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_title_from_url(url: str, log=None) -> str:
    """
    単一URLに対して商品タイトルを取得する
    優先順位：<meta property="og:title"> → <title>
    """

    if log:
        log(f"🟡 fetch_title_from_url() ▶ 開始 URL: {url}")
        log("🌐 リクエスト送信準備...")

    try:
        res = requests.get(url, timeout=10)

        # --- 念のため文字コード補正 ---
        res.encoding = res.apparent_encoding

        # --- ステータスコード確認 ---
        if log:
            log(f"📡 ステータスコード: {res.status_code}")
        if res.status_code != 200:
            if log:
                log(f"⚠️ HTTPエラー発生（code={res.status_code}）")
                # 応答内容の一部表示（文字化け対策付き）
                snippet = res.text[:100].replace("\n", " ").strip()
                log(f"🧾 HTML抜粋: {snippet} ...")
            return "タイトル取得失敗"

        # --- HTMLパース ---
        soup = BeautifulSoup(res.text, "html.parser")

        # --- og:title 抽出 ---
        og_tag = soup.find("meta", property="og:title")
        if og_tag:
            og_title = og_tag.get("content", "").strip()
            if og_title:
                if log:
                    log(f"✅ og:title 抽出成功 ▶ {og_title}")
                return og_title
            else:
                if log:
                    log("⚠️ og:titleタグは存在するが中身が空")

        # --- fallback: titleタグ ---
        if soup.title:
            if soup.title.string:
                title_text = soup.title.string.strip()
                if title_text:
                    if log:
                        log(f"✅ <title> タグから抽出 ▶ {title_text}")
                    return title_text
                else:
                    if log:
                        log("⚠️ <title> タグが空")
            else:
                if log:
                    log("⚠️ <title> タグに文字列が存在しない")
        else:
            if log:
                log("⚠️ <title> タグ自体が存在しない")

        return "タイトル不明"

    except Exception as e:
        if log:
            log(f"❌ 例外発生 ▶ {type(e).__name__}: {e}")
        return "取得エラー"


def add_product_titles(df: pd.DataFrame, log) -> pd.DataFrame:
    """
    集計済みURLのDataFrameに対して、商品タイトル列を追加する

    Parameters:
        df (pd.DataFrame): '商品ID'（=URL）と '登場回数' を含むDataFrame
        log (function): ログ出力用関数

    Returns:
        pd.DataFrame: '商品名' 列を追加したDataFrame（列順：商品名 / 登場回数 / 商品ID）
    """

    titles = []
    total = len(df)

    log(f"📌 商品タイトル取得を開始します（全 {total} 件）")

    for i, row in df.iterrows():
        url = row["商品ID"]
        log(f"\n🔗 [{i+1}/{total}] 対象URL: {url}")

        title = fetch_title_from_url(url, log)
        log(f"📝 タイトル結果: {title}")

        time.sleep(1.2)  # 通信間隔確保
        titles.append(title)

    df["商品名"] = titles
    df = df[["商品名", "登場回数", "商品ID"]]  # 列順調整

    log("✅ 商品タイトル列の追加が完了しました")
    return df
