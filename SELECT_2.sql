SELECT g.name       AS genre,
       COUNT(ag.artist_id) AS artist_count
FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY g.name;

SELECT COUNT(t.id) AS track_count
FROM track t
JOIN album a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

SELECT a.title              AS album,
       AVG(t.duration)      AS avg_duration
FROM album a
JOIN track t ON t.album_id = a.id
GROUP BY a.title;

SELECT DISTINCT ar.name
FROM artist ar
WHERE ar.id NOT IN (
    SELECT aa.artist_id
    FROM artist_album aa
    JOIN album a ON aa.album_id = a.id
    WHERE a.release_year = 2020
);

SELECT DISTINCT c.title
FROM collection c
JOIN collection_track ct ON c.id = ct.collection_id
JOIN track t ON ct.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'Queen';

SELECT a.title
FROM album a
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist_genre ag ON aa.artist_id = ag.artist_id
GROUP BY a.title
HAVING COUNT(DISTINCT ag.genre_id) > 1;

SELECT t.title
FROM track t
LEFT JOIN collection_track ct ON t.id = ct.track_id
WHERE ct.collection_id IS NULL;

SELECT DISTINCT ar.name
FROM artist ar
JOIN artist_album aa ON ar.id = aa.artist_id
JOIN album a ON aa.album_id = a.id
JOIN track t ON t.album_id = a.id
WHERE t.duration = (
    SELECT MIN(duration)
    FROM track
);

SELECT a.title
FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.title
HAVING COUNT(t.id) = (
    SELECT MIN(track_cnt)
    FROM (
        SELECT COUNT(t2.id) AS track_cnt
        FROM album a2
        JOIN track t2 ON a2.id = t2.album_id
        GROUP BY a2.id
    ) sub
);

