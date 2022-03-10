from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import DataRequired

class PitchForm(FlaskForm):

  details = TextAreaField('Add your pitch', validators=[DataRequired()])
  category = SelectField("Choose Category",choices=[('interview','interview'),('Adverts','Adverts'),('products','products')])
  pitch = TextAreaField('Your Pitch',validators=[DataRequired()])
  title = TextAreaField('Add your pitch', validators=[DataRequired()])
  submit = SubmitField('Submit')
  
class CommentForm(FlaskForm):
  comment = TextAreaField('Your Comment')
  submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself.',validators = [DataRequired()])
    submit = SubmitField('Submit')