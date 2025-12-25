from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_12345'

# In-memory storage for students (dictionary)
students_data = {}
student_id_counter = 1

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    global student_id_counter
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        course = request.form.get('course')
        
        # Check if email already exists
        email_exists = any(student['email'] == email for student in students_data.values())
        
        if email_exists:
            flash('Email already registered!', 'error')
        else:
            # Add student to dictionary
            students_data[student_id_counter] = {
                'id': student_id_counter,
                'name': name,
                'email': email,
                'phone': phone,
                'course': course
            }
            student_id_counter += 1
            flash('Registration successful!', 'success')
            return redirect(url_for('view_students'))
    
    return render_template('register.html')

# View all students
@app.route('/students')
def view_students():
    # Convert dictionary to list for template
    students_list = list(students_data.values())
    return render_template('students.html', students=students_list)

# Search student route
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '').lower()
    
    # Filter students based on search term
    filtered_students = [
        student for student in students_data.values()
        if search_term in student['name'].lower() or search_term in student['email'].lower()
    ]
    
    return render_template('students.html', students=filtered_students)

# Delete student route
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    if student_id in students_data:
        del students_data[student_id]
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found!', 'error')
    
    return redirect(url_for('view_students'))

# Update/Edit student route
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if student_id not in students_data:
        flash('Student not found!', 'error')
        return redirect(url_for('view_students'))
    
    if request.method == 'POST':
        students_data[student_id]['name'] = request.form.get('name')
        students_data[student_id]['email'] = request.form.get('email')
        students_data[student_id]['phone'] = request.form.get('phone')
        students_data[student_id]['course'] = request.form.get('course')
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('view_students'))
    
    student = students_data[student_id]
    return render_template('edit.html', student=student)

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
