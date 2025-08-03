"""
normalize_urls.py
商品URLを一意な商品IDとして正規化するモジュール

このモジュールは以下の責任を持つ：
1. 抽出されたAmazon・楽天・YahooのURLを正規化する
2. AmazonはASIN、楽天は商品コード、YahooはitemIDを抽出
3. 集計処理において「同一商品としてカウント」できるように整形
"""

import re

def normalize_url(url: str, log=None) -> str:
    """
    商品URLを正規化して商品単位に変換する
    結果は 'amazon:B0XXXXXXX' や 'rakuten:shop/item' 形式

    Parameters:
        url (str): 元のURL
        log (function, optional): ログ出力用関数

    Returns:
        str: 正規化後の商品ID
    """

    if log:
        log(f"🌀 normalize_url() ▶ URL: {url}")

    # --- Amazon URL処理 ---
    amazon_match = re.search(r'/dp/([A-Z0-9]{10})|/gp/product/([A-Z0-9]{10})', url)
    if amazon_match:
        asin = amazon_match.group(1) or amazon_match.group(2)
        norm = f"amazon:{asin}"
        if log:
            log(f"✅ Amazon ASIN抽出成功 ▶ {norm}")
        return norm

    # --- 楽天 URL処理（itemコード） ---
    rakuten_match = re.search(r'rakuten\.co\.jp/([^/?#]+/[^/?#]+)', url)
    if rakuten_match:
        item_code = rakuten_match.group(1)
        norm = f"rakuten:{item_code}"
        if log:
            log(f"✅ 楽天商品コード抽出成功 ▶ {norm}")
        return norm

    # --- Yahooショッピング URL処理 ---
    yahoo_match = re.search(r'yahoo\.co\.jp/[^/]+/item/([a-zA-Z0-9\-_]+)', url)
    if yahoo_match:
        item_id = yahoo_match.group(1)
        norm = f"yahoo:{item_id}"
        if log:
            log(f"✅ Yahoo itemID 抽出成功 ▶ {norm}")
        return norm

    # --- 規格外URL（正規化失敗） ---
    if log:
        log(f"⚠️ 正規化できないURL ▶ {url}（形式不明としてそのまま使用）")

    return url
