from django import forms
from .models import Resturant, States
from django.forms import ModelForm

REGIONS = {
    "new england": "New England", 
    "mid-atlantic": "Mid-Atlantic", 
    "midwest": "Midwest",
    "south atlantic": "South Atlantic", 
    "south central": "South Central", 
    "mountain": "Mountain",
    "pacific": "Pacific"
}
TYPE = {
    "landmark": "Landmark",
    "resturant": "Resturant",
    "activity": "Activity"
}
TYPE_LANDMARK = {
    "C": "Cultural",
    "H": "Historical",
    "N": "Natural"
}
TYPE_ACTIVITY = {
    "O": "Outdoor",
    "I": "Indoor",
    "B": "Both"
}
PRICE_POINT = {
    "$": "$0-10 /person",
    "$$": "$11-20 /person",
    "$$$": "$21-100 /person",
    "$$$$": "$+101 /person",
}
cusines = Resturant.objects.values_list('cusine').order_by("cusine")
CUSINE = {
    "all": "All"
}
for i in cusines:
    string = i
    CUSINE.update({i[0] : i[0]})

states = States.objects.values_list('name').order_by("name")
STATE_LIST = {
    "all": "All"
}
STATE_LIST_LIMITED = {
    "": ""
}
for i in states:
    string = i
    STATE_LIST.update({i[0] : i[0]})
    STATE_LIST_LIMITED.update({i[0] : i[0]})

class StateForm(forms.Form):
    # state_name = forms.CharField(label="state_name", max_length=100)
    region = forms.MultipleChoiceField(
        label="Regions",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=REGIONS
    ) 
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices= TYPE
    ) 
    states = forms.MultipleChoiceField(
        label="States",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=STATE_LIST
    ) 

class LandmarkSort(forms.Form):
    landmark_type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices= TYPE_LANDMARK
    )
    start_time = forms.TimeField(required=False, label="Start Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, label="End Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))

class ResturantSort(forms.Form):
    price_range = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices= PRICE_POINT
    )
    rating = forms.DecimalField(required=False, max_value = 5, min_value = 0, step_size = 0.1, max_digits=2, initial=0)
    start_time = forms.TimeField(required=False, label="Start Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, label="End Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    cusine = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices = CUSINE
    )

class ActivitySort(forms.Form):
    activity_type = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices = TYPE_ACTIVITY
    )
    keyword = forms.CharField(required=False, label="Keyword", max_length=20)

class LandmarkEdit(forms.Form):
    name = forms.CharField(required=False, label="Name", max_length=40)
    state = forms.ChoiceField(
        label="States",
        required=True,
        widget=forms.Select,
        choices=STATE_LIST_LIMITED
    ) 
    city = forms.CharField(required=False, label="City", max_length=40)
    landmark_type = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices= TYPE_LANDMARK
    )
    price = forms.DecimalField(required=False)
    start_time = forms.TimeField(required=False, label="Start Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, label="End Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))

class ResturantEdit(forms.Form):
    name = forms.CharField(required=False, label="Name", max_length=40)
    state = forms.ChoiceField(
        label="States",
        required=True,
        widget=forms.Select,
        choices=STATE_LIST_LIMITED
    ) 
    city = forms.CharField(required=False, label="City", max_length=40)
    type = forms.CharField(required=False, label="Cusine", max_length=40)
    price_range = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices= PRICE_POINT
    )
    rating = forms.DecimalField(required=False, max_value = 5, min_value = 0, step_size = 0.1, max_digits=2, initial=0)
    start_time = forms.TimeField(required=False, label="Opening Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, label="Closing Time", input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))


class ActivityEdit(forms.Form):
    state = forms.ChoiceField(
        label="States",
        required=True,
        widget=forms.Select,
        choices=STATE_LIST_LIMITED
    ) 
    city = forms.CharField(required=False, label="City", max_length=40)
    name = forms.CharField(required=False, label="Name", max_length=40)
    description = forms.CharField(required=False, label="Description", max_length=200)
    type = forms.ChoiceField(
        label="Type",
        required=True,
        widget=forms.RadioSelect,
        choices= {
            "O": "outdoor",
            "I": "indoor",
        }
    ) 