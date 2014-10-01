from setuptools import setup
import os

import fm


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name="django-fm",
    version=fm.__version__,
    description="Twitter Bootstrap 3 based modal AJAX form for Django",
    long_description="Twitter Bootstrap 3 based modal AJAX form for Django",
    keywords="django, views, forms, ajax, bootstrap, modal, create, update, delete",
    author="Alexandr Emelin <frvzmb@gmail.com>",
    author_email="frvzmb@gmail.com",
    url="https://github.com/FZambia/django-fm/",
    license=fm.__license__,
    packages=get_packages('fm'),
    package_data=get_package_data('fm'),
    zip_safe=False,
    install_requires=["django-crispy-forms>=1.4.0"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
)
