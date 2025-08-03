"""
logger.py
ログ記録ユーティリティ（共通ログ出力機構）

このモジュールは以下の責任を持つ：
1. ファイルパスを指定して log() 関数を生成する
2. 生成された log() は、標準出力とログファイル両方に出力される
3. すべてのモジュールで同一のlog関数を共有可能
"""

from datetime import datetime

def setup_logger(log_file_path):
    """
    ロガー関数を生成して返す

    Parameters:
        log_file_path (str or Path): ログ出力先ファイル

    Returns:
        function: log(msg: str) → stdoutとファイルに同時出力
    """
    def log(msg: str):
        # --- 時刻付きメッセージ ---
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {str(msg)}"

        # --- コンソール出力 ---
        print(full_msg)

        # --- ファイル出力（追記） ---
        try:
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(full_msg + "\n")
                f.flush()  # 即時書き込み保証
        except Exception as e:
            print(f"⚠️ ログファイルへの書き込みに失敗: {e}")

    return log
