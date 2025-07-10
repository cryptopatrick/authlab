CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tokens (
    token_id TEXT PRIMARY KEY,
    token_user_id TEXT NOT NULL,
    token_value TEXT UNIQUE NOT NULL,
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (token_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
