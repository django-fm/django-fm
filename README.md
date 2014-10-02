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
