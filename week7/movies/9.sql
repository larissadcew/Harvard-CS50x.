SELECT distinct(name)
FROM movies,stars,people
WHERE movies.id = stars.movie_id
AND people.id =stars.person_id
AND year = 2004
ORDER by birth;