"""
save_screenshot.py

投稿デバッグ用の補助構造。
本文取得に失敗した投稿のスクリーンショットとHTMLソースを保存する責任を持つ。

主に fetch_post_texts から呼び出される想定。
"""

from selenium.webdriver.remote.webdriver import WebDriver
from pathlib import Path
import logging
from urllib.parse import urlparse

def extract_post_id(url: str) -> str:
    """
    投稿URLから投稿ID（末尾の文字列）を抽出する
    """
    return urlparse(url).path.strip("/").split("/")[-1]

def save_screenshot_and_html(driver: WebDriver, post_url: str) -> None:
    """
    指定された投稿のスクリーンショットとHTMLを保存する。

    Parameters:
        driver (WebDriver): SeleniumのWebDriverインスタンス
        post_url (str): 投稿URL（ID抽出に使用）
    """
    post_id = extract_post_id(post_url)

    # --- スクリーンショット保存 ---
    ss_dir = Path("screenshot")
    ss_dir.mkdir(parents=True, exist_ok=True)
    ss_path = ss_dir / f"{post_id}.png"
    driver.save_screenshot(str(ss_path))
    logging.debug(f"📸 スクリーンショット保存: {ss_path}")

    # --- HTMLソース保存 ---
    html_dir = Path("html_dump")
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"{post_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logging.debug(f"📝 HTMLソース保存: {html_path}")
