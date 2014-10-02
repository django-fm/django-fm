[Live example](http://djangofm.herokuapp.com/) - see the source code of demonstration in `demo` repository folder.

Django FM
=========

Requires jQuery and Bootstrap 3 on client side. Depends on Django-crispy-forms.

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

You create urls for them as always, in templates you just create links to create, update, delete resources with special class (`fm-create`, `fm-update`, `fm-delete`).

Every link can have some attributes which define modal window behaviour and callback after successfull object creation, update or deletion.

See demo project to see this concept in action
