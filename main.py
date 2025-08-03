"""
main.py
Instagramアフィリエイト巡回の全体制御スクリプト（実行エントリーポイント）

このスクリプトは以下の責任を持つ：
1. .envから設定を読み込み
2. Instagramへログインし、指定タグの投稿を巡回
3. 各投稿から楽天アフィリエイトURLを抽出・正規化
4. URLの登場回数を集計し、商品名を取得
5. 商品名 / 回数 / URL で構成されたCSVを出力
6. 全処理のログをファイルに保存
"""

from dotenv import load_dotenv
from browser.instagram_login import login_and_get_driver
from browser.fetch_post_links import get_post_links
from browser.fetch_post_texts import get_post_texts
from parser.extract_urls import extract_affiliate_urls
from parser.normalize_urls import normalize_url
from parser.fetch_titles import add_product_titles  # ✅ 商品名取得ステップ
from aggregator.count_urls import count_normalized_urls
from aggregator.export_to_csv import export_csv
from util.logger import setup_logger

import os
from datetime import datetime
from pathlib import Path

# --- 初期設定：環境変数・タイムスタンプ ---
load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USER")
PASSWORD = os.getenv("INSTAGRAM_PASS")
TARGET_TAG = os.getenv("TARGET_TAG", "楽天room")
MAX_POSTS = int(os.getenv("MAX_POSTS", 5))

now = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- ログディレクトリとロガー初期化 ---
log_dir = Path("log")
log_dir.mkdir(parents=True, exist_ok=True)
log = setup_logger(log_dir / f"log_{now}.txt")
log(f"📁 ログファイル作成")

# --- Instagramログイン ---
log("🚀 Instagramログイン処理を開始します")
driver = login_and_get_driver(USERNAME, PASSWORD, log)

try:
    # --- タグページの投稿リンクを取得 ---
    log("📌 タグ巡回を開始します")
    post_links = get_post_links(driver, TARGET_TAG, log, max_posts=MAX_POSTS)

    # --- 各投稿ページから本文を取得 ---
    log("📌 各投稿の本文を取得します")
    post_texts = get_post_texts(driver, post_links, max_count=MAX_POSTS)

    # --- 本文から楽天アフィリエイトURLを抽出・正規化 ---
    all_urls = []
    for i, post in enumerate(post_texts):
        log(f"🔎 [{i+1}/{len(post_texts)}] 投稿本文からリンク抽出中")

        # ⭐ 本文の先頭だけ確認ログ（多すぎると煩雑なので80文字制限）
        log(f"📝 本文抜粋: {post['text'][:80].replace('\n', ' ')}...")

        urls = extract_affiliate_urls(post["text"])
        normed = [normalize_url(u) for u in urls]
        
        if normed:
            log(f"✅ 抽出されたリンク: {normed}")
        else:
            log("ℹ️ 商品リンクは見つかりませんでした")
        all_urls.extend(normed)

    # --- URLごとの登場回数を集計 ---
    log("📊 商品リンクの出現回数を集計します")
    count_df = count_normalized_urls(all_urls, log)

    # --- 各URLから商品タイトルを取得して列追加 ---
    log("📌 各URLから商品タイトルを取得します")
    count_df = add_product_titles(count_df, log)

    # --- CSVに保存（成果物出力）---
    log("💾 結果をCSVとして保存します")
    export_csv(count_df, now, log)

except Exception as e:
    log(f"💥 処理中にエラーが発生しました: {e}")

finally:
    # --- ドライバ終了処理 ---
    driver.quit()
    log("🛑 ブラウザを終了しました")
    log("🎉 全処理が完了しました")
