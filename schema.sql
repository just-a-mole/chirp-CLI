CREATE TABLE users(
id INTEGER PRIMARY KEY,
name TEXT
);
CREATE TABLE credentials(
user_id INTEGER,
password TEXT,
email TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE friends(
user_id INTEGER,
friend_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(friend_id) REFERENCES users(id)
);
CREATE TABLE enemies(
user_id INTEGER,
friend_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(friend_id) REFERENCES users(id)
);
CREATE TABLE friend_posts(
user_id INTEGER,
post TEXT, title TEXT,
time TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE enemy_posts(
user_id INTEGER,
post TEXT, title TEXT,
time TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(id)
);
