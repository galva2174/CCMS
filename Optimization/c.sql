CREATE INDEX idx_members_dob_firstname ON Members(DOB, FirstName);
CREATE INDEX idx_clubs_clubtype_establishmentyear ON Clubs(ClubType, EstablishmentYear);
CREATE INDEX idx_clubs_clubname ON Clubs(ClubName);
CREATE INDEX idx_events_eventdate ON Events(EventDate);


EXPLAIN ANALYZE 
SELECT * 
FROM Members m
WHERE m.ClubID NOT IN (
    SELECT c.ClubID
    FROM Clubs c
    WHERE c.ClubType = 'Sports' AND c.EstablishmentYear > 2000
)
AND m.DOB > '1990-01-01'
ORDER BY m.FirstName;

EXPLAIN ANALYZE
SELECT c.ClubName, COUNT(m.MemberID) AS MemberCount
FROM Members m
INNER JOIN Clubs c ON m.ClubID = c.ClubID
INNER JOIN Events e ON c.ClubID = e.ClubID
WHERE e.EventDate > '2024-01-01' AND c.ClubType = 'Sports'
GROUP BY c.ClubName
HAVING COUNT(m.MemberID) > 3
ORDER BY MemberCount DESC;
