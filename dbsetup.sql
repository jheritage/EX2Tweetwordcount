
CREATE DATABASE tcount;
ALTER ROLE  postgres WITH PASSWORD 'pass';
\c tcount;

CREATE TABLE tweetwordcount
(
	word_id serial PRIMARY KEY,
	word 	VARCHAR(150) NOT NULL,
        count 	INT NOT NULL
);

