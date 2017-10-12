# Wagtail StreamForms

[![CircleCI](https://circleci.com/gh/AccentDesign/wagtail_streamforms/tree/master.svg?style=svg)](https://circleci.com/gh/AccentDesign/wagtail_streamforms/tree/master)
[![Coverage Status](https://coveralls.io/repos/github/AccentDesign/wagtail_streamforms/badge.svg?branch=master)](https://coveralls.io/github/AccentDesign/wagtail_streamforms?branch=master)

This package is currently a concept but allows you to add add forms that are built in the cms admin area to
any streamfield. You can also create your own form templates which will then appear as a template choice when you build
your form. This allows you to decide how the form is submitted and to where.

Documentation is currently being worked on but the basics are below


## Whats included?

- Forms can be built in the cms admin and used site wide in any streamfield.
- You can create your own form templates to display/submit how ever you wish to do it.
- We have included a mixin which will handle the form post if it is being submitted to a wagtail page.
- Forms are catagorised by their class in the cms admin for easier navigation.
- Form submissions are also listed by their form which you can filter by date and are ordered by newest first.
- Recaptcha can be added to a form.
- You can also add site wide regex validators fo use in regex fields.


## Screen shots

![Screen1](/images/screen1.png)

![Screen2](/images/screen2.png)

![Screen3](/images/screen3.png)

![Screen4](/images/screen4.png)

![Screen5](/images/screen5.png)


## General setup

Add wagtail_streamforms to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    'wagtail_streamforms'
    ...
]
```

Next define the form templates in your settings.py:

```
# this is the defaults 
WAGTAIL_STREAMFORMS_FORM_TEMPLATES = (
    ('streamforms/form_block.html', 'Default Form Template'),
)
```

and if you want to the admin base area label:

```
# this is the default
WAGTAIL_STREAMFORMS_ADMIN_MENU_LABEL = 'Streamforms'
```


## Optionally enable recaptcha

Has been enabled via the [django-recaptcha](https://github.com/praekelt/django-recaptcha) package. 
Please note that only one recapcha should be used per page, this is a known issue and we are looking to fix it.

Just add captcha to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    'captcha'
    ...
]
```

Add the required keys in your settings.py which you can get from google's recapcha service:

```
RECAPTCHA_PUBLIC_KEY = 'xxx'
RECAPTCHA_PRIVATE_KEY = 'xxx'
 
# To use the new No Captcha reCaptcha
NOCAPTCHA = True
```


## Defining your own form functionality

Currently we have defined two different types of forms one which just enables saving the submission and one to 
addionally email the results of the submission, As shown [here](https://github.com/AccentDesign/wagtail_streamforms/blob/master/wagtail_streamforms/models/form.py#L112).

You can easily add your own all you have to do is create a model that inherits from our form base class add any addional
fields/properties and this will be added to the cms admin area.

Example:

```
from wagtail_streamforms.models import BaseForm

class SomeForm(BaseForm):

    def process_form_submission(self, form):
        super(SomeForm, self).process_form_submission(form) # handles the submission saving
        # do your own stuff here

```


## Choosing a form in a streamfield

The below is an example of a page model with the form block in a stream field. It inherits from our form submission
mixin fo that the forms can be posted to the page they appear on.

```
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail_streamforms.blocks import WagtailFormBlock
from wagtail_streamforms.models import StreamFormPageMixin


class BasicPage(StreamFormPageMixin, Page):

    body = StreamField([
        ('form', WagtailFormBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```


## Example site with docker

Run the docker container

```bash
$ docker-compose up
```

Create yourself a superuser

```bash
$ docker exec -it <container_name> bash
$ python manage.py createsuperuser
```

Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)


## Testing

Install dependencies

You will need pyenv installed see [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

Also tox needs to be installed

```bash
$ pip install tox
```

Install python versions in pyenv

```bash
$ pyenv install 3.4.4
$ pyenv install 3.5.3
$ pyenv install 3.6.2
```

Set local project versions

```bash
$ pyenv local 3.4.4 3.5.3 3.6.2
```

Run the tests

```bash
$ tox
```

or run for a single environment

```bash
$ tox -e py36-dj111-wt112
```
