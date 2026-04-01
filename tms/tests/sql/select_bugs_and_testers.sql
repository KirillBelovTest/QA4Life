SELECT
    bugs.*,
    testers.name,
    testers.grade
FROM bugs
LEFT JOIN testers ON bugs.author_id = testers.id