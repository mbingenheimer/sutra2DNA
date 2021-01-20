from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class IsBinary():
	def __call__(self, form, field):
		for i in field.data:
			if i != '1' and i != '0':
				raise ValidationError("Field must be a binary string")

class HammingInput(FlaskForm):
	message = StringField('Message', validators=[DataRequired(), Length(min=4), IsBinary()])
	encodeButton = SubmitField('Encode')