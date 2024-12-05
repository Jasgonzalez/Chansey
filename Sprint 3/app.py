from flask import Flask, request, render_template, redirect, url_for, flash
from sql_db import get_db_connection  # Importing the connection function from sql_db
from services.twilio_sevice import send_sms
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Hardcoded secret key (for now)

# Route to display the form and list of medications
@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM medicine_log")
        medicines = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching medicines: {e}")
        flash("Failed to load medications.")
        medicines = []
    finally:
        connection.close()
    return render_template('index.html', medicines=medicines)

# Route to add a new medication
@app.route('/add', methods=['POST'])
def add_medication():
    med_name = request.form['med_name']
    med_type = request.form['med_type']
    dosage = request.form['dosage']
    start_date = request.form['start_date']
    frequency = request.form['frequency']
    
    try:
        datetime.strptime(start_date, '%Y-%m-%d')  # Validate date format
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO medicine_log (medicine_name, medicine_type, dosage, start_date, frequency)
            VALUES (%s, %s, %s, %s, %s)
        """, (med_name, med_type, dosage, start_date, frequency))
        connection.commit()
        flash("Medication added successfully!")
    except Exception as e:
        print(f"Error adding medication: {e}")
        flash("Failed to add medication.")
    finally:
        connection.close()
    return redirect(url_for('index'))

# Route to update an existing medication
@app.route('/update/<int:med_id>', methods=['POST'])
def update_medication(med_id):
    med_name = request.form['med_name']
    med_type = request.form['med_type']
    dosage = request.form['dosage']
    start_date = request.form['start_date']
    frequency = request.form['frequency']
    
    try:
        datetime.strptime(start_date, '%Y-%m-%d')  # Validate date format
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE medicine_log
            SET medicine_name = %s, medicine_type = %s, dosage = %s, start_date = %s, frequency = %s
            WHERE id = %s
        """, (med_name, med_type, dosage, start_date, frequency, med_id))
        connection.commit()
        flash("Medication updated successfully!")
    except Exception as e:
        print(f"Error updating medication: {e}")
        flash("Failed to update medication.")
    finally:
        connection.close()
    return redirect(url_for('index'))

# Route to delete a medication
@app.route('/delete/<int:med_id>', methods=['POST'])
def delete_medication(med_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM medicine_log WHERE id = %s", (med_id,))
        connection.commit()
        flash("Medication deleted successfully!")
    except Exception as e:
        print(f"Error deleting medication: {e}")
        flash("Failed to delete medication.")
    finally:
        connection.close()
    return redirect(url_for('index'))

# Route to manage and send notifications
@app.route('/notification', methods=['GET', 'POST'])
def notification():
    if request.method == 'POST':
        # Collect form data
        med_name = request.form.get('med_name')
        reminder_time = request.form.get('Reminder_time')
        am_pm = request.form.get('AM_PM')
        start_date = request.form.get('start_date')
        frequency = request.form.get('frequency')
        user_phone = request.form.get('user_phone', '+15403951893')  # Default phone number

        # Insert notification details into the database and send SMS
        try:
            datetime.strptime(start_date, '%Y-%m-%d')  # Validate date format
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO notifications (medicine_name, reminder_time, am_pm, start_date, frequency, user_phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (med_name, reminder_time, am_pm, start_date, frequency, user_phone))
            connection.commit()

            # Send SMS notification
            sms_sid = send_sms(med_name, reminder_time, am_pm, user_phone)
            print(f"SMS sent with SID: {sms_sid}")
            flash("Notification and SMS sent successfully!")
        except Exception as e:
            print(f"Error in notification: {e}")
            flash("Failed to send notification.")
        finally:
            connection.close()
        return redirect(url_for('notification'))

    # Fetch existing notifications and unique medication names
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notifications")
        notifications = cursor.fetchall()

        cursor.execute("SELECT DISTINCT medicine_name FROM medicine_log")
        medications = [row['medicine_name'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        flash("Failed to load notifications.")
        notifications = []
        medications = []
    finally:
        connection.close()

    return render_template('noti.html', notifications=notifications, medications=medications)

# Route to delete a notification
@app.route('/delete_notification/<int:notif_id>', methods=['POST'])
def delete_notification(notif_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = %s", (notif_id,))
        connection.commit()
        flash("Notification deleted successfully!")
    except Exception as e:
        print(f"Error deleting notification: {e}")
        flash("Failed to delete notification.")
    finally:
        connection.close()
    return redirect(url_for('notification'))

# Route to test the Twilio SMS functionality
@app.route('/test_sms', methods=['GET'])
def test_sms():
    try:
        # Call the send_sms function with test values
        sms_sid = send_sms('Test Medication', '3:00', 'AM', '+15403951893')
        return f"Test SMS sent successfully. SID: {sms_sid}"
    except Exception as e:
        return f"Failed to send test SMS: {e}"

@app.route('/emergency_refill', methods=['GET'])
def emergency_refill():
    return render_template('sprint3.html')


# Add route to handle emergency form submission
@app.route('/emergency', methods=['POST'])
def handle_emergency():
    hospital_name = request.form['hospital_name']
    hospital_address = request.form['hospital_address']
    ambulance_request = request.form.get('Ambulance_Request')
    home_address = request.form['home_address']
    personal_phone = request.form['personal_phone']
    ems_description = request.form['EMS_description']
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO emergency_requests 
            (hospital_name, hospital_address, ambulance_needed, home_address, personal_phone, description, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (hospital_name, hospital_address, ambulance_request, home_address, personal_phone, ems_description))
        connection.commit()

        flash("Emergency request submitted successfully!")
    except Exception as e:
        print(f"Error handling emergency request: {e}")
        flash("Emergency request submitted successfully!")
    finally:
        connection.close()
    return redirect(url_for('emergency_refill'))


# Add route to handle refill form submission
@app.route('/add_refill', methods=['POST'])
def add_refill():
    med_name = request.form['med_name']
    med_type = request.form['med_type']
    pickup_date = request.form['Pick-Up_date']
    
    try:
        datetime.strptime(pickup_date, '%Y-%m-%d')  # Validate date format
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO refill_requests (medicine_name, medicine_type, pickup_date, timestamp)
            VALUES (%s, %s, %s, NOW())
        """, (med_name, med_type, pickup_date))
        connection.commit()
        flash("Refill request submitted successfully!")
    except Exception as e:
        print(f"Error adding refill request: {e}")
        flash("Failed to submit refill request.")
    finally:
        connection.close()
    return redirect(url_for('emergency_refill'))


if __name__ == '__main__':
    app.run(debug=True)
