from django import forms

from .models import Shift, Expenses


class LeadMarketer_SignUpForm(forms.ModelForm):

    class Meta:
        model = Shift
        fields = ['lead_marketer']
        widgets = {'lead_marketer': forms.HiddenInput()}

    # Check to see if the lead marketer is already filled
    def clean_lead_marketer(self):
        lead_marketer = self.cleaned_data.get("lead_marketer")
        if lead_marketer != None:
            raise forms.ValidationError("There already is a lead marketer for this shift")


class Marketer_SignUpForm(forms.ModelForm):

    class Meta:
        model = Shift
        fields = ['marketers']
        widgets = {'marketers': forms.CheckboxSelectMultiple()} #forms.HiddenInput()}

    def clean_marketers(self):
        return [self.cleaned_data['marketers']]

    # Check to see if the lead marketer is already filled
    # def clean_lead_marketer(self):
    #
    #     lead_marketer = self.cleaned_data.get("lead_marketer")
    #     if lead_marketer != None:
    #         raise forms.ValidationError("There already is a lead marketer for this shift")


class Expense_report(forms.ModelForm):

    class Meta:
        model = Expenses
        fields = [
            'user',
            'amount',
            'receipt',
            'date',
            'description'
        ]
        widgets = {
            'lead_marketer': forms.HiddenInput(),
        }

    # Check to see if the lead marketer is already filled

