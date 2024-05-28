CREATE TABLE Authors(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_name VARCHAR(50)
);

CREATE TABLE Genres(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	genre_name VARCHAR(50)
);

CREATE TABLE Addresses(
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	city_name VARCHAR(50),
	street_name VARCHAR(50)	
);

CREATE TABLE Users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	address_id INTEGER NOT NULL,
	first_name VARCHAR(50),
	last_name  VARCHAR(50),
	FOREIGN KEY (address_id) REFERENCES Addresses(id) ON DELETE CASCADE
);

CREATE TABLE Books(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(50),
	author_id INTEGER NOT NULL,
	genre_id  INTEGER NOT NULL,
	FOREIGN KEY (author_id) REFERENCES Authors(id),
	FOREIGN KEY (genre_id) REFERENCES Genres(id)
);

CREATE TABLE Distribution(
	user_id INT NOT NULL,
	book_id INT NOT NULL,
	load_date DATETIME NOT NULL,
	return_date DATETIME,
	expected_return_date DATETIME NOT NULL,
	FOREIGN KEY (user_id) REFERENCES Users(id),
	FOREIGN KEY (book_id) REFERENCES Books(id)
);


drop table Authors;
drop table Genres;
drop table Users;
drop table Books;
drop table Distribution;
drop table Addresses;

