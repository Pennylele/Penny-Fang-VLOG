from django import forms


class SyncForm(forms.Form):
	r = forms.CharField(label="Sync")