CREATE TABLE book_user (
	id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(64) NOT NULL,
	mail VARCHAR(128) NOT NULL,
	hashed_password VARCHAR(128) NOT NULL,
	salt VARCHAR(32) NOT NULL
);