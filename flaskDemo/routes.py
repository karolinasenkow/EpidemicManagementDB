import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PatientForm, LabForm, TestForm, PatientUpdateForm, LabUpdateForm, TestUpdateForm, SymptomForm, TreatmentForm, TreatmentUpdateForm, SymptomUpdateForm
from flaskDemo.models import User, Post, Patient, Test, Laboratory, Symptom, Treatment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import and_


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
    # subquery: return patients that are negative
    sql_query = "SELECT patient.name FROM patient WHERE ssn IN (SELECT p_ssn FROM Test WHERE test.result = 'negative');"
    cursor = db.session.execute(sql_query)
    row = ''
    returnString = str(row)
    row = cursor.fetchone()
    while row is not None:
        returnString += "\n" + str(row)
        row = cursor.fetchone()
    posts = Patient.query.all()
    return render_template('patient_home.html', title='Home', returnString=returnString, outString=posts)

@app.route("/")
@app.route("/home/lab")
def lab_home():
    # aggregate: return number of tests for each lab
    sql_query = "SELECT laboratory.name, COUNT(test.id) FROM Test, Laboratory WHERE test.lab_id = laboratory.id GROUP BY laboratory.name;"
    cursor = db.session.execute(sql_query)
    row = ''
    returnString = str(row)
    row = cursor.fetchone()
    while row is not None:
        returnString += "\n" + str(row)
        row = cursor.fetchone()
    posts = Laboratory.query.all()
    return render_template('lab_home.html', title='Home', returnString=returnString, outString=posts)

@app.route("/")
@app.route("/home/test")
def test_home():
    posts = Test.query.all()
    return render_template('test_home.html', title='Home',outString=posts)

@app.route("/")
@app.route("/home/symptom")
def symptom_home():
    # left join: return treatment for each symptom
    sql_query = "SELECT treatment.t_name, symptom.s_name FROM symptom LEFT JOIN treatment on(symptom.s_id = treatment.s_id) GROUP BY treatment.t_name;"
    cursor = db.session.execute(sql_query)
    row = ''
    returnString = str(row)
    row = cursor.fetchone()
    while row is not None:
        returnString += "\n" + str(row)
        row = cursor.fetchone()
    posts = Symptom.query.all()
    return render_template('symptom_home.html', title='Home',returnString=returnString, outString=posts)

@app.route("/")
@app.route("/home/treatment")
def treatment_home():
    # compound condition: return symptoms where treatment is nyquil
    sql_query = "SELECT symptom.s_name FROM symptom, treatment WHERE treatment.s_id = symptom.s_id AND treatment.t_name = 'nyquil'"
    cursor = db.session.execute(sql_query)
    row = ''
    returnString = str(row)
    row = cursor.fetchone()
    while row is not None:
        returnString += "\n" + str(row[0])
        row = cursor.fetchone()
    posts = Treatment.query.all()
    return render_template('treatment_home.html', title='Home', returnString=returnString, outString=posts) 


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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            patient.image_file = picture_file
        patient = Patient(ssn=form.ssn.data, name=form.name.data,dob=form.dob.data,address=form.address.data,sex=form.sex.data)
        db.session.add(patient)
        db.session.commit()
        flash('You have added a new patient!', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('create_patient.html', title='New Patient',
                           form=form, legend='New Patient')

@app.route("/patient/<ssn>")
@login_required
def patient(ssn):
    patient = Patient.query.get_or_404(ssn)
    return render_template('patient.html', title=patient.ssn, patient=patient, now=datetime.utcnow())

@app.route("/patient/<ssn>/update", methods=['GET', 'POST'])
@login_required
def update_patient(ssn):
    patient = Patient.query.get_or_404(ssn)
    currentPatient = patient.name

    form = PatientUpdateForm()
    if form.validate_on_submit():         
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            patient.image_file = picture_file
        if currentPatient !=form.name.data:
            patient.name=form.name.data
        patient.dob=form.dob.data
        patient.address=form.address.data
        patient.sex=form.sex.data
        db.session.commit()
        flash('Your patient has been updated!', 'success')
        return redirect(url_for('patient', ssn=ssn))
    elif request.method == 'GET':           

        form.ssn.data = patient.ssn
        form.name.data = patient.name
        form.dob.data = patient.dob
        form.address.data = patient.address
        form.sex.data = patient.sex
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('create_patient.html', title='Update Patient',
                           form=form, legend='Update Patient')

@app.route("/patient/<ssn>/delete", methods=['POST'])
@login_required
def delete_patient(ssn):
    patient = Patient.query.get_or_404(ssn)
    flash('You cannot delete a patient. Reassign patient for test before deleting.', 'danger')
    return redirect(url_for('test_home', id=id))
    db.session.delete(patient)
    db.session.commit()
    flash('The patient has been deleted!', 'success')
    return redirect(url_for('home'))

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

@app.route("/lab/<id>")
@login_required
def lab(id):
    laboratory = Laboratory.query.get_or_404(id)
    return render_template('laboratory.html', title=laboratory.id, laboratory=laboratory, now=datetime.utcnow())

@app.route("/lab/<id>/update", methods=['GET', 'POST'])
@login_required
def update_lab(id):
    lab = Laboratory.query.get_or_404(id)
    currentLab = lab.name

    form = LabUpdateForm()
    if form.validate_on_submit():          
        if currentLab !=form.name.data:
            lab.name=form.name.data
        lab.location=form.location.data
        db.session.commit()
        flash('Your laboratory has been updated!', 'success')
        return redirect(url_for('lab_home', id=id))
    elif request.method == 'GET':              

        form.id.data = lab.id
        form.name.data = lab.name
        form.location.data = lab.location
    return render_template('create_lab.html', title='Update Laboratory',
                           form=form, legend='Update Laboratory')

@app.route("/lab/<id>/delete", methods=['POST'])
@login_required
def delete_lab(id):
    lab = Laboratory.query.get_or_404(id)
    flash('You cannot delete a laboratory. Reassign lab for test before deleting.', 'danger')
    return redirect(url_for('test_home', id=id))
    db.session.delete(lab)
    db.session.commit()
    flash('The laboratory has been deleted!', 'success')
    return redirect(url_for('home'))


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

@app.route("/test/<id>")
@login_required
def test(id):
    test = Test.query.get_or_404(id)
    return render_template('test.html', title=test.id, test=test, now=datetime.utcnow())

@app.route("/test/<id>/update", methods=['GET', 'POST'])
@login_required
def update_test(id):
    test = Test.query.get_or_404(id)
    currentTest = test.result

    form = TestUpdateForm()
    if form.validate_on_submit():      
        if currentTest !=form.result.data:
            test.result=form.result.data
        test.date=form.date.data
        test.p_ssn=form.p_ssn.data
        test.lab_id=form.lab_id.data
        db.session.commit()
        flash('Your test has been updated!', 'success')
        return redirect(url_for('test', id=id))
    elif request.method == 'GET':            

        form.id.data = test.id
        form.date.data = test.date
        form.result.data = test.result
        form.p_ssn.data = test.p_ssn
        form.lab_id.data = test.lab_id
    return render_template('create_test.html', title='Update Test',
                           form=form, legend='Update Test')

@app.route("/test/<id>/delete", methods=['POST'])
@login_required
def delete_test(id):
    test = Test.query.get_or_404(id)
    db.session.delete(test)
    db.session.commit()
    flash('The test has been deleted!', 'success')
    return redirect(url_for('home'))

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

@app.route("/symptom/<s_id>")
@login_required
def symptom(s_id):
    symptom = Symptom.query.get_or_404(s_id)
    return render_template('symptom.html', title=symptom.s_id, symptom=symptom, now=datetime.utcnow())

@app.route("/symptom/<s_id>/update", methods=['GET', 'POST'])
@login_required
def update_symptom(s_id):

    symptom = Symptom.query.get_or_404(s_id)
    currentSymptom = symptom.s_name

    form = SymptomUpdateForm()
    if form.validate_on_submit():          
        if currentSymptom !=form.s_name.data:
            symptom.s_name=form.s_name.data
            symptom.s_id = form.s_id.data
        
        db.session.commit()
        flash('Symptom has been updated!', 'success')
        return redirect(url_for('symptom_home', s_id=symptom.s_id))
    elif request.method == 'GET':              
        form.s_id.data = symptom.s_id
        form.s_name.data = symptom.s_name
  
    return render_template('create_symptom.html', title='Update Symptom',
                           form=form, legend='Update Symptom')

@app.route("/symptom/<s_id>/delete", methods=['POST'])
@login_required
def delete_symptom(s_id):
    symptom = Symptom.query.get_or_404(s_id)
    db.session.delete(symptom)
    db.session.commit()
    flash('The symptom has been deleted!', 'success')
    return redirect(url_for('symptom_home'))



@app.route("/")
@app.route("/treatment/new", methods=['GET', 'POST'])
@login_required
def new_treatment():
    form = TreatmentForm()
    if form.validate_on_submit():
        treatment = Treatment(t_id=form.t_id.data, s_id = form.s_id.data, t_name = form.t_name.data, p_ssn=form.p_ssn.data)
        db.session.add(treatment)
        db.session.commit()
        flash('You have added a new treatment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_treatment.html', title='New Treatment',
                           form=form, legend='New Treatment')

@app.route("/treatment/<t_id>")
@login_required
def treatment(t_id):
    # inner join: return treatment for each symptom
    treatment = Treatment.query.get_or_404(t_id)
    result = Treatment.query.join(Symptom, Treatment.s_id == Symptom.s_id) \
    .add_columns(Treatment.t_name, Symptom.s_name) \
    .filter(Treatment.s_id == Symptom.s_id).group_by(Treatment.t_name)
    cursor = db.session.execute(result)
    row = ''
    returnString = str(row)
    row = cursor.fetchone()
    while row is not None:
        returnString += "\n{" + str(row[2]) + ':\n' + str(row[4]) + '}'
        row = cursor.fetchone()
    return render_template('treatment.html', title=treatment.t_id, returnString=returnString, treatment=treatment, now=datetime.utcnow())

@app.route("/treatment/<t_id>/update", methods=['GET', 'POST'])
@login_required
def update_treatment(t_id):

    treatment = Treatment.query.get_or_404(t_id)
    patient = Patient.query.get_or_404(treatment.p_ssn)
    currentTreatment = treatment.t_name

    form = TreatmentUpdateForm()
    if form.validate_on_submit():          
        if currentTreatment !=form.t_name.data:
            treatment.t_name=form.t_name.data
            treatment.p_ssn = form.p_ssn.data
            treatment.s_id = form.s_id.data
        
        db.session.commit()
        flash('Treatment has been updated!', 'success')
        return redirect(url_for('treatment', t_id=treatment.t_id))
    elif request.method == 'GET':              
        form.p_ssn.data = treatment.p_ssn
        form.t_name.data = treatment.t_name
        form.t_name.data = treatment.s_id
       
    return render_template('create_treatment.html', title='Update Treatment',
                           form=form, legend='Update Treatment')

@app.route("/treatment/<t_id>/delete", methods=['POST'])
@login_required
def delete_treatment(t_id):
    treatment = Treatment.query.get_or_404(t_id)
    db.session.delete(treatment)
    db.session.commit()
    flash('The treatment has been deleted!', 'success')
    return redirect(url_for('home'))




