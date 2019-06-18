from django import forms


class Search(forms.Form):
    id_search = forms.IntegerField(min_value=3000, max_value=3078, label='')