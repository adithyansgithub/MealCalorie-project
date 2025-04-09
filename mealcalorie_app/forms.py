from django import forms
from .models import MealEntry, FoodItem
from datetime import datetime

class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ['food_item', 'quantity', 'quantity_type', 'date_time']

        widgets = {
            'food_item': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_type': forms.Select(attrs={'class': 'form-select'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food_item'].queryset = FoodItem.objects.none()

        # Set default value for date_time field
        if not self.initial.get('date_time'):
            self.initial['date_time'] = datetime.now().strftime('%Y-%m-%dT%H:%M')

        # Set default value for quantity_type field
        if not self.initial.get('quantity_type'):
            self.initial['quantity_type'] = 'number'  # Default to "number"

        if 'category' in self.data:
            try:
                category = self.data.get('category')
                self.fields['food_item'].queryset = FoodItem.objects.filter(category=category)
            except (ValueError, TypeError):
                pass  # Invalid input; fallback to empty queryset