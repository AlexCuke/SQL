CREATE TABLE genre (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE artist (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL
);

CREATE TABLE album (
id SERIAL PRIMARY KEY,
title VARCHAR(200) NOT NULL,
release_year INT
);

CREATE TABLE track (
id SERIAL PRIMARY KEY,
title VARCHAR(200) NOT NULL,
duration INT NOT NULL, – длительность в секундах
album_id INT NOT NULL REFERENCES album(id)
);

CREATE TABLE collection (
id SERIAL PRIMARY KEY,
title VARCHAR(200) NOT NULL,
release_year INT
);

CREATE TABLE artist_genre (
artist_id INT NOT NULL REFERENCES artist(id),
genre_id INT NOT NULL REFERENCES genre(id),
PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE artist_album (
artist_id INT NOT NULL REFERENCES artist(id),
album_id INT NOT NULL REFERENCES album(id),
PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE collection_track (
collection_id INT NOT NULL REFERENCES collection(id),
track_id INT NOT NULL REFERENCES track(id),
PRIMARY KEY (collection_id, track_id)
);