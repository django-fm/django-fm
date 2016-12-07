from django import forms
from feedback.models import Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import datetime


class FeedbackForm(forms.ModelForm):

    created = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(options={
            "calendarWeeks": True,
            "showClear": True,
            "showClose": True,
            "format": "YYYY-MM-DD HH:mm:ss",
            "maxDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pickTime": True,
        }))

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'test-form'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('url'),
            Field('text'),
            Field('created'),
        )

    class Meta:
        model = Feedback
        exclude = ('update_count',)
