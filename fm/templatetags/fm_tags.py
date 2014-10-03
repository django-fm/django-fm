from django import template
import fm


register = template.Library()


def fm_version():
    return fm.__version__


register.simple_tag(fm_version)