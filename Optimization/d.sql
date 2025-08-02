
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount
FROM Members m
INNER JOIN Clubs c ON m.ClubID = c.ClubID
INNER JOIN Events e ON c.ClubID = e.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports'
GROUP BY c.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;

EXPLAIN ANALYZE
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount
FROM Members m
INNER JOIN Clubs c ON m.ClubID = c.ClubID
INNER JOIN Events e ON c.ClubID = e.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports'
GROUP BY c.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;

EXPLAIN ANALYZE
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount 
FROM Clubs c
INNER JOIN Events e ON c.ClubID = e.ClubID
INNER JOIN Members m ON c.ClubID = m.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports' 
GROUP BY c.ClubName 
HAVING COUNT(m.MemberID) > 3 
ORDER BY MemberCount DESC;

EXPLAIN ANALYZE
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount 
FROM Events e
INNER JOIN Clubs c ON e.ClubID = c.ClubID
INNER JOIN Members m ON c.ClubID = m.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports' 
GROUP BY c.ClubName 
HAVING COUNT(m.MemberID) > 3 
ORDER BY MemberCount DESC;

EXPLAIN ANALYZE
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount
FROM Clubs c
LEFT JOIN Members m ON c.ClubID = m.ClubID
WHERE c.ClubType = 'Sports'
AND c.ClubID IN (
    SELECT DISTINCT e.ClubID
    FROM Events e
    WHERE e.EventDate > '2024-01-01'
)
GROUP BY c.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;


EXPLAIN ANALYZE
WITH FilteredClubs AS (
    SELECT ClubID, ClubName
    FROM Clubs
    WHERE ClubType = 'Sports'
),
ActiveClubs AS (
    SELECT DISTINCT fc.ClubID, fc.ClubName
    FROM FilteredClubs fc
    INNER JOIN Events e ON fc.ClubID = e.ClubID
    WHERE e.EventDate > '2024-01-01'
)
SELECT ac.ClubName, COUNT(m.MemberID) AS MemberCount
FROM ActiveClubs ac
INNER JOIN Members m ON ac.ClubID = m.ClubID
GROUP BY ac.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;



