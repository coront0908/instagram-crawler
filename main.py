from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from pathlib import Path

# --- ログ機構の設定 ---
now = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path("log")
log_dir.mkdir(parents=True, exist_ok=True)
log_file_path = log_dir / f"log_{now}.txt"

def log(msg: str):
    print(msg)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log(f"📁 ログファイル作成: {log_file_path}")

# --- .env読み込み ---
load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USER")
PASSWORD = os.getenv("INSTAGRAM_PASS")
TARGET_TAG = os.getenv("TARGET_TAG", "楽天room")
MAX_POSTS = int(os.getenv("MAX_POSTS", 5))

# --- Edge起動オプション設定 ---
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)

try:
    # --- Instagramログイン画面へ ---
    log("🔐 ログインページへアクセス中...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    log(f"🌐 現在URL: {driver.current_url}")

    # --- ログイン情報入力 ---
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    log("🔄 Enter押下 → ログインリクエスト送信")

    # --- URL変化でログイン判定（最大3秒） ---
    for i in range(3):
        time.sleep(1)
        current = driver.current_url
        log(f"⏱️ {i+1}s: 現在URL ➜ {current}")
        if "/accounts/login/" not in current:
            log("✅ URL遷移を検出 ➜ ログイン成功の可能性あり")
            break
    else:
        log("❌ URLが変化せず、ログイン遷移が発生していない")
        raise Exception("ログイン後の遷移が確認できませんでした")

    # --- 表示されているボタン一覧を記録 ---
    buttons = driver.find_elements(By.TAG_NAME, "button")
    log(f"🔘 現在表示中のボタン数: {len(buttons)}")
    for i, btn in enumerate(buttons):
        try:
            log(f"  {i+1}. text = '{btn.text}'")
        except:
            log(f"  {i+1}. text = [取得失敗]")

    # --- 「情報を保存」ボタンを押す（モーダルではなく画面上表示） ---
    try:
        save_info_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '情報を保存')]"))
        )
        save_info_btn.click()
        log("📌 『情報を保存』ボタンをクリックしました")
        time.sleep(1)
    except:
        log("ℹ️ 『情報を保存』ボタンは表示されませんでした")

    # --- タグページに移動 ---
    url = f"https://www.instagram.com/explore/tags/{TARGET_TAG}/"
    log(f"🌐 タグページへアクセス中: {url}")
    driver.get(url)
    time.sleep(5)

    # --- スクロールして投稿読み込み ---
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        log(f"↕️ スクロール {i+1} 回目")
        time.sleep(2)

    # --- 投稿リンク取得 ---
    log("🔍 投稿リンクを取得中...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/p/"):
            full_link = f"https://www.instagram.com{href}"
            if full_link not in links:
                links.append(full_link)

    log(f"✅ {len(links)} 件の投稿リンクを取得")
    for link in links[:MAX_POSTS]:
        log(link)

except Exception as e:
    log(f"💥 エラー発生: {e}")

finally:
    driver.quit()
    log("🛑 ブラウザを終了しました")
    log("🎉 全処理が完了しました")
