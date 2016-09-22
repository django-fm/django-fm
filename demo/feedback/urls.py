from django.conf.urls import url
from feedback.views import FeedbackListView, FeedbackCreateView, FeedbackUpdateView, FeedbackDeleteView


urlpatterns = [
    url(r'^$', FeedbackListView.as_view(), name="feedback_list"),
    url(r'^create/$', FeedbackCreateView.as_view(), name="feedback_create"),
    url(r'^update/(?P<feedback_pk>\d+)/$', FeedbackUpdateView.as_view(), name="feedback_update"),
    url(r'^delete/(?P<feedback_pk>\d+)/$', FeedbackDeleteView.as_view(), name="feedback_delete"),
]
