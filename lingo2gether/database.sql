-- CREATE DATABASE lingo2gether;

-- DROP TABLE words;

CREATE TABLE words(
    wordName VARCHAR(30),
    userID INT,
    special BOOLEAN,
    PRIMARY KEY(userID, wordName)
);