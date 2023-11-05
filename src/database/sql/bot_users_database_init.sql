CREATE TABLE IF NOT EXISTS bot_users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    chat_id TEXT NOT NULL,
    selected_db TEXT
)