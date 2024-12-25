from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

DATABASE = 'app_data.db'  # SQLite database file

# Check if the database file exists; if not, create it using init_db.py
if not os.path.exists(DATABASE):
    from init_db import init_db
    init_db()

# Connect to SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check default admin credentials
        if username == 'Admin' and password == 'Admin@123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Admin dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    # Fetch all data
    cursor.execute("SELECT * FROM Locations")
    locations = cursor.fetchall()

    cursor.execute("SELECT * FROM Buildings")
    buildings = cursor.fetchall()

    cursor.execute("SELECT * FROM Houses")
    houses = cursor.fetchall()

    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()

    if request.method == 'POST':
        # Add Location
        if 'add_location' in request.form:
            location_name = request.form['location_name']
            cursor.execute("INSERT INTO Locations (name) VALUES (?)", (location_name,))
            conn.commit()

        # Update Location
        if 'update_location' in request.form:
            location_id = request.form['location_id']
            location_name = request.form['location_name']
            cursor.execute("UPDATE Locations SET name = ? WHERE id = ?", (location_name, location_id))
            conn.commit()

        # Add Building
        if 'add_building' in request.form:
            building_name = request.form['building_name']
            location_id = request.form['location_id']
            cursor.execute("INSERT INTO Buildings (name, location_id) VALUES (?, ?)", (building_name, location_id))
            conn.commit()

        # Update Building
        if 'update_building' in request.form:
            building_id = request.form['building_id']
            building_name = request.form['building_name']
            location_id = request.form['location_id']
            cursor.execute("UPDATE Buildings SET name = ?, location_id = ? WHERE id = ?", (building_name,location_id, building_id))
            conn.commit()

        # Add House
        if 'add_house' in request.form:
            house_name = request.form['house_name']
            building_id = request.form['building_id']
            cursor.execute("INSERT INTO Houses (name, building_id) VALUES (?, ?)", (house_name, building_id))
            conn.commit()

        # Update House
        if 'update_house' in request.form:
            house_id = request.form['house_id']
            house_name = request.form['house_name']
            cursor.execute("UPDATE Houses SET name = ? WHERE id = ?", (house_name, house_id))
            conn.commit()

        # Add Room
        if 'add_room' in request.form:
            room_name = request.form['room_name']
            house_id = request.form['house_id']
            cursor.execute("INSERT INTO Rooms (name, house_id) VALUES (?, ?)", (room_name, house_id))
            conn.commit()

        # Update Room
        if 'update_room' in request.form:
            room_id = request.form['room_id']
            room_name = request.form['room_name']
            cursor.execute("UPDATE Rooms SET name = ? WHERE id = ?", (room_name, room_id))
            conn.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', locations=locations, buildings=buildings, houses=houses, rooms=rooms)

# Route to edit Location
@app.route('/edit_location/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        location_name = request.form['location_name']
        cursor.execute("UPDATE Locations SET name = ? WHERE id = ?", (location_name, id))
        conn.commit()
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM Locations WHERE id = ?", (id,))
    location = cursor.fetchone()

    return render_template('edit_location.html', location=location)

# Route to edit Building
@app.route('/edit_building/<int:id>', methods=['GET', 'POST'])
def edit_building(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        building_name = request.form['building_name']
        location_id = request.form['location_id']
        cursor.execute("UPDATE Buildings SET name = ?, location_id = ? WHERE id = ?", (building_name, location_id, id))
        conn.commit()
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM Buildings WHERE id = ?", (id,))
    building = cursor.fetchone()

    return render_template('edit_building.html', building=building)

# Route to edit House
@app.route('/edit_house/<int:id>', methods=['GET', 'POST'])
def edit_house(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        house_name = request.form['house_name']
        building_id = request.form['building_id']
        cursor.execute("UPDATE Houses SET name = ?, building_id = ? WHERE id = ?", (house_name, building_id, id))
        conn.commit()
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM Houses WHERE id = ?", (id,))
    house = cursor.fetchone()

    return render_template('edit_house.html', house=house)

# Route to edit Room
@app.route('/edit_room/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        room_name = request.form['room_name']
        house_id = request.form['house_id']
        cursor.execute("UPDATE Rooms SET name = ?, house_id = ? WHERE id = ?", (room_name, house_id, id))
        conn.commit()
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM Rooms WHERE id = ?", (id,))
    room = cursor.fetchone()

    return render_template('edit_room.html', room=room)

if __name__ == '__main__':
    app.run(debug=True)
