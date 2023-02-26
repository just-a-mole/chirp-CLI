sqlite> .schema
CREATE TABLE users(
id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT
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
first_name BOOLEAN,
last_name BOOLEAN,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(friend_id) REFERENCES users(id)
);
CREATE TABLE enemies(
user_id INTEGER,
friend_id INTEGER,
first_name BOOLEAN,
last_name BOOLEAN,
FOREIGN KEY(user_id) REFERENCES users(id),
FOREIGN KEY(friend_id) REFERENCES users(id)
);
CREATE TABLE friend_first_posts(
user_id INTEGER,
post TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE friend_last_posts(
user_id INTEGER,
post TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE enemy_first_posts(
user_id INTEGER,
post TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE enemy_last_posts(
user_id INTEGER,
post TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
