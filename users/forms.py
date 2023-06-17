from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserCreationForm(UserCreationForm):

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class': 'input-teacher'
        })
        self.fields["password1"].widget.attrs.update({
            'class': 'input-teacher'
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'input-teacher'
        })
        self.fields["status"].widget.attrs.update({
            'class': 'input-teacher'
        })

    # CHOICES = [('S', 'Студент'), ('T', 'Викладач')]

    # status = forms.ChoiceField(
    #     choices=CHOICES,
    #     widget=forms.RadioSelect,
    #     label=_('Вкажіть ваш статус:'),
    #     required=True
    #     )
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2", "status")
