from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)


class TranscriptSearchForm(forms.Form):
    seqname = forms.CharField(max_length=50, required=False)
    line = forms.ChoiceField(initial='',
                             choices=[('', 'All'),
                                      ('ss_old', 'SS/Hsu1'),
                                      ('ss_new', 'SS/Hsu2'),
                                      ('ss_chi', 'SS/China'),
                                      ('rs_for', 'RS/Formothion'),
                                      ('rs_fen', 'RS/Fenthion'),
                                      ('rs_met', 'RS/Methomyl'),
                                      # ('rs_mal', 'RS/Malathion'),
                                      # ('rs_nal', 'RS/Naled'),
                                      # ('rs_tri', 'RS/Trichlorfon'),
                                      ('rc_for', 'RC/Formothion'),
                                      ('rc_fen', 'RC/Fenthion'),
                                      ('rc_met', 'RC/Methomyl')],
                             required=False)
    seq = forms.CharField(required=False)
    refacc = forms.CharField(max_length=15, required=False)
    refdes = forms.CharField(required=False)
    items_per_page = forms.ChoiceField(initial=20,
                                       choices=[(20, '20'),
                                                (50, '50'),
                                                (100, '100'),
                                                (200, '200')],
                                       required=False)


class ArchiveSearchForm(forms.Form):
    line = forms.ChoiceField(initial='ss_old',
                             choices=[('ss_old', 'SS/Hsu1'),
                                      ('ss_new', 'SS/Hsu2'),
                                      ('ss_chi', 'SS/China'),
                                      ('rs_for', 'RS/Formothion'),
                                      ('rs_fen', 'RS/Fenthion'),
                                      ('rs_met', 'RS/Methomyl'),
                                      # ('rs_mal', 'RS/Malathion'),
                                      # ('rs_nal', 'RS/Naled'),
                                      # ('rs_tri', 'RS/Trichlorfon'),
                                      ('rc_for', 'RC/Formothion'),
                                      ('rc_fen', 'RC/Fenthion'),
                                      ('rc_met', 'RC/Methomyl')],
                             required=False)
    refacc = forms.CharField(max_length=15, required=False)


class ExportTranscriptListForm(forms.Form):
    pass


class ExportTranscriptDetailsForm(forms.Form):
    pass
