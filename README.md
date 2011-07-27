# Django Open Badge Integration

## Overview

You'll need to modify your settings file and include something resembling the
following:

    MOZBADGES = {
        'hub': 'http://badgehub.com',
        'badge_getter': 'users.badges.get_awarded_badges',
    }

Be sure to run the test suite afterwards and make sure everything is kosher.

## Badge Getter

### Input
The badge getter is going to get called a little something like this:

    def some_view(request):
        user = request.user
        if user.is_authenticated():
            badges = badge_getter(request.user)

Your badge_getter method should take a User object and know how to get awarded
badges from it.

### Output

**This is absolutely going to change. It is currently tailored specifically to
  the p2pu badge pilot data**

The badge processer expects badge_getter to output a dictionary looking something like this:
    {
          'proud_js_expert' : {
              'name' : 'JavaScript Expert',
              'url': 'http://example.com/badge-evidence/user-1/js-expert',
              'image_url': 'http://example.com/badge-images/js-expert.png',
              'description': 'Awarded for being totally rad at JavaScript',
              'template': 'http://example.com/badge-requirements/js-expert', }
          'ashamed_cobol_master': { ... },
          'reluctant_java_user': { ... },
     }

You are welcome to include other information in the dictionary; at the moment
it will be ignored. In future versions it will likely be included as extra
metadata passed to the hub.
