# Django Open Badge Integration

You'll need to modify your settings file and include something resembling the following:

    MOZBADGES = {
        'hub': 'http://badgehub.com',
        'badge_getter': 'users.badges.get_awarded_badges',
    }

Be sure to run the test suite afterwards and make sure everything is kosher.
