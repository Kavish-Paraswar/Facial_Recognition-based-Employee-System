from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from datetime import date
import csv
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration (Using SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Employee Model
class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Password will be stored as a hashed value
    profile_pic = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='employee') 
    face_captured = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        password = request.form['password']

        employee = Employee.query.filter_by(employee_id=employee_id).first()

        if employee and check_password_hash(employee.password, password):
            login_user(employee)
            if employee.role == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('emp_dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    employees = Employee.query.all()
    return render_template('dashboard.html', employee=current_user, employees=employees)

@app.route('/emp_dashboard')
@login_required
def emp_dashboard():
    if current_user.role != 'employee':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    return render_template('emp_dashboard.html', employee=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/employee_details', methods=['GET'])
@login_required
def employee_details():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    search_query = request.args.get('search', '').strip()
    if search_query:
        employees = Employee.query.filter(Employee.role != 'admin', Employee.name.ilike(f'%{search_query}%')).all()
    else:
        employees = Employee.query.filter(Employee.role != 'admin').all()

    return render_template('employee_details.html', employees=employees, employee=current_user, search_query=search_query)

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if not employee_id or not name or not department or not email or not password:
            flash(' All fields are required', 'danger')
            return redirect(url_for('add_employee'))

        existing_employee = Employee.query.filter(
            (Employee.employee_id == employee_id) | (Employee.email == email)).first()
        if existing_employee:
            flash('Employee ID or Email already exists.', 'danger')
            return redirect(url_for('add_employee'))

        new_employee = Employee(employee_id=employee_id, name=name, department=department, email=email, password=password, role='employee')
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added successfully!', 'success')
        return redirect(url_for('employee_details'))

    return render_template('add_employee.html', employee=current_user)

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    employee = Employee.query.get(id)

    if not employee or employee.role != 'employee':
        flash('Cannot edit this user.', 'danger')
        return redirect(url_for('employee_details'))

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.department = request.form['department']
        employee.email = request.form['email']
        db.session.commit()

        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employee_details'))

    return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    employee = Employee.query.get(id)

    if not employee or employee.role != 'employee':
        flash('Cannot delete this user.', 'danger')
        return redirect(url_for('employee_details'))

    db.session.delete(employee)
    db.session.commit()

    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('employee_details'))

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('reset_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('reset_password'))

        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password reset successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('reset_password.html', employee=current_user)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    employee = current_user

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.department = request.form['department']
        employee.email = request.form['email']
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('update_profile.html', employee=employee)

@app.route('/attendance_records')
@login_required
def attendance_records():
    today = date.today().strftime('%Y-%m-%d')
    attendance_file = f"Attendance/attendance_{today}.csv"
    records = []

    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as file:
            reader = csv.DictReader(file)
            records = list(reader)

    return render_template('attendance_records.html', employee=current_user, records=records, today=today)

@app.route('/mark_attendance')
@login_required
def mark_attendance():
    if current_user.role != 'employee':
        flash('Unauthorized', 'danger')
        return redirect(url_for('login'))
    return render_template('mark_attendance.html', employee=current_user)

if __name__ == '__main__':
    app.run(debug=True)
