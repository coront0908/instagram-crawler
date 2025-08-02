# settings.py

# 巡回するハッシュタグ（先頭に "#" は不要）
TARGET_TAGS = [
    "楽天room",
    "amazon購入品",
    "LTK",
]

# 投稿を取得する件数（各タグあたり）
MAX_POSTS_PER_TAG = 30

# アフェリエイトリンクを判定するキーワード
AFFILIATE_DOMAINS = [
    "rakuten.co.jp",
    "amazon.co.jp",
    "amzn.to",
    "ltk.app",
    "shopstyle.jp",
    "a8.net",
]

# 保存対象のDBファイル名
DB_PATH = "db/affiliate_posts.db"
