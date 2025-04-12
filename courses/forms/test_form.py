from django import forms
from courses.models import PlacementQuestion, PlacementAnswer


class PlacementTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [(a.id, a.text) for a in PlacementAnswer.objects.filter(question=question)]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text, choices=choices, widget=forms.RadioSelect
            )
