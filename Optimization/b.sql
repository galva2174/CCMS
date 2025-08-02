-- Select all data from Clubs table
SELECT * FROM Clubs;

-- Count rows in Clubs table
SELECT COUNT(*) FROM Clubs;

-- Select all data from Members table
SELECT * FROM Members;

-- Count rows in Members table
SELECT COUNT(*) FROM Members;

-- Select all data from Events table
SELECT * FROM Events;

-- Count rows in Events table
SELECT COUNT(*) FROM Events;

-- Select all data from Activities table
SELECT * FROM Activities;

-- Count rows in Activities table
SELECT COUNT(*) FROM Activities;

-- Select all data from FacultyMembers table
SELECT * FROM FacultyMembers;

-- Count rows in FacultyMembers table
SELECT COUNT(*) FROM FacultyMembers;

-- Index scan
SELECT FirstName, LastName, Email
FROM Members
WHERE ClubID = 1 
  AND DOB > '1990-01-01'
  AND Email LIKE '%@example.com';



-- Table scan
-- table scan on members to find members born after 1990 ordered by first name who are not in sports clubs established after 2000
SELECT * 
FROM Members m
WHERE m.ClubID NOT IN (
    SELECT c.ClubID
    FROM Clubs c
    WHERE c.ClubType = 'Sports' AND c.EstablishmentYear > 2000
)
AND m.DOB > '1990-01-01'
ORDER BY m.FirstName;

-- This query performs a table scan on the Activities table, groups the data, and orders it
SELECT a.ActivityName, COUNT(m.MemberID) AS MemberCount
FROM Activities a
LEFT JOIN Members m ON a.ClubID = m.ClubID
GROUP BY a.ActivityName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;

-- This query performs a table scan on FacultyMembers and Activities, creating a Cartesian product
SELECT f.FirstName, f.LastName, a.ActivityName
FROM FacultyMembers f
CROSS JOIN Activities a;




-- Join Members, Clubs, and Events tables, group by ClubName with a count of members per club
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount
FROM Members m
INNER JOIN Clubs c ON m.ClubID = c.ClubID
INNER JOIN Events e ON c.ClubID = e.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports'
GROUP BY c.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;

-- Join Members, Clubs, and Events tables and use a nested query for filtering
SELECT * 
FROM Members m
INNER JOIN Clubs c ON m.ClubID = c.ClubID
INNER JOIN Events e ON c.ClubID = e.ClubID
WHERE e.EventDate IN (
    SELECT e2.EventDate
    FROM Events e2
    WHERE e2.EventLocation = 'Court' AND e2.EventDate > '2025-01-01'
)
ORDER BY e.EventDate;



CREATE VIEW ClubMembers AS
SELECT c.ClubName, m.FirstName, m.LastName, m.Email
FROM Clubs c
INNER JOIN Members m ON c.ClubID = m.ClubID;

-- Query using the view to select a subset of columns with filtering
SELECT ClubName, FirstName, LastName
FROM ClubMembers
WHERE ClubName = 'Club 54 Dance' AND LastName = 'YP';


