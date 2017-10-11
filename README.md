# wagtail_streamforms

[![CircleCI](https://circleci.com/gh/AccentDesign/wagtail_streamforms/tree/master.svg?style=svg)](https://circleci.com/gh/AccentDesign/wagtail_streamforms/tree/master)
[![Coverage Status](https://coveralls.io/repos/github/AccentDesign/wagtail_streamforms/badge.svg?branch=master)](https://coveralls.io/github/AccentDesign/wagtail_streamforms?branch=master)

## General Setup

1. Add wagtail_streamforms to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    'wagtail_streamforms'
    ...
]
```

2. Define the form templates in your settings.py:

```python
# defaults 
WAGTAIL_STREAMFORMS_FORM_TEMPLATES = (
    ('streamforms/form_block.html', 'Default Form Template'),
)
```

3. Include in your base template the javascript to handle the post and response

```html
<script src="//code.jquery.com/jquery-2.2.4.min.js"></script>
<script src="{% static 'streamforms/js/form-handler.js' %}"></script>
```

## Enable Recaptcha

Has been enabled via the [django-recaptcha](https://github.com/praekelt/django-recaptcha) package. Please note that only one recapcha should be used per page.

Just add captcha to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...
    'captcha'
    ...
]
```

and add the required keys in your settings.py which you can get from google's recapcha service:

```
RECAPTCHA_PUBLIC_KEY = 'xxx'
RECAPTCHA_PRIVATE_KEY = 'xxx'
 
# To use the new No Captcha reCaptcha
NOCAPTCHA = True
```

## Styling Form Errors

Below is an example of the css you will need to highlight the form errors:

```scss
// errors
.has-error input,
.has-error select,
.has-error textarea { border-color: red; }
 
.has-error label,
.has-error .error-msg { color: red; }
 
// recaptcha
.g-recaptcha { margin-bottom: 20px; }
```

## Example Site

1. Run the docker container

```bash
$ docker-compose up
```

2. Create yourself a superuser
```bash
$ docker exec -it <container_name> bash
$ python manage.py createsuperuser
```

3. Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Useful commands

Clean cache:

```
find . -name \*.pyc -delete
find . -name \*__pycache__ -delete
```
