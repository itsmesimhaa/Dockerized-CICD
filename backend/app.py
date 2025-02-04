import os
from flask import Flask, request, render_template
import pymysql
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Database configuration using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')  # Get the MySQL host from the environment
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')  # Get the MySQL user from the environment
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')  # Get the MySQL password from the environment
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')  # Get the MySQL database name from the environment

# Setup MySQL connection
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'GET':
        # Render the appointment booking form
        return render_template('appointments.html', message=None, status=None)

    # Handle the form submission (POST)
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date = request.form.get('date')
    time = request.form.get('time')

    if not all([name, email, phone, date, time]):
        return render_template('appointments.html', message="All fields are required.", status="error")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Insert appointment details into the database
            sql = "INSERT INTO appointments (name, email, phone, date, time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, phone, date, time))
            connection.commit()

        # After successful booking, send a success message
        success_message = f"Appointment booked successfully for {name} on {date} at {time}."
        return render_template('appointments.html', message=success_message, status="success")

    except Exception as e:
        # Handle database connection or SQL execution errors
        return render_template('appointments.html', message=f"An error occurred: {str(e)}", status="error")

    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
