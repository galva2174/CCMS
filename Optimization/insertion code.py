import mysql.connector
import random
from datetime import datetime, timedelta
import names

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mohul2004',
    'database': 'DBT25_A1_PES1UG22CS360_MohulYP'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to the database successfully.")
    
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE FacultyMembers")
    cursor.execute("TRUNCATE TABLE Activities")
    cursor.execute("TRUNCATE TABLE Events")
    cursor.execute("TRUNCATE TABLE Members")
    cursor.execute("TRUNCATE TABLE Clubs")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    club_types = ['Technical', 'Cultural', 'Sports', 'Literary', 'Social', 'Environmental', 
                  'Research', 'Music', 'Dance', 'Art', 'Drama', 'Photography', 'Robotics', 
                  'Coding', 'Debate', 'Quiz']
    
    event_prefixes = ['Annual', 'Quarterly', 'Monthly', 'Weekly', 'Special', 'National', 
                      'International', 'Regional', 'Local', 'Campus', 'Virtual', 'Summer', 
                      'Winter', 'Spring', 'Fall', 'Inaugural', 'Grand', 'Mini', 'Mega', 
                      'Inter-College', 'Intra-College']
    
    event_types = ['Conference', 'Workshop', 'Seminar', 'Competition', 'Meetup', 'Hackathon', 
                   'Festival', 'Concert', 'Exhibition', 'Tournament', 'Summit', 'Symposium', 
                   'Fair', 'Showcase', 'Launch', 'Celebration', 'Gathering', 'Forum', 'Webinar', 
                   'Camp', 'Session']
    
    locations = ['Main Auditorium', 'Conference Hall', 'Sports Complex', 'Library', 'Student Center', 
                 'Online', 'Amphitheater', 'Lab', 'Classroom', 'Field', 'Court', 'Stadium', 
                 'Recreation Center', 'Media Room', 'Meeting Room', 'Cafeteria', 'Quadrangle', 
                 'Garden', 'Lobby', 'Gymnasium', 'Theater']
    
    activity_types = ['Workshop', 'Training', 'Practice', 'Meeting', 'Brainstorming', 'Planning', 
                      'Rehearsal', 'Discussion', 'Design', 'Development', 'Research', 'Networking', 
                      'Study', 'Mentoring', 'Orientation', 'Outreach', 'Recruiting', 'Team Building', 
                      'Social', 'Volunteering', 'Project']
    
    activity_prefixes = ['Weekly', 'Monthly', 'Quarterly', 'Annual', 'Special', 'Beginner', 
                         'Intermediate', 'Advanced', 'Mandatory', 'Optional', 'Open', 'Closed', 
                         'Internal', 'External', 'Group', 'Individual', 'Collaborative', 'Competitive', 
                         'Hands-on', 'Interactive', 'Informational']
    
    def random_date(start_date, end_date):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + timedelta(days=random_number_of_days)
    
    print("Inserting data into Clubs table...")
    clubs_data = []
    for i in range(1, 101):
        club_type = random.choice(club_types)
        establishment_year = random.randint(1990, 2024)
        
        clubs_data.append((
            i,
            f"Club {i} {club_type}",
            club_type,
            establishment_year
        ))
    
    clubs_insert_query = """
    INSERT INTO Clubs (ClubID, ClubName, ClubType, EstablishmentYear)
    VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(clubs_insert_query, clubs_data)
    conn.commit()
    print(f"Inserted {len(clubs_data)} rows into Clubs table.")
    
    print("Inserting data into Members table...")
    members_data = []
    members_data.append((
        1,  
        'Mohul', 
        'YP', 
        'mohulyp@gmail.com',
        '555-1234', 
        '2004-03-10',  
        random.randint(1, 100) 
    ))

    for i in range(2, 10001):
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
        phone_number = f"555-{random.randint(1000, 9999)}"
        
        start_date = datetime.now() - timedelta(days=30*365)
        end_date = datetime.now() - timedelta(days=18*365)
        dob = random_date(start_date, end_date).strftime('%Y-%m-%d')
        
        club_id = random.randint(1, 100)
        
        members_data.append((
            i,
            first_name,
            last_name,
            email,
            phone_number,
            dob,
            club_id
        ))
        
        if i % 1000 == 0:
            members_insert_query = """
            INSERT INTO Members (MemberID, FirstName, LastName, Email, PhoneNumber, DOB, ClubID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(members_insert_query, members_data)
            conn.commit()
            print(f"Inserted {len(members_data)} rows into Members table (batch {i//1000}).")
            members_data = []
    
    if members_data:
        members_insert_query = """
        INSERT INTO Members (MemberID, FirstName, LastName, Email, PhoneNumber, DOB, ClubID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(members_insert_query, members_data)
        conn.commit()
        print(f"Inserted {len(members_data)} remaining rows into Members table.")
    
    print("Inserting data into Events table...")
    events_data = []
    for i in range(1, 10001):
        prefix = random.choice(event_prefixes)
        event_type = random.choice(event_types)
        location = random.choice(locations)
        
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now() + timedelta(days=365)
        event_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        
        club_id = random.randint(1, 100)
        
        event_name = f"{prefix} {event_type} {random.randint(2023, 2025)}"
        event_description = f"This is a description for the {prefix} {event_type}. It will be held at the {location} and is organized by Club ID {club_id}."
        
        events_data.append((
            i,
            event_name,
            event_date,
            location,
            event_description,
            club_id
        ))
        
        if i % 1000 == 0:
            events_insert_query = """
            INSERT INTO Events (EventID, EventName, EventDate, EventLocation, EventDescription, ClubID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(events_insert_query, events_data)
            conn.commit()
            print(f"Inserted {len(events_data)} rows into Events table (batch {i//1000}).")
            events_data = []
    
    if events_data:
        events_insert_query = """
        INSERT INTO Events (EventID, EventName, EventDate, EventLocation, EventDescription, ClubID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(events_insert_query, events_data)
        conn.commit()
        print(f"Inserted {len(events_data)} remaining rows into Events table.")

    print("Inserting data into Activities table...")
    activities_data = []
    for i in range(1, 10001):
        activity_type = random.choice(activity_types)
        prefix = random.choice(activity_prefixes)
        
        start_date = datetime.now() - timedelta(days=180)
        end_date = datetime.now() + timedelta(days=180)
        activity_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        
        club_id = random.randint(1, 100)
        
        activity_name = f"{prefix} {activity_type} {random.randint(1, 100)}"
        activity_description = f"This is a description for the {prefix} {activity_type} activity. It is organized by Club ID {club_id}."
        
        activities_data.append((
            i,
            activity_name,
            activity_description,
            activity_date,
            club_id
        ))
        
        if i % 1000 == 0:
            activities_insert_query = """
            INSERT INTO Activities (ActivityID, ActivityName, ActivityDescription, ActivityDate, ClubID)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(activities_insert_query, activities_data)
            conn.commit()
            print(f"Inserted {len(activities_data)} rows into Activities table (batch {i//1000}).")
            activities_data = []
    
    if activities_data:
        activities_insert_query = """
        INSERT INTO Activities (ActivityID, ActivityName, ActivityDescription, ActivityDate, ClubID)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(activities_insert_query, activities_data)
        conn.commit()
        print(f"Inserted {len(activities_data)} remaining rows into Activities table.")
    
    print("Inserting data into FacultyMembers table...")
    faculty_data = []
    for i in range(1, 10001):
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = f"prof.{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@university.edu"
        phone_number = f"555-{random.randint(1000, 9999)}"
        
        club_id = random.randint(1, 100)
        
        faculty_data.append((
            i,
            first_name,
            last_name,
            email,
            phone_number,
            club_id
        ))
        
        if i % 1000 == 0:
            faculty_insert_query = """
            INSERT INTO FacultyMembers (FacultyID, FirstName, LastName, Email, PhoneNumber, ClubID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(faculty_insert_query, faculty_data)
            conn.commit()
            print(f"Inserted {len(faculty_data)} rows into FacultyMembers table (batch {i//1000}).")
            faculty_data = []
    
    if faculty_data:
        faculty_insert_query = """
        INSERT INTO FacultyMembers (FacultyID, FirstName, LastName, Email, PhoneNumber, ClubID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(faculty_insert_query, faculty_data)
        conn.commit()
        print(f"Inserted {len(faculty_data)} remaining rows into FacultyMembers table.")
    
    print("All data has been inserted successfully.")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Database connection closed.")
