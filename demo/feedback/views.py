from django.views.generic import ListView
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from feedback.models import Feedback
from feedback.forms import FeedbackForm


class FeedbackListView(ListView):
    model = Feedback


class FeedbackCreateView(AjaxCreateView):

    form_class = FeedbackForm


class FeedbackUpdateView(AjaxUpdateView):

    message_template = "feedback/feedback_instance.html"
    form_class = FeedbackForm
    model = Feedback
    pk_url_kwarg = 'feedback_pk'

    def pre_save(self):
        self.object.update_count += 1


class FeedbackDeleteView(AjaxDeleteView):

    model = Feedback
    pk_url_kwarg = 'feedback_pk'