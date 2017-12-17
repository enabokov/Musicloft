CREATE TABLE "Songs" (
	"id" serial NOT NULL,
	"title" VARCHAR(255) NOT NULL,
	"genre" integer NOT NULL,
	"img_url" VARCHAR(255) NOT NULL,
	"popularity" DECIMAL NOT NULL,
	"vote_average" DECIMAL NOT NULL,
	"vote_count" integer NOT NULL,
	"overview" VARCHAR(255) NOT NULL,
	"language" VARCHAR(255) NOT NULL,
	"budget" VARCHAR(255) NOT NULL,
	"country" integer NOT NULL,
	"release_date" DATE NOT NULL,
	"song_status" integer NOT NULL,
	CONSTRAINT Songs_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Genres" (
	"id" serial NOT NULL UNIQUE,
	"name" VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT Genres_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Singers" (
	"id" serial NOT NULL,
	"name" VARCHAR(255) NOT NULL,
	"img_url" VARCHAR(255) NOT NULL,
	"gender" BINARY NOT NULL,
	"country" integer NOT NULL,
	CONSTRAINT Singers_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "SongSinger" (
	"song_id" DECIMAL NOT NULL,
	"singer_id" DECIMAL NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Users" (
	"id" serial NOT NULL,
	"name" VARCHAR(255) NOT NULL,
	"is_adult" BINARY NOT NULL,
	CONSTRAINT Users_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ratings" (
	"user_id" DECIMAL NOT NULL,
	"song_id" DECIMAL NOT NULL,
	"rating" DECIMAL NOT NULL,
	"date" DATETIME NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Languages" (
	"id" serial NOT NULL,
	"name" serial(255) NOT NULL,
	CONSTRAINT Languages_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Countries" (
	"id" serial NOT NULL,
	"name" VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT Countries_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Status" (
	"id" serial NOT NULL,
	"name" serial NOT NULL,
	CONSTRAINT Status_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Songs" ADD CONSTRAINT "Songs_fk0" FOREIGN KEY ("genre") REFERENCES "Genres"("id");
ALTER TABLE "Songs" ADD CONSTRAINT "Songs_fk1" FOREIGN KEY ("language") REFERENCES "Languages"("id");
ALTER TABLE "Songs" ADD CONSTRAINT "Songs_fk2" FOREIGN KEY ("country") REFERENCES "Countries"("id");
ALTER TABLE "Songs" ADD CONSTRAINT "Songs_fk3" FOREIGN KEY ("song_status") REFERENCES "Status"("id");


ALTER TABLE "Singers" ADD CONSTRAINT "Singers_fk0" FOREIGN KEY ("country") REFERENCES "Countries"("id");

ALTER TABLE "SongSinger" ADD CONSTRAINT "SongSinger_fk0" FOREIGN KEY ("song_id") REFERENCES "Songs"("id");
ALTER TABLE "SongSinger" ADD CONSTRAINT "SongSinger_fk1" FOREIGN KEY ("singer_id") REFERENCES "Singers"("id");


ALTER TABLE "Ratings" ADD CONSTRAINT "Ratings_fk0" FOREIGN KEY ("user_id") REFERENCES "Users"("id");
ALTER TABLE "Ratings" ADD CONSTRAINT "Ratings_fk1" FOREIGN KEY ("song_id") REFERENCES "Songs"("id");




-- Select all not released songs of the precise singer
SELECT Singers.name, Songs.title, Songs.genre, Status.name FROM Singers
JOIN SongSinger ON SongSinger.singer_id = Singer.id
JOIN Songs ON SongSinger.song_id = Song.id
JOIN Status ON Status.id = Songs.id
WHERE name = 'waiting' AND
Songers.name = '{singer}';

-- Select top 10 genres of user by average rating
SELECT Users.name, Genres.name, AVG(Ratings.rating) AS avg_rating FROM Users 
JOIN Ratings ON Ratings.user_id = Users.id
JOIN Songs ON Songs.is = Ratings.song_id
JOIN Genres ON Genres.id = Songs.genre
WHERE Users.id = {id}
GROUP BY Genres.name
ORDER BY avg_rating DESC
LIMIT 10;

-- Insert or update already existed song
INSERT INTO Songs (id, title, genre) 
VALUES (14, 'new song', 'genre')
ON CONFLICT (id) DO UPDATE
SET title = excluded.title, genre = excluded.genre;

values_to_update = [f"'{value}'" for value in parameter_value if value]
'INSERT INTO Songs (id, {", ".join(columns_to_update)}) ' \
f'VALUES ({id}, {", ".join(values_to_update)}) ' \
f'ON CONFLICT (id) DO UPDATE ' \
f'SET ' + ', '.join([f'{column} = excluded.{column}' for column in columns_to_update])


-- The most popular dates of singer's carea
SELECT AVG(Ratings.rating) as avg_rating FROM Singers
JOIN SongSinger ON SongSinger.singer_id = Singers.id
JOIN Songs ON Songs.id = SongSinger.song_id
JOIN Ratings ON Songs.id = Ratings.song_id
WHERE Singers.name = 'Some Name'
GROUP BY Ratings.data
ORDER BY avg_rating DESC;

-- Statistic of rating for precise singer
SELECT COUNT(Songs.rating) FROM Songs
JOIN SongSinger ON Songs.id = SongSinger.song_id
JOIN Singer ON Singer.id = SongSinger.singer_id
WHERE Singer.name = 'Some name'
GROUP By Songs.rating;


-- Make analytics of rated songs by users
SELECT "Users".name,
        CASE WHEN rating >= 0.8 THEN "Very Popular"
             WHEN rating >= 0.5 AND rating < 0.8 THEN "Getting popular"
             WHEN rating < 0.5 AND rating >= 0.2 THEN "Well-know among old people..."
             ELSE "Not popular"
        END,
        "Songs".name
FROM "Ratings"
JOIN "Songs" ON "Songs".id = "Ratings".song_id
JOIN "Users" ON "Users".id = "Ratings".user_id;

-- Find average popularity by genre
SELECT title,
       genre,
       AVG(popularity) OVER (PARTITION by genre ORDER by title) AS avg_popularity,
       language
FROM "Songs"
JOIN "Genres" ON "Genres".id = "Songs".genre
JOIN "Languages" ON "language".id = "Songs".language
WHERE song_status = "Released";


-- sum total budget of all songs grouped by genre
SELECT genre, SUM(budget) as total
FROM "Songs"
JOIN "Genres" ON "Genres".id = "Songs".genre
GROUP by genre
HAVING EXTRACT('year', release_date) >= (now() - interval '2 month');
ORDER by 2 DESC;

-- rank countries by their songs,
-- find total budget of songs of certain country,
-- that were liked by adolescence
WITH songs_with_country as (
      SELECT
        title, genre, img_url, popularity, "Countries".name, budget, release_date, song_status
      FROM "Songs"
        JOIN "Countries" ON "Countries".id = "Songs".country
    ), liked_by_users as (
      SELECT rating FROM "Ratings"
      JOIN "Users" ON "Users".id = "Ratings".user_id
      WHERE is_adult IS FALSE;
    )

SELECT
  title,
  SUM(budget) OVER (PARTITION by country) as budget,
  RANK() OVER (PARTITION by county ORDER by budget)
FROM songs_with_country
WHERE vote_avg = (SELECT rating FROM liked_by_users)


-- calculate singer by genre in specific country
SELECT
  Singers.name,
  ROW_NUMBER() OVER (PARTITION by country) as total_number
FROM "Singers"
JOIN "Countries" ON "Countries".id = "Singers".country
WHERE "Countries".name = 'USA';