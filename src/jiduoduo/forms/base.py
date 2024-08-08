from flask import flash
from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash(f"{getattr(self, field).label.text}: {error}", 'error')
