import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PatientForm, LabForm, TestForm, SymptomForm, TreatmentForm
from flaskDemo.models import User, Post, Patient, Test, Laboratory, Symptom, Treatment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime



'''def home():
    results = Department.query.all()
    return render_template('dept_home.html', outString = results)
    posts = Post.query.all()
    return render_template('home.html', posts=posts)
    results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
               .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
               .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
    results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
              .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
    return render_template('join.html', title='Join',joined_1_n=results, joined_m_n=results2) '''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Choose one of the following to view info.')

@app.route("/")
@app.route("/home/patient")
def patient_home():
    posts = Patient.query.all()
    return render_template('patient_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/lab")
def lab_home():
    posts = Laboratory.query.all()
    return render_template('lab_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/test")
def test_home():
    posts = Test.query.all()
    return render_template('test_home.html', title='Home',outString=posts) 

@app.route("/")
@app.route("/home/symptom")
def symptom_home():
    posts = Symptom.query.all()
    return render_template('symptom_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/treatment")
def treatment_home():
    posts = Treatment.query.all()
    return render_template('treatment_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/strain")
def symptom_home():
    posts = Symptom.query.all()
    return render_template('strain_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/hadDisease")
def symptom_home():
    posts = Symptom.query.all()
    return render_template('had_disease_home.html', title='Home',outString=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/")
@app.route("/patient/new", methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(ssn=form.ssn.data, name=form.name.data,dob=form.dob.data,address=form.address.data,sex=form.sex.data)
        db.session.add(patient)
        db.session.commit()
        flash('You have added a new patient!', 'success')
        return redirect(url_for('home'))
    return render_template('create_patient.html', title='New Patient',
                           form=form, legend='New Patient')

@app.route("/")
@app.route("/lab/new", methods=['GET', 'POST'])
@login_required
def new_lab():
    form = LabForm()
    if form.validate_on_submit():
        lab = Laboratory(id=form.id.data, name=form.name.data,location=form.location.data)
        db.session.add(lab)
        db.session.commit()
        flash('You have added a new laboratory!', 'success')
        return redirect(url_for('home'))
    return render_template('create_lab.html', title='New Laboratory',
                           form=form, legend='New Laboratory')
@app.route("/")
@app.route("/test/new", methods=['GET', 'POST'])
@login_required
def new_test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test(id=form.id.data, date=form.date.data,result=form.result.data,p_ssn=form.p_ssn.data,lab_id=form.lab_id.data)
        db.session.add(test)
        db.session.commit()
        flash('You have added a new test!', 'success')
        return redirect(url_for('home'))
    return render_template('create_test.html', title='New Test',
                           form=form, legend='New Test')

@app.route("/")
@app.route("/symptom/new", methods=['GET', 'POST'])
@login_required
def new_symptom():
    form = SymptomForm()
    if form.validate_on_submit():
        symptom = Symptom(s_id=form.s_id.data, s_name=form.s_name.data)
        db.session.add(symptom)
        db.session.commit()
        flash('You have added a new symptom!', 'success')
        return redirect(url_for('home'))
    return render_template('create_symptom.html', title='New Symptom',
                           form=form, legend='New Symptom')

@app.route("/")
@app.route("/strain/new", methods=['GET', 'POST'])
@login_required
def new_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        strain = Strain(strain_id=form.strain_id.data, strain_name = form.strain_name.data)
        db.session.add(strain)
        db.session.commit()
        flash('You have added a new treatment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_strain.html', title='New Strain',
                           form=form, legend='New Strain')

@app.route("/")
@app.route("/treatment/new", methods=['GET', 'POST'])
@login_required
def new_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        treatment = Treatment(t_id=form.t_id.data, t_name = form.t_name.data, s_id = form.s_id.data, p_ssn=form.p_ssn.data)
        db.session.add(treatment)
        db.session.commit()
        flash('You have added a new treatment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_treatment.html', title='New Treatment',
                           form=form, legend='New Treatment')


'''
@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')
@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())
@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
@login_required
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname
    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        form.dnumber.data = dept.dnumber
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('create_dept.html', title='Update Department',
                           form=form, legend='Update Department')
@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home')) '''
