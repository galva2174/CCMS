-- Create the database
CREATE DATABASE ClubManagement;
USE ClubManagement;

-- Creating the Users table for authentication
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'member') NOT NULL
);

-- Creating the Clubs table
CREATE TABLE Clubs (
    club_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    description TEXT,
    user_id INT
);

-- Creating the Faculty table
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);

-- Creating the Events table
CREATE TABLE Events (
    e_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    date DATE,
    block VARCHAR(50),
    floor VARCHAR(50),
    campus VARCHAR(50),
    description TEXT,
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);

-- Creating the Sponsors table
CREATE TABLE Sponsors (
    sponsor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone1 VARCHAR(15),
    phone2 VARCHAR(15),
    amount DECIMAL(10, 2),
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);


-- Creating the Announcements table
CREATE TABLE Announcements (
    a_id INT PRIMARY KEY AUTO_INCREMENT,
    a_text TEXT,
    date DATE,
    time TIME,
    year YEAR
    club_id INT,
    FOREIGN KEY(club_id) REFERENCES Clubs(club_id)
);

-- Creating the Members table
CREATE TABLE Members (
    mem_id INT PRIMARY KEY AUTO_INCREMENT,
    dob DATE,
    department VARCHAR(100),
    registration_date DATE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    attendance INT
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)

);

-- Creating the Resources table
CREATE TABLE Resources (
    r_id INT PRIMARY KEY AUTO_INCREMENT,
    time_used_from TIME,
    time_used_till TIME,
    e_id INT,
    FOREIGN KEY (e_id) REFERENCES Events(e_id)
);

-- Stored Procedure: Get Events by Club ID
DELIMITER //
CREATE PROCEDURE GetEventsByClub(IN clubID INT)
BEGIN
    
    SELECT * FROM Events WHERE club_id = clubID;
    
END //
DELIMITER ;

--Stored Procedure to get all clubs
DELIMITER //
CREATE PROCEDURE GetAllClubs()
BEGIN
    SELECT * FROM Clubs;
END //
DELIMITER ;


-- Trigger: Check Sponsor Amount
DELIMITER //
CREATE TRIGGER before_sponsor_insert
BEFORE INSERT ON Sponsors
FOR EACH ROW
BEGIN
    IF NEW.amount < 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sponsor amount must be at least Rs.100';
    END IF;
END //
DELIMITER ;
