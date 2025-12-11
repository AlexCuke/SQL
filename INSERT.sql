INSERT INTO genre (name)
VALUES
    ('Rock'),
    ('Pop'),
    ('Jazz'),
    ('Electronic');

INSERT INTO artist (name)
VALUES
    ('Queen'),
    ('The Beatles'),
    ('Daft Punk'),
    ('Miles Davis');
INSERT INTO album (title, release_year)
VALUES
    ('A Night at the Opera', 1975),
    ('Abbey Road', 1969),
    ('Random Access Memories', 2013);

INSERT INTO track (title, duration, album_id)
VALUES
    ('Bohemian Rhapsody', 355, 1),
    ('Love of My Life', 220, 1),
    ('Come Together', 259, 2),
    ('Here Comes the Sun', 185, 2),
    ('Get Lucky', 369, 3),
    ('Instant Crush', 337, 3);

INSERT INTO collection (title, release_year)
VALUES
    ('Best of Rock', 2020),
    ('Classic Hits', 2018),
    ('Chill Vibes', 2021),
    ('Jazz & Lounge', 2019);

INSERT INTO collection_track (collection_id, track_id)
VALUES
    (1, 1),  -- Best of Rock: Bohemian Rhapsody
    (1, 3),  -- Best of Rock: Come Together
    (2, 4),  -- Classic Hits: Here Comes the Sun
    (2, 1),  -- Classic Hits: Bohemian Rhapsody
    (3, 5),  -- Chill Vibes: Get Lucky
    (3, 6),  -- Chill Vibes: Instant Crush
    (4, 2),  -- Jazz & Lounge: Love of My Life (условно)
    (4, 6);  -- Jazz & Lounge: Instant Crush (условно)
INSERT INTO artist_genre (artist_id, genre_id)
VALUES
    (1, 1),  -- Queen - Rock
    (2, 1),  -- The Beatles - Rock
    (2, 2),  -- The Beatles - Pop
    (3, 4),  -- Daft Punk - Electronic
    (4, 3);  -- Miles Davis - Jazz

INSERT INTO artist_album (artist_id, album_id)
VALUES
    (1, 1),  -- Queen - A Night at the Opera
    (2, 2),  -- The Beatles - Abbey Road
    (3, 3);  -- Daft Punk - Random Access Memories