from django.forms import ModelForm
from django import forms
from .models import Thread, Note
from tinymce.widgets import TinyMCE

class Noteform(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    
    class Meta:
        model = Note
        fields = ["content"]
        widgets = {
            "content":TinyMCE()
        }
    

class Threadsetting(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    class Meta:
        model = Thread
        fields = ["title","description","privacy"]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'textarea textarea-primary', 'placeholder': 'Your Description here'}),
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full max-w-xs p-5', 'placeholder': 'Your Thread Title'}),
            'privacy':forms.Select(attrs={'class': 'select select-primary w-full max-w-xs', 'placeholder': 'Your Thread Title'}),
        }
    


class Threadform(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    class Meta:
        model = Thread
        fields = ["title","description"]
        # Override the widget for field1
        # labels = {
        #     'title': 'Tasdasdatle',
        #     #'users': 'Access',
        #  }

        widgets = {
            'description': forms.Textarea(attrs={'class': 'textarea textarea-primary', 'placeholder': 'Your Description here'}),
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full max-w-xs p-5', 'placeholder': 'Your Thread Title'}),
        }

    # def __init__(self, *args, **kwargs):
    #     creator = kwargs.pop('creator', None)
    #     friends = kwargs.pop('friends', [])

    #     super().__init__(*args, **kwargs)

    #     # Filter the users field choices to include only friends
    #     self.fields['users'].queryset = friends

    #     self.creator = creator