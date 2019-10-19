PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  registered_at TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  last_login TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  username VARCHAR(255),
  password VARCHAR(200),
  email VARCHAR(200)
);

CREATE TRIGGER triggerUserLogin AFTER UPDATE ON users
BEGIN
  update users SET last_login = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;

CREATE TABLE debt(
date VARCHAR(20),
 location VARCHAR(255),
 -- amount DOUBLE,
 -- balance DOUBLE,
 parent_id INTEGER,
 FOREIGN KEY (parent_id) REFERENCES users(id)

);