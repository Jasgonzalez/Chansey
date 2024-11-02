from flask import Flask, request, render_template, redirect, url_for, flash
from sql_db import get_db_connection  # Importing the connection function from sql_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Route to display the form and list of medications
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicine_log")
    medicines = cursor.fetchall()
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

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO medicine_log (medicine_name, medicine_type, dosage, start_date, frequency)
        VALUES (%s, %s, %s, %s, %s)
    """, (med_name, med_type, dosage, start_date, frequency))
    connection.commit()
    connection.close()
    flash("Medication added successfully!")
    return redirect(url_for('index'))

# Route to update an existing medication
@app.route('/update/<int:med_id>', methods=['POST'])
def update_medication(med_id):
    med_name = request.form['med_name']
    med_type = request.form['med_type']
    dosage = request.form['dosage']
    start_date = request.form['start_date']
    frequency = request.form['frequency']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE medicine_log
        SET medicine_name = %s, medicine_type = %s, dosage = %s, start_date = %s, frequency = %s
        WHERE id = %s
    """, (med_name, med_type, dosage, start_date, frequency, med_id))
    connection.commit()
    connection.close()
    flash("Medication updated successfully!")
    return redirect(url_for('index'))

# Route to delete a medication
@app.route('/delete/<int:med_id>', methods=['POST'])
def delete_medication(med_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM medicine_log WHERE id = %s", (med_id,))
    connection.commit()
    connection.close()
    flash("Medication deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
