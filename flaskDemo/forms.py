from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db

from flaskDemo.models import User, Post, Patient, Laboratory, Test, Symptom, Treatment, Strain, HadDisease

from flaskDemo.models import User, Post, Patient, Laboratory, Test, Symptom, Treatment

from wtforms.fields.html5 import DateField

test_result = Test.query.with_entities(Test.result).distinct()
patient_ssn = Patient.query.with_entities(Patient.ssn).distinct()
lab_id = Laboratory.query.with_entities(Laboratory.id).distinct()

symptom_id = Symptom.query.with_entities(Symptom.s_id).distinct()
treatment_id = Treatment.query.with_entities(Treatment.t_id).distinct()
strain_id = Strain.query.with_entities(Strain.strainid).distinct()

sex = Patient.query.with_entities(Patient.sex).distinct()
symptom_id = Symptom.query.with_entities(Symptom.s_id).distinct()
treatment_id = Treatment.query.with_entities(Treatment.t_id).distinct()

#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above

# myChoices2 = [(row[0],row[0]) for row in ssns]  # change

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
    ssn=IntegerField('Social Security Number', validators=[DataRequired()])
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


class PatientForm(FlaskForm):
    ssn=IntegerField('Social Security Number', validators=[DataRequired()])
    name=StringField('Name', validators=[DataRequired()])
    dob=DateField('Date of Birth', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    sex=StringField('Sex', validators=[DataRequired()])
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

class SymptomForm(FlaskForm):
    s_id=IntegerField('Symptom ID', validators=[DataRequired()])
    s_name=StringField('Symptom Name', validators=[DataRequired()])
    submit = SubmitField('Add this test.')

class TreatmentForm(FlaskForm):
    t_id=IntegerField('Treatment ID', validators=[DataRequired()])
    t_name =StringField('Treatment Name', validators=[DataRequired()])
    s_id = SelectField('Symptom ID', choices=symptom_choice)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    submit = SubmitField('Add this test.')

class StrainForm(FlaskForm):
    strain_id=IntegerField('Strain ID', validators=[DataRequired()])
    strain_name =StringField('Strain Name', validators=[DataRequired()])
    submit = SubmitField('Add this test.')

class HadDiseaseForm(FlaskForm):
    duration = SelectField('Duration', [DataRequired()]))
    date_of_disease_start = SelectField('DATE', [DataRequired()]))
    submit = SubmitField('Add this test.')

'''    
class DeptUpdateForm(FlaskForm):
#    dnumber=IntegerField('Department Number', validators=[DataRequired()])

    dnumber = HiddenField("")
    dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])

    ssn = HiddenField("")

    name=StringField('Patient Name:', validators=[DataRequired(),Length(max=30)])

#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])
#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
    address = StringField("Address", validators=[DataRequired(),Length(max=30)])  # myChoices defined at top
    sex = SelectField("Sex", choices=sex_choice)
    dob = DateField("Date of Birth:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
    submit = SubmitField('Update this patient')

# got rid of def validate_dnumber

    def validate_ssn(self, ssn):    # apparently in the company DB, dname is specified as unique
         patient = Patient.query.filter_by(ssn=ssn.data).first()
         if patient and (str(patient.ssn) != str(self.ssn.data)):
             raise ValidationError('That patient name is already being used. Please choose a different name.')

class PatientForm(PatientUpdateForm):

    ssn=IntegerField('Social Security Number', validators=[DataRequired()])
    submit = SubmitField('Add this patient.')

    def validate_ssn(self, ssn):    #because dnumber is primary key and should be unique
        patient = Patient.query.filter_by(ssn=ssn.data).first()
        if patient:
            raise ValidationError('That patient number is taken. Please choose a different one.')

class LabUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    id = HiddenField("")

    name=StringField('Laboratory Name:', validators=[DataRequired(),Length(max=30)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

    location = StringField("Location", validators=[DataRequired(),Length(max=30)])
    submit = SubmitField('Update this laboratory')
    

# got rid of def validate_dnumber

    def validate_id(self, id):    # apparently in the company DB, dname is specified as unique
         lab = Laboratory.query.filter_by(id=id.data).first()
         if lab and (str(lab.id) != str(self.id.data)):
             raise ValidationError('That laboratory name is already being used. Please choose a different name.')


class LabForm(LabUpdateForm):

    id=IntegerField('ID', validators=[DataRequired()])
    submit = SubmitField('Add this laboratory.')

    def validate_id(self, id):    #because dnumber is primary key and should be unique
        lab = Laboratory.query.filter_by(id=id.data).first()
        if lab:
            raise ValidationError('That laboratory number is taken. Please choose a different one.')

class TestUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    id = HiddenField("")

    date=DateField('Test Date', validators=[DataRequired()])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

    result=SelectField('Test Result', choices=test_Choices)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    lab_id = SelectField('Lab ID', choices=lab_choice)
    submit = SubmitField('Update this test')
    

# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
#    mgr_start = DateField("Manager's Start Date")
#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
    mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
    submit = SubmitField('Update this department')
# got rid of def validate_dnumber
    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
         dept = Department.query.filter_by(dname=dname.data).first()
         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
             raise ValidationError('That department name is already being used. Please choose a different name.')
class DeptForm(DeptUpdateForm):
    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    submit = SubmitField('Add this department')
    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
        dept = Department.query.filter_by(dnumber=dnumber.data).first()
        if dept:
            raise ValidationError('That department number is taken. Please choose a different one.')
            '''


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

class TreatmentForm(FlaskForm):
    t_id=IntegerField('Treatment ID', validators=[DataRequired()])
    t_name =StringField('Treatment Name', validators=[DataRequired()])
    s_id = SelectField('Symptom ID', choices=symptom_choice)
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    submit = SubmitField('Add this test.')

class TreatmentUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    t_id = HiddenField("")

    t_name=StringField('Treatment Name:', validators=[DataRequired(),Length(max=30)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
    p_ssn = SelectField('Patient SSN', choices=patient_choice)
    s_id = SelectField('Symptom ID', choices=symptom_choice)
    submit = SubmitField('Update this treatment.')

# got rid of def validate_dnumber

    def validate_id(self, t_id):    # apparently in the company DB, dname is specified as unique
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
            
