"""
fetch_post_texts.py

各投稿ページにアクセスし、投稿本文を取得する責任を持つ構造。
本文はすべての <span> 要素から抽出し、結合して判定を行う。

対象は「https://a.rakuten.co.jp/」を含む投稿のみ。
該当がある場合は本文とURLを記録。

ログ出力あり：
- 処理開始・アクセスURL・本文抽出の詳細
- 楽天リンク含有判定・保存処理・抽出失敗理由
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import time

# 投稿本文のspan要素のclassに含まれるキーワード
TARGET_CLASS_KEY = "x193iq5w"

def get_post_texts(driver: WebDriver, post_links: list[str], max_count: int = 5) -> list[dict]:
    """
    投稿本文を取得し、楽天リンクを含む投稿のみ返す

    Parameters:
        driver (WebDriver): SeleniumのWebDriverインスタンス
        post_links (list[str]): 投稿リンクのリスト
        max_count (int): 最大取得件数（.envのMAX_POSTSが反映される）

    Returns:
        list[dict]: [{'url': 投稿URL, 'text': 本文テキスト}]
    """
    try:
        max_count = int(max_count)
    except Exception as e:
        logging.error(f"❌ max_count の型変換に失敗しました: {e}")
        return []

    result = []
    logging.info(f"📌 投稿本文の抽出処理を開始（最大 {max_count} 件）")

    for idx, link in enumerate(post_links[:max_count], 1):
        logging.info(f"🌐 [{idx}/{max_count}] 投稿ページへアクセス中: {link}")
        try:
            driver.get(link)
            time.sleep(2)

            # --- 全ての該当span要素を取得 ---
            span_elements = driver.find_elements(By.XPATH, f"//span[contains(@class, '{TARGET_CLASS_KEY}')]")
            logging.debug(f"🔍 抽出されたspan要素数: {len(span_elements)}")

            # --- テキスト結合 ---
            post_text = "\n".join(
                span.text.strip() for span in span_elements if span.text.strip()
            )
            logging.debug(f"📝 結合後テキスト先頭: {post_text[:60]}...")

            # --- 楽天リンク含有チェック ---
            if "https://a.rakuten." in post_text:
                logging.info("✅ 楽天リンクを含む投稿として抽出")
                result.append({"url": link, "text": post_text})
            else:
                logging.info("🚫 楽天リンクを含まないためスキップ")
                logging.debug(f"📭 本文全文:\n{post_text}")

        except NoSuchElementException:
            logging.warning("⚠️ 本文要素が見つかりません（NoSuchElement）")
        except TimeoutException:
            logging.error("⏱ ページ読み込みタイムアウト")
        except Exception as e:
            logging.error(f"❌ 予期しないエラー発生: {type(e).__name__} ▶ {e}")

    logging.info(f"📦 本文抽出完了：楽天リンク付き投稿 {len(result)} 件")
    return result
