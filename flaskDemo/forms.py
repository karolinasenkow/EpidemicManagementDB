from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Post, Patient, Laboratory, Test, Symptom, Treatment
from wtforms.fields.html5 import DateField

test_result = Test.query.with_entities(Test.result).distinct()
patient_ssn = Patient.query.with_entities(Patient.ssn).distinct()
lab_id = Laboratory.query.with_entities(Laboratory.id).distinct()
sex = Patient.query.with_entities(Patient.sex).distinct()
symptom_id = Symptom.query.with_entities(Symptom.s_id).distinct()
treatment_id = Treatment.query.with_entities(Treatment.t_id).distinct()

# test choices (select field)
results=list()
for row in test_result:
    rowDict=row._asdict()
    results.append(rowDict)
test_Choices = [(row['result'],row['result']) for row in results]

# patient choices (select field)
p_results=list()
for row in patient_ssn:
    rowDict=row._asdict()
    p_results.append(rowDict)
patient_choice = [(row['ssn'],row['ssn']) for row in p_results]

# lab choices (select field)
l_results=list()
for row in lab_id:
    rowDict=row._asdict()
    l_results.append(rowDict)
lab_choice = [(row['id'],row['id']) for row in l_results]

# sex choices (select field)
s_results=list()
for row in sex:
    rowDict=row._asdict()
    s_results.append(rowDict)
sex_choice = [(row['sex'],row['sex']) for row in s_results]

#sympotm choices (select field)
s_results = list()
for row in symptom_id:
    rowDict = row._asdict()
    s_results.append(rowDict)
symptom_choice = [(row['s_id'], row['s_id']) for row in s_results]

t_results = list()
for row in treatment_id:
    rowDict = row._asdict()
    t_results.append(rowDict)
symptom_choice = [(row['t_id'], row['t_id']) for row in t_results]

regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2




class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class PatientForm(FlaskForm):
    ssn=IntegerField('Social Security Number', validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    name=StringField('Name', validators=[DataRequired()])
    dob=DateField('Date of Birth', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    sex=SelectField('Sex', choices=sex_choice)
    submit = SubmitField('Add this patient.')

class LabForm(FlaskForm):
    id=IntegerField('Lab ID', validators=[DataRequired()])
    name=StringField('Name', validators=[DataRequired()])
    location=StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add this laboratory.')

class TestForm(FlaskForm):
    id=IntegerField('Test ID', validators=[DataRequired()])
    date=DateField('Test Date', validators=[DataRequired()])
    result=SelectField('Test Result', choices=test_Choices)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    lab_id = SelectField('Lab ID', choices=lab_choice)
    submit = SubmitField('Add this test.')

class PatientUpdateForm(FlaskForm):


    ssn = HiddenField("")
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    name=StringField('Patient Name:', validators=[DataRequired(),Length(max=30)])
    address = StringField("Address", validators=[DataRequired(),Length(max=30)])  
    sex = SelectField("Sex", choices=sex_choice)
    dob = DateField("Date of Birth:", format='%Y-%m-%d')  
    submit = SubmitField('Update this patient')



    def validate_ssn(self, ssn):    
         patient = Patient.query.filter_by(ssn=ssn.data).first()
         if patient and (str(patient.ssn) != str(self.ssn.data)):
             raise ValidationError('That patient name is already being used. Please choose a different name.')

class PatientForm(PatientUpdateForm):

    ssn=IntegerField('Social Security Number', validators=[DataRequired()])
    submit = SubmitField('Add this patient.')

    def validate_ssn(self, ssn): 
        patient = Patient.query.filter_by(ssn=ssn.data).first()
        if patient:
            raise ValidationError('That patient number is taken. Please choose a different one.')

class LabUpdateForm(FlaskForm):


    id = HiddenField("")
    name=StringField('Laboratory Name:', validators=[DataRequired(),Length(max=30)])
    location = StringField("Location", validators=[DataRequired(),Length(max=30)])
    submit = SubmitField('Update this laboratory')
    

    def validate_id(self, id):   
         lab = Laboratory.query.filter_by(id=id.data).first()
         if lab and (str(lab.id) != str(self.id.data)):
             raise ValidationError('That laboratory name is already being used. Please choose a different name.')


class LabForm(LabUpdateForm):

    id=IntegerField('ID', validators=[DataRequired()])
    submit = SubmitField('Add this laboratory.')

    def validate_id(self, id):    
        lab = Laboratory.query.filter_by(id=id.data).first()
        if lab:
            raise ValidationError('That laboratory number is taken. Please choose a different one.')

class TestUpdateForm(FlaskForm):

    id = HiddenField("")

    date=DateField('Test Date', validators=[DataRequired()])
    result=SelectField('Test Result', choices=test_Choices)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    lab_id = SelectField('Lab ID', choices=lab_choice)
    submit = SubmitField('Update this test')
    

# got rid of def validate_dnumber

    def validate_id(self, id):    # apparently in the company DB, dname is specified as unique
         test = Test.query.filter_by(id=id.data).first()
         if test and (str(test.id) != str(self.id.data)):
             raise ValidationError('That test name is already being used. Please choose a different name.')


class LabForm(LabUpdateForm):

    id=IntegerField('ID', validators=[DataRequired()])
    submit = SubmitField('Add this test.')

    def validate_id(self, id):    #because dnumber is primary key and should be unique
        test = Test.query.filter_by(id=id.data).first()
        if test:
            raise ValidationError('That test number is taken. Please choose a different one.')

class SymptomForm(FlaskForm):
    s_id=IntegerField('Symptom ID', validators=[DataRequired()])
    s_name=StringField('Symptom Name', validators=[DataRequired()])
    submit = SubmitField('Add this test.')

class SymptomUpdateForm(FlaskForm):

    s_id = HiddenField("")
    s_name=StringField('Symptom Name:', validators=[DataRequired(),Length(max=30)])
    submit = SubmitField('Update this treatment.')

    def validate_id(self, s_id):   
         symptom = Symptom.query.filter_by(s_id=s_id.data).first()
         if treatment and (str(symptom.s_id) != str(self.s_id.data)):
             raise ValidationError('That symptom already being exists. Please choose a different entry.')

class Symptom(SymptomUpdateForm):

    s_id=IntegerField('Symptom ID', validators=[DataRequired()])
    submit = SubmitField('Add this Symptom.')

    def validate_id(self, s_id):
        symptom = Symptom.query.filter_by(s_id=s_id.data).first()
        if symptom:
            raise ValidationError('That symptom id already exists. Please try another entry')


class TreatmentForm(FlaskForm):
    t_id=IntegerField('Treatment ID', validators=[DataRequired()])
    t_name =StringField('Treatment Name', validators=[DataRequired()])
    s_id = SelectField('Symptom ID', choices=symptom_choice)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    submit = SubmitField('Add this test.')

class TreatmentUpdateForm(FlaskForm):

    t_id = HiddenField("")
    t_name=StringField('Treatment Name:', validators=[DataRequired(),Length(max=30)])
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    s_id = SelectField('Symptom ID', choices=symptom_choice)
    submit = SubmitField('Update this treatment.')

    def validate_id(self, t_id):   
         treatment = Treatment.query.filter_by(t_id=t_id.data).first()
         if treatment and (str(treatment.t_id) != str(self.t_id.data)):
             raise ValidationError('That Treatment already being exists. Please choose a different entry.')

class TreatmentForm(TreatmentUpdateForm):

    t_id=IntegerField('Treatment ID', validators=[DataRequired()])
    submit = SubmitField('Add this Treatment.')

    def validate_id(self, t_id):
        treatment = Treatment.query.filter_by(t_id=t_id.data).first()
        if treatment:
            raise ValidationError('That treatment id already exists. Please try another entry')
            


