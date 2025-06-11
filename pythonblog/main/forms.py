from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ComboForm(FlaskForm):
    combo_string = StringField(
        "combo_string", validators=[DataRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Convert| Text ➢ Image")
