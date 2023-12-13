from django import forms
from courses.models import Profile

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
