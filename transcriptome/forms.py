from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.PasswordInput(max_length=15)


class TranscriptSearchForm(forms.Form):
    transcript_name = forms.CharField(max_length=50, required=False)
    insecticide = forms.ChoiceField(initial={'All': 'all'},
                                    choices=[('All', 'all'),
                                             ('Formothion', 'formothion'),
                                             ('Fenthion', 'fenthion'),
                                             ('Methomyl', 'methomyl')])
    line = forms.ChoiceField(initial={'All', 'all'},
                             choices=[('All', 'all'),
                                      ('Susceptible', 'susceptible'),
                                      ('Resistant', 'resistant'),
                                      ('Recovered', 'recovered')],
                             attrs={'onchange': 'this.form.submit();',
                                    'name': 'line'})
    transcript_seq = forms.CharField(min_length=100, required=False)
    refacc = forms.CharField(max_length=10, required=False)
    refdes = forms.CharField(min_length=100, required=False)
    items_per_page = forms.IntegerField(max_length=4, initial='20')


class ExportTranscriptListForm(forms.Form):
    pass


class ExportTranscriptDetailsForm(forms.Form):
    pass
