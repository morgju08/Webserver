CREATE TABLE IF NOT EXISTS "Tweets" (
	"Content"	TEXT NOT NULL,
	"Timestamp"	INTEGER,
	"Likes"	INTEGER,
	"Location"	TEXT,
	"ID"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("ID" AUTOINCREMENT)
);


CREATE TABLE IF NOT EXISTS "Users" (
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT,
    "cookie" TEXT,
    "salt" TEXT
)