from django import forms

class CreatePollForm(forms.Form):
    question_text = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ask a question...',
            'class': 'form-input',
            'id': 'question-input',
        })
    )