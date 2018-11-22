[Live example](http://djangofm.herokuapp.com/) - see the source code of demonstration in `demo` repository folder.

Django FM
=========

Requires jQuery and Bootstrap 3 on client side. Depends on [django-crispy-forms](https://github.com/maraujop/django-crispy-forms/) on server side.

This app allows to make responsive AJAX modal forms for creating, editing, deleting objects in Django. This is a very personalized approach to quickly build admin-like interfaces. It reduces an amount of time and code when making tedious Django work.

Install:

```bash
pip install django-fm
```

Add `crispy_forms` and `fm` to INSTALLED_APPS:

```python
INSTALLED_APPS = (
    ...
    'crispy_forms',
    'fm',
)
```

Also in `settings.py` set crispy template pack to `bootstrap3`:

```python
CRISPY_TEMPLATE_PACK = 'bootstrap3'
```

Include modal template into your project template and initialize jQuery plugin:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
        <script type="text/javascript" src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    </head>
    <body>
        {% block content %}{% endblock %}
        {% include "fm/modal.html" %}
        <script type="text/javascript">
            $(function() {
                $.fm({debug: true});
            });
        </script>
    </body>
</html>
```

There are 3 class-based views in django-fm to inherit from when you want AJAX forms:

* AjaxCreateView
* AjaxUpdateView
* AjaxDeleteView

You create urls for them as usual, in templates you just create links to create, update, delete resources with special class (`fm-create`, `fm-update`, `fm-delete`).

Get started
-----------

So let's create a view to create new instance of some model. In `views.py`:

```python
from fm.views import AjaxCreateView
from feedback.forms import FeedbackForm

class FeedbackCreateView(AjaxCreateView):
    form_class = FeedbackForm
```

You are just inherit from `AjaxCreateView` and provide `form_class` argument - you do this every day in Django when inherit from `django.views.generic.CreateView`, right?

Also you should create url for this resource in `urls.py`:

```python
from django.conf.urls import patterns, url
from feedback.views import FeedbackCreateView

urlpatterns = patterns(
    'feedback.views',
    ...
    url(r'^create/$', FeedbackCreateView.as_view(), name="feedback_create"),
    ...
)
```

Again - nothing new here.

The most interesting part in  template - you don't have to define template for your form - just write a link to create new object with special attributes which tell django-fm how to behave.

So in your template write:

```html
<a href="{% url 'feedback_create' %}" class="fm-create" data-fm-head="Create" data-fm-callback="reload">Create new</a>
```

Look at `fm-create` special class - it's necessary. And that's all - now when user clicks on this link - modal AJAX window with form will be shown.

Every link can have some attributes which define modal window behaviour and callback after successfull object creation, update or deletion:

* `data-fm-head` - header of modal
* `data-fm-ok` - OK button label override
* `data-fm-cancel` - Cancel button label override
* `data-fm-callback` - what to do after successfull modal submission - at moment the following values allowed: `reload`, `redirect`, `replace`, `remove`, `prepend`, `append`, `redirect_from_response`
* `data-fm-target` - value of action specific for each action type - for example this must be an URL when `data-fm-callback` is `redirect`

Let's take a closer look at all these available actions:

* when `data-fm-callback` omitted - nothing happens - modal window just closes after successfull submission
* `reload` - page will be reloaded
* `redirect` - page will be redirected to URL from `data-fm-target`
* `replace` - content from element defined via jQuery selector in `data-fm-target` will be replaced with `message` from incoming JSON from server
* `remove` - element defined via jQuery selector in `data-fm-targer` will be removed from DOM
* `prepend` - `message` from JSON coming from server will be prepended to element defined in `data-fm-target`
* `append` - `message` from JSON coming from server will be appended to element defined in `data-fm-target`
* `redirect_from_response` - the current window will be redirected to the `message` from JSON coming from server. Your view must override the `get_response_message` method to return the URL to redirect to. 
* also there is a possibility to set custom callback how to react on successfull submission.

See demo project to see this concept in action.

Custom callbacks
----------------

Since version 0.2.4 it's possible to register custom callback functions to do non-standard or more
complicated logic after success form submission. Here is how you can register new callback (should be used with `data-fm-callback="appendWithAlert"` parameter):

```
$(function() {
    $.fm({
        debug: true,
        custom_callbacks: {
            "appendWithAlert": function(data, options) {
                $(options.modal_target).append(data.message);
                alert("model instance created!");
            }
        }
    });
});
```

Some other things to be aware of
--------------------------------

* note that file upload via AJAX will work in modern browsers only - see [this](http://caniuse.com/#feat=xhr2) table.
* when modal with form ready - an event `fm.ready` will be triggered on `body` element (by default). This can help to add some javascript widgets into form.
* you can extend `AjaxCreateView`, `AjaxUpdateView` and `AjaxDeleteView` using standard Django techniques. For example, you can add permission checking using `PermissionMixin` from [django-braces](https://github.com/brack3t/django-braces) project
