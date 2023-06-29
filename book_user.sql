CREATE TABLE book_user (
	id SERIAL PRIMARY KEY,
	name VARCHAR(64),
	mail VARCHAR(128),
	hashed_password VARCHAR(128),
	salt VARCHAR(32)
);