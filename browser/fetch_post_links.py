"""
fetch_post_links.py

Instagramタグページから投稿リンク一覧を収集するモジュール

このモジュールは以下の責任を持つ：
1. 指定タグページへアクセス
2. ページを数回スクロールして投稿を読み込む
3. 投稿リンク（/p/〜形式）を抽出し、最大 max_posts 件返す
4. 抽出内容・スクロール段階・HTML構造の解析状況をログに詳細記録する
"""

import time
from bs4 import BeautifulSoup
from selenium.webdriver.edge.webdriver import WebDriver

def get_post_links(driver: WebDriver, tag: str, log, max_posts: int = 5) -> list[str]:
    """
    指定タグページにアクセスし、投稿リンクを最大 max_posts 件まで抽出

    Parameters:
        driver (WebDriver): selenium の Edge WebDriver
        tag (str): 対象ハッシュタグ（例: 楽天room）
        log (function): ログ出力関数
        max_posts (int): 取得件数の上限

    Returns:
        list[str]: 投稿リンクのURL一覧（最大 max_posts 件）
    """

    log("🟡 get_post_links() 開始")

    # --- タグページにアクセス ---
    url = f"https://www.instagram.com/explore/tags/{tag}/"
    log(f"🌐 タグページへアクセス中: {url}")
    driver.get(url)
    time.sleep(5)  # 初回読み込みを待機

    # --- スクロールして投稿を読み込む ---
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        log(f"↕️ ページ下端までスクロール ({i+1}/3)")
        time.sleep(2)

    # --- HTMLを解析して投稿リンク抽出 ---
    log("🔍 投稿リンクを解析中（/p/ 形式を対象）")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/p/"):
            full_link = f"https://www.instagram.com{href}"
            if full_link not in links:
                links.append(full_link)

    log(f"✅ 全抽出リンク数: {len(links)} 件（上限 {max_posts} 件）")

    if links:
        preview = links[:3]
        log(f"📎 抽出された投稿リンク（先頭3件）:\n" + "\n".join(preview))
    else:
        log("⚠️ /p/ 投稿リンクが1件も見つかりませんでした")

    return links[:max_posts]
