from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import hashlib
from psycopg2 import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Update with your database username
        password="mohul2004",  # Update with your password
        database="ClubManagement"
    )

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        hashed_password = hash_password(password)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO Users (user_id, username, password, role) VALUES (%s, %s, %s, %s)", 
                (user_id, username, hashed_password, role)
            )
            connection.commit()
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Error as e:
            flash('Error: Could not register user', 'error')
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        hashed_password = hash_password(password)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM Users WHERE user_id = %s AND password = %s", (user_id, hashed_password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[3]  # user_id
            session['username'] = user[0]  # username
            session['role'] = user[2]  # role
            cursor.close()
            connection.close()
            
            if user[2] == 'admin':
                return redirect(url_for('admin_landing'))
            elif user[2] == 'faculty':
                return redirect(url_for('faculty_landing'))
            elif user[2] == 'member':
                return redirect(url_for('member_landing'))
        else:
            flash('Invalid user ID or password', 'error')
            cursor.close()
            connection.close()
            return render_template('login.html')  # Reload login page with the flash message

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))
@app.route('/admin_landing', methods=['GET', 'POST'])
def admin_landing():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    user_id = session['user_id']  # Current user_id

    # Fetch all club IDs owned by the logged-in admin
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT club_id FROM Clubs WHERE user_id = %s", (user_id,))
    owned_clubs = [club[0] for club in cursor.fetchall()]  # Get a list of club IDs only
    connection.close()

    if request.method == 'POST':
        # Creating a Club
        if 'create_club' in request.form:
            club_id = request.form['club_id']
            name = request.form['club_name']
            department = request.form['department']
            description = request.form['description']
            
            # Add user_id as the owner of the club
            connection = get_db_connection()
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Clubs (club_id, name, department, description, user_id) VALUES (%s, %s, %s, %s, %s)",
                    (club_id, name, department, description, user_id)
                )
                connection.commit()
                flash("Club added successfully!", "success")  # Display success message
            except Exception as e:
                connection.rollback()  # Rollback the transaction in case of an error
                flash("Error: Duplicate club_id. Please choose a unique ID.", "danger")  # Display error message
                print(f"IntegrityError: {e}")  # Optional: Log the error for debugging
            
            connection.commit()
            connection.close()
            flash('Club created successfully!', 'success')

        # Adding a Member
        elif 'add_member' in request.form:
            club_id = request.form['club_id']
            
            # Check if the club is owned by the logged-in user
            if int(club_id) not in owned_clubs:
                flash('You can only add members to clubs you own!', 'error')
                return redirect(url_for('admin_landing'))

            # Extract member details from the form
            member_id = request.form['member_id']
            name = request.form['member_name']
            department = request.form['member_department']
            registration_date = request.form['registration_date']
            email = request.form['email']
            phone = request.form['phone']
            
            # Insert new member into the database
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO Members (mem_id, club_id, name, department, registration_date, email, phone) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (member_id, club_id, name, department, registration_date, email, phone))
                connection.commit()
                connection.close()
                flash('Member added successfully!', 'success')
            except Exception as e:
                connection.rollback()
                connection.close()
                flash(f'Error: Member_id does not exist', 'error')

        # Removing a Member
        elif 'remove_member' in request.form:
            club_id = request.form['club_id']
            if int(club_id) not in owned_clubs:
                flash('You can only remove members from clubs you own!', 'error')
                return redirect(url_for('admin_landing'))

            member_id = request.form['member_id']
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Members WHERE mem_id = %s AND club_id = %s", (member_id, club_id))
                connection.commit()
                connection.close()
                flash('Member removed successfully!', 'success')
            except Exception as e:
                connection.rollback()
                connection.close()
                flash(f'Error: Member_id does not exist', 'error')


        # Creating an Event
        elif 'create_event' in request.form:
            club_id = request.form['club_id']
            if int(club_id) not in owned_clubs:
                flash('You can only create events for clubs you own!', 'error')
                return redirect(url_for('admin_landing'))

            event_id = request.form['event_id']
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            location = request.form['event_location']
            block = request.form['event_block']
            floor = request.form['event_floor']
            campus = request.form['event_campus']
            description = request.form['event_description']
            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Events (e_id, club_id, name, date, block, floor, campus, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                            (event_id, club_id, event_name, event_date, block, floor, campus, description))
                connection.commit()
                connection.close()
                flash('Event created successfully!', 'success')
            except Exception as e:
                connection.rollback()
                connection.close()
                flash("Event_id already exists.")

        # Adding a Resource
        elif 'add_resource' in request.form:
            club_id = request.form['club_id']
            if int(club_id) not in owned_clubs:
                flash('You can only add resources to clubs you own!', 'error')
                return redirect(url_for('admin_landing'))

            e_id = request.form.get('e_id')
            r_id = request.form.get('r_id')
            time_used_from = request.form.get('time_used_from')
            time_used_till = request.form.get('time_used_till')

            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                # Verify if the event is associated with the club owned by the user
                cursor.execute("""
                    SELECT COUNT(*) FROM Events 
                    WHERE e_id = %s AND club_id = %s
                """, (e_id, club_id))
                event_exists = cursor.fetchone()[0]

                if event_exists == 0:
                    flash('You can only add resources to events of clubs you own!', 'error')
                    return redirect(url_for('admin_landing'))

                # Proceed to insert the resource since the check passed
                cursor.execute(""" 
                    INSERT INTO Resources (e_id, r_id, time_used_from, time_used_till) 
                    VALUES (%s, %s, %s, %s)
                """, (e_id, r_id, time_used_from, time_used_till))
                
                connection.commit()
                flash('Resource added successfully!', 'success')
            
            except Error as e:
                flash('Error: Resource_id already in use', 'error')
                connection.rollback()
            
            finally:
                connection.close()

    return render_template('admin_landing.html', owned_clubs=owned_clubs)

@app.route('/faculty_landing', methods=['GET', 'POST'])
def faculty_landing():
    if 'role' not in session or session['role'] != 'faculty':
        return redirect(url_for('login'))

    faculty_id = session['user_id']

    # Fetch the club ID for the faculty member
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the faculty member is already part of a club
    cursor.execute("SELECT club_id FROM Faculty WHERE faculty_id = %s", (faculty_id,))
    result = cursor.fetchone()


    # If no club is found, handle the join club process
    if not result:
        if request.method == 'POST' and 'join_club' in request.form:
            club_id = request.form['club_id']
            name = request.form['faculty_name']
            department = request.form['faculty_department']
            
            # Insert the new faculty member into the Faculty table
            cursor.execute("""
                INSERT INTO Faculty (faculty_id, name, department, club_id) 
                VALUES (%s, %s, %s, %s)
            """, (faculty_id, name, department, club_id))
            connection.commit()

            flash('You have successfully joined the club!', 'success')
            return redirect(url_for('faculty_landing'))

        # Fetch available clubs
        cursor.execute("SELECT club_id, name FROM Clubs")
        clubs = cursor.fetchall()

        cursor.close()
        connection.close()

        # Render the faculty join club page
        return render_template('faculty_join_club.html', clubs=clubs)

    else:
        # Extract the club_id (ensure it's correctly fetched)
        club_id = result[-1]  # club_id is the last column in the result

        cursor.execute("""
    SELECT name, email, department
    FROM Members
    WHERE club_id = (
        SELECT club_id
        FROM Faculty
        WHERE faculty_id = %s
    )
""", (faculty_id,))
        members = cursor.fetchall()

        cursor.execute("""
            SELECT Clubs.name AS club_name, SUM(Sponsors.amount) AS total_sponsorship
            FROM Sponsors
            JOIN Clubs ON Sponsors.club_id = Clubs.club_id
            GROUP BY Clubs.name
            ORDER BY total_sponsorship DESC
        """)

        sponsorship_totals = cursor.fetchall()
        
        cursor.execute("SELECT e_id FROM Events WHERE club_id = %s", (club_id,))
        event_id = cursor.fetchone()

        if event_id:
            cursor.execute("SELECT * FROM Resources WHERE e_id = %s", (event_id[0],))
            resources = cursor.fetchall()
        else:
            resources = []

        
        if request.method == 'POST' and 'add_sponsor' in request.form:
            sponsor_name = request.form['sponsor_name']
            sponsor_email = request.form['sponsor_email']
            sponsor_phone1 = request.form['sponsor_phone1']
            sponsor_phone2 = request.form.get('sponsor_phone2')  # Optional field
            sponsor_amount = float(request.form['sponsor_amount'])

            # Insert sponsor data into the Sponsors table
            cursor.execute("""
                INSERT INTO Sponsors (club_id, name, email, phone1, phone2, amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (club_id,sponsor_name, sponsor_email, sponsor_phone1, sponsor_phone2, sponsor_amount))
            connection.commit()

            flash('Sponsor has been successfully added!', 'success')

        # Render the faculty landing page with club details and sponsor form
        cursor.close()
        connection.close()

        return render_template('faculty_landing.html', members=members, resources=resources, sponsorship_totals=sponsorship_totals)
@app.route('/member_landing', methods=['GET', 'POST'])
def member_landing():
    if 'role' not in session or session['role'] != 'member':
        return redirect(url_for('login'))
    
    member_id = session['user_id']
    
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the member is part of a club
    cursor.execute("SELECT club_id, name, department, email, phone FROM Members WHERE mem_id = %s", (member_id,))
    result = cursor.fetchone()

    # Debugging: Print the result to see what is returned
    print("Member details result:", result)

    if not result:
        # Member is not part of any club, show available clubs to join
        if request.method == 'POST' and 'join_club' in request.form:
            club_id = request.form['club_id']
            member_name = request.form['member_name']
            department = request.form['member_department']
            email = request.form['member_email']
            phone = request.form['member_phone']
            registration_date = request.form['member_registration_date']
            
            # Insert the new member into the Members table
            cursor.execute(""" 
                INSERT INTO Members (mem_id, department, registration_date, name, email, phone, club_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (member_id, department, registration_date, member_name, email, phone, club_id))
            connection.commit()

            flash('You have successfully joined the club!', 'success')
            return redirect(url_for('member_landing'))

        # Fetch available clubs
        cursor.callproc('GetAllClubs')
        
        # Fetch the result of the stored procedure
        clubs = []
        for club in cursor.stored_results():
            clubs = club.fetchall()

        cursor.close()
        connection.close()
        
        return render_template('member_join_club.html', clubs=clubs)

    else:
        # Member is already part of a club, fetch upcoming events for that club
        club_id = result[0]  # club_id is the first column in the result

        # If the form is submitted to update details
        if request.method == 'POST' and 'update_details' in request.form:
            member_name = request.form['member_name']
            department = request.form['member_department']
            email = request.form['member_email']
            phone = request.form['member_phone']

            # Update the member details in the database
            cursor.execute("""
                UPDATE Members
                SET name = %s, department = %s, email = %s, phone = %s
                WHERE mem_id = %s
            """, (member_name, department, email, phone, member_id))
            connection.commit()

            flash('Your details have been updated successfully!', 'success')
            return redirect(url_for('member_landing'))

        # Fetch upcoming events for the member's club
        cursor.callproc('GetEventsByClub', (club_id,))
        
        # Fetch the result of the stored procedure
        events = []
        for event in cursor.stored_results():
            events = event.fetchall()

        cursor.close()
        connection.close()

        # Render the member landing page with the upcoming events for the club
        return render_template('member_landing.html', upcoming_events=events, member_details=result)




if __name__ == '__main__':
    app.run(debug=True)
