from django import forms

class ListingFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Keywords",
        widget=forms.TextInput(attrs={'placeholder': 'Search by title or description'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        label="Min Price",
        widget=forms.NumberInput(attrs={'placeholder': '0'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        label="Max Price",
        widget=forms.NumberInput(attrs={'placeholder': '10000'})
    )
    location = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'City or region'})
    )
    min_rooms = forms.IntegerField(
        required=False,
        min_value=1,
        label="Min Rooms",
        widget=forms.NumberInput(attrs={'placeholder': '1'})
    )
    max_rooms = forms.IntegerField(
        required=False,
        min_value=1,
        label="Max Rooms",
        widget=forms.NumberInput(attrs={'placeholder': '5'})
    )
    type = forms.ChoiceField(
        required=False,
        choices=[
            ('apartment', 'Квартира'),
            ('house', 'Дом'),
            ('duplex', 'Дуплекс'),
            ('studio', 'Студия'),
            ('cottage', 'Коттедж'),
        ],
        label="Type",
        widget=forms.Select()
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('price_asc', 'Price (Low to High)'),
            ('price_desc', 'Price (High to Low)'),
            ('date_new', 'Newest First'),
            ('date_old', 'Oldest First'),
        ],
        label="Sort By",
        widget=forms.Select()
    )
