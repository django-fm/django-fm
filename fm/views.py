# coding: utf-8
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

try:
    import json
except ImportError:
    from django.utils import simplejson as json


class JSONResponseMixin(object):
    """
    This is a slightly modified version from django-braces project
    (https://github.com/brack3t/django-braces)
    """
    content_type = None
    json_dumps_kwargs = None

    def get_content_type(self):
        return self.content_type or u"application/json"

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault(u'ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_json_response(self, context_dict, status=200):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(
            context_dict,
            cls=DjangoJSONEncoder,
            **self.get_json_dumps_kwargs()
        ).encode(u'utf-8')
        return HttpResponse(
            json_context,
            content_type=self.get_content_type(),
            status=status
        )


class AjaxFormMixin(JSONResponseMixin):

    message_template = None

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def form_valid(self, form):
        """
        If the request is ajax, save the form and return a json response.
        Otherwise return super as expected.
        """
        self.object = form.save(commit=False)
        self.pre_save()
        self.object.save()
        if hasattr(form, 'save_m2m'):
            form.save_m2m()
        self.post_save()

        if self.request.is_ajax():
            return self.render_json_response(self.get_success_result())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        We have errors in the form. If ajax, return them as json.
        Otherwise, proceed as normal.
        """
        if self.request.is_ajax():
            return self.render_json_response(self.get_error_result(form))
        return super(AjaxFormMixin, self).form_invalid(form)

    def get_message_template_context(self):
        return {
            'instance': self.object,
            'object': self.object
        }

    def get_message_template_html(self):
        return render_to_string(
            self.message_template,
            self.get_message_template_context(),
            context_instance=RequestContext(self.request)
        )

    def get_response_message(self):
        message = ''
        if self.message_template:
            message = self.get_message_template_html()
        return message

    def get_success_result(self):
        return {'status': 'ok', 'message': self.get_response_message()}

    def get_error_result(self, form):
        html = render_to_string(
            self.template_name,
            self.get_context_data(form=form),
            context_instance=RequestContext(self.request)
        )
        return {'status': 'error', 'message': html}


DEFAULT_FORM_TEMPLATE = getattr(settings, "FM_DEFAULT_FORM_TEMPLATE", "fm/form.html")


class AjaxCreateView(AjaxFormMixin, CreateView):

    template_name = DEFAULT_FORM_TEMPLATE


class AjaxUpdateView(AjaxFormMixin, UpdateView):

    template_name = DEFAULT_FORM_TEMPLATE


class AjaxDeleteView(JSONResponseMixin, DeleteView):

    def pre_delete(self):
        pass

    def post_delete(self):
        pass

    def get_success_result(self):
        return {'status': 'ok'}

    def delete(self, request, *args, **kwargs):
        """
        The same logic as in DeleteView but some hooks and
        JSON response in case of AJAX request
        """
        self.object = self.get_object()
        self.pre_delete()
        self.object.delete()
        self.post_delete()

        if self.request.is_ajax():
            return self.render_json_response(self.get_success_result())

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)