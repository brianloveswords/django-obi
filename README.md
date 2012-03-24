# Django Open Badge Integration

## Installation

```pip install -e git://github.com/brianlovesdata/django-obi.git#egg=django_obi```

## Configuration
Step 0: Include `django_obi` in your setting file's `INSTALLED_APPS`.

While you're mucking around in there, include an additional setting, something
resembling the following:

```python    
MOZBADGES = {
    'hub': 'http://beta.openbadges.org',
    'badge_getter': 'users.badges.get_awarded_badges',
}
```

Configure urls.py:

```urlpatterns = patterns('',
    (r'^obi/', include('django_obi.urls')),
    ...
)
```

Be sure to run the test suite afterwards and make sure everything is kosher.

## Badge Getter

### Input
The badge getter is going to get called a little something like this:

```python
def some_view(request):
    user = request.user
    if user.is_authenticated():
        badges = badge_getter(user)
```

Your badge_getter method should take a User object and know how to get awarded
badges from it.

### Output

The badge processer expects badge_getter to output a dictionary looking something like this:

```python
{
    'proud_js_expert' : {
        'name' : 'JavaScript Expert',
        'evidence': 'http://example.com/badge-evidence/user-1/js-expert',
        'image': 'http://example.com/badge-images/js-expert.png',
        'description': 'Awarded for being totally rad at JavaScript',
        'criteria': 'http://example.com/badge-requirements/js-expert',
    },
    'ashamed_cobol_master': { ... },
    'reluctant_java_user': { ... },
}
```
You are welcome to include other information in the dictionary; at the moment
it will be ignored. In future versions it will likely be included as extra
metadata passed to the hub.

## Usage

> **Important Note!**

> The authenticated user must have an email address associated with their
  account (that is, stored in the auth_user table and accessible by
  django.contrib.auth.models.User).

> Django's site framework must be enabled, and Site.objects.get_current()
  must provide the issuers name and domain.

In your templates, you need to load `django_obi_tags`:

```
...
{% load django_obi_tags %}
...
```

Then use the `send_badges_action` inclusion-tag to add a 'Send' button
and the neccesary javascript to interact with the Issuer API:

```
...
{% send_badges_action %}
...
```

## Related Projects

* Mozilla Open Badges project -- https://github.com/mozilla/openbadges


