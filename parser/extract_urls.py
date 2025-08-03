"""
extract_urls.py

投稿本文から商品リンクを抽出するモジュール（正規表現）

この構造は以下の責任を持つ：
1. テキスト中に埋め込まれたURLを正規表現で検出
2. 現時点では Amazon / 楽天 / Yahoo ショッピングに対応
3. 各マッチパターンごとに何件ヒットしたかをログで記録
"""

import re

def extract_affiliate_urls(text: str, log=None) -> list[str]:
    """
    投稿本文からAmazon・楽天・Yahoo系の商品URLを抽出して返す

    Parameters:
        text (str): 投稿本文
        log (function, optional): ログ出力関数

    Returns:
        list[str]: 対象ドメインにマッチする商品URLリスト
    """

    if log:
        log("🟡 extract_affiliate_urls() 開始")
        log(f"📋 本文文字数: {len(text)}")

    urls = []

    # --- 対象ドメインごとの抽出パターン定義 ---
    patterns = [
        ("Amazon", r'https?://(?:www\.)?amazon\.co\.jp/[^\s\'")]+'),
        ("楽天",    r'https?://(?:item\.rakuten\.co\.jp|a\.rakuten\.co\.jp)[^\s\'")]+'),
        ("Yahoo",  r'https?://(?:shopping\.yahoo\.co\.jp|store\.shopping\.yahoo\.co\.jp|paypaymall\.yahoo\.co\.jp)[^\s\'")]+'),
    ]

    # --- 各パターンごとにURL抽出 ---
    for label, pattern in patterns:
        found = re.findall(pattern, text)
        if found:
            urls.extend(found)
            if log:
                log(f"✅ {label} リンク検出: {len(found)} 件")
                for u in found[:3]:
                    log(f"   - {u}")
        else:
            if log:
                log(f"🚫 {label} リンクなし")

    if log:
        log(f"📦 抽出された全URL数: {len(urls)}")
        if len(urls) == 0:
            log("⚠️ 対象URLが1件も抽出されませんでした")

    return urls
