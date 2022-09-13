from wtforms import StringField, SubmitField, PasswordField, RadioField, SearchField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired as required, Length, EqualTo
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileRequired


class UserForm(FlaskForm):
    """A form for taking user details for login, signup, etc."""
    firstname = StringField('Your first name', [required()])
    lastname = StringField('Your last name', [required()])
    email = StringField('Your email', [required()])
    role = StringField('Your current role')
    tel = StringField('Your phone number', [Length(10, 12, 'Number is invalid')])
    password = PasswordField('Your password')
    confirm = PasswordField('Type your password again', [EqualTo('password')])
    submit = SubmitField('Login')

class Contact(FlaskForm):
    """Creates and validates message"""
    email = SearchField('Your Email Address', [required()])
    name = StringField()
    subject = StringField()
    message = CKEditorField('Type in your message', [required()])
    submit = SubmitField('Submit Message')


class NewArticle(FlaskForm):
    """Creates a post form"""
    subject = StringField('Enter your post title')
    message = CKEditorField()
    category = StringField(validators=[required()])
    submit = SubmitField()
    cover = FileField('Cover image')


class UploadFile(FlaskForm):
    """File Upload Form"""
    category = RadioField('Select the file type', [required()],
    choices=[('images', 'Image'), ('documents', 'Document (Example: pdf, docx, etc)'), ('videos', 'Video')])
    content = FileField('Cover image', [FileRequired('You must select a file')],)
    f_name = StringField('Type in a short file name')
    message = CKEditorField('Describe the file in detail (For videos and images)')
    submit = SubmitField()


class Search(FlaskForm):
    search = SearchField()
    submit = SubmitField()

class NoticeForm(FlaskForm):
    """Creates a form for Notice"""
    message = CKEditorField('Your notice body here', [
                            required('Please type your notice')])
    subject = StringField('Your notice title', [
                          required('Please type your notice title')])
    submit = SubmitField()
