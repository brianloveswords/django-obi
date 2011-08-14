from django import forms


class SendBadgesForm(forms.Form):

    def __init__(self, badges, *args, **kwargs):
        super(SendBadgesForm, self).__init__(*args, **kwargs)
        self.badges = badges
        choices = [(badge_id, badges[badge_id]['name']) for badge_id in badges]
        self.fields['badges'] = forms.TypedMultipleChoiceField(
            choices=choices, empty_value={}, coerce=self.badge_data)

    def badge_data(self, badge_id):
        return (badge_id, self.badges[badge_id])
