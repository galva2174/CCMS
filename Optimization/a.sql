--a)
-- Create the database
CREATE DATABASE DBT25_A1_PES1UG22CS360_MohulYP;

-- Use the created database
USE DBT25_A1_PES1UG22CS360_MohulYP;

-- Create Clubs table
CREATE TABLE Clubs (
    ClubID INT PRIMARY KEY,
    ClubName VARCHAR(100) NOT NULL,
    ClubType VARCHAR(50),
    EstablishmentYear INT
);

-- Create Members table
CREATE TABLE Members (
    MemberID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(15),
    DOB DATE,
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Create Events table
CREATE TABLE Events (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(100) NOT NULL,
    EventDate DATE,
    EventLocation VARCHAR(100),
    EventDescription TEXT,
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Create Activities table
CREATE TABLE Activities (
    ActivityID INT PRIMARY KEY,
    ActivityName VARCHAR(100) NOT NULL,
    ActivityDescription TEXT,
    ActivityDate DATE,
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Create FacultyMembers table
CREATE TABLE FacultyMembers (
    FacultyID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(15),
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);
