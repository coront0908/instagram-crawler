"""
instagram_login.py

Instagramへのログイン処理モジュール（Selenium）

この構造は以下の責任を持つ：
1. Edgeブラウザを起動し、ログインページにアクセス
2. 指定されたユーザー名・パスワードでログインを試行
3. URL遷移・要素取得の失敗も含め、詳細ログを記録
4. ログイン成功後のdriverオブジェクトを返す
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_and_get_driver(username: str, password: str, log) -> webdriver.Edge:
    """
    Instagramにログインし、ログイン済みdriverを返す

    Parameters:
        username (str): InstagramログインID
        password (str): Instagramパスワード
        log (function): ログ出力関数

    Returns:
        webdriver.Edge: ログイン済みのEdge WebDriver
    """

    log("🟡 login_and_get_driver() 開始")

    # --- ブラウザ起動設定 ---
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(options=options)
    log("🖥️ Edgeブラウザを起動しました")

    # --- ログインページへアクセス ---
    login_url = "https://www.instagram.com/accounts/login/"
    log(f"🔐 Instagramログインページへアクセス中: {login_url}")
    driver.get(login_url)
    time.sleep(3)

    current_url = driver.current_url
    log(f"🌐 現在URL: {current_url}")
    if "/login" not in current_url:
        log("⚠️ ログインページ以外に遷移している可能性があります")

    # --- ログインフォーム入力処理 ---
    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        log("🧾 ログインフォームの入力欄を検出しました")
    except Exception as e:
        log(f"❌ ログインフォームの取得に失敗 ▶ {type(e).__name__}: {e}")
        driver.quit()
        raise

    try:
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        log("🔄 認証情報を入力し、ログインを送信しました")
    except Exception as e:
        log(f"❌ フォーム入力中にエラー発生 ▶ {type(e).__name__}: {e}")
        driver.quit()
        raise

    # --- URL変化を監視（最大5秒） ---
    for i in range(5):
        time.sleep(1)
        current = driver.current_url
        log(f"⏱️ {i+1}s: 現在URL ➜ {current}")
        if "/accounts/login/" not in current:
            log("✅ URL遷移を検出 ➜ ログイン成功の可能性あり")
            break
    else:
        log("❌ URLが変化せず、ログイン失敗の可能性があります")
        driver.quit()
        raise Exception("Instagramログインが失敗した可能性があります")

    # --- 処理完了 ---
    log("🔓 ログイン処理完了。WebDriverを返却します")
    return driver
