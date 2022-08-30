from django import forms
from .models import Topic,Post
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    
    class Meta:
        model = Topic
        
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class InputRecordsForm(forms.Form):
    
    records = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        required=True,
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    CHOICES= (
('A', 'A'),
('TXT', 'TXT'), 
('CNAME', 'CNAME'),
('MX', 'MX'),
)
    type_record = forms.CharField(widget=forms.Select(choices=CHOICES))
    TTL = forms.IntegerField(initial=3600)
    def clean_records(self):
        print("<egegzezegzegzegzeg")
        data = self.cleaned_data.get("records")
        print(data)
        print(data)
        #data = self.cleaned_data.get("emails")


        for line in data.splitlines():
            spli = line.split('|')
            if len(spli) == 2:
                
                x = re.search("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", spli[0])
                if x:
                    pass
                else:
                    raise forms.ValidationError("Invalide domain: {0}".format(spli[0]))

            else:
                raise forms.ValidationError("Invalide format: {0}".format(line))
            
            
        return data




class Input_pmtaconfig_Form(forms.Form):
    
    config_p = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        
        required=False,
        max_length=40000,
        
        label=('Pmta Config :  ')
    )
    CHOICES= (
    ('', '-----------'),
    ('185.225.19.162', 'serv75583'),
    ('74.82.4.225', 'serv71866'), 

    )
    CHOICES2= (
    ('', '-----------'),
    ('1', 'gmail'),
    ('2', 'hotmail'), 

    )
    server = forms.CharField(widget=forms.Select(choices=CHOICES))
    isp = forms.CharField(widget=forms.Select(choices=CHOICES2))

   