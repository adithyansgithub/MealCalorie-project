from django.shortcuts import render, redirect
from .forms import MealEntryForm
from .models import FoodItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mealcalorie_app.models import MealEntry
from .forms import FoodItemForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def add_meal(request):
    category = request.GET.get('category', None)

    if request.method == 'POST':
        form = MealEntryForm(request.POST)
        if 'category' in request.POST:
            category = request.POST.get('category')
        if category:
            queryset = FoodItem.objects.filter(category=category)
            form.fields['food_item'].queryset = queryset

        if form.is_valid():
            meal_entry = form.save(commit=False)
            meal_entry.user = request.user
            meal_entry.save()
            messages.success(request, "Meal added successfully!")  # Add success message
            return redirect('add_meal')  # Redirect back to the same page to clear the form
        else:
            messages.error(request, "There was an error adding the meal. Please try again.")  # Add error message
    else:
        form = MealEntryForm()
        if category:
            queryset = FoodItem.objects.filter(category=category)
            form.fields['food_item'].queryset = queryset

    categories = FoodItem.CATEGORY_CHOICES
    return render(request, 'mealcalorie_app/add_meal.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def records(request):
    # Fetch all meal records for the logged-in user, grouped by date
    records = MealEntry.objects.filter(user=request.user).order_by('-date_time')

    # Group records by date
    grouped_records = {}
    for record in records:
        record_date = record.date_time.date()
        if record_date not in grouped_records:
            grouped_records[record_date] = []
        grouped_records[record_date].append(record)

    return render(request, 'mealcalorie_app/records.html', {  # Updated path
        'grouped_records': grouped_records,
    })

@login_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully!")  # Add success message
            return redirect('add_food_item')  # Redirect to the same page after saving
    else:
        form = FoodItemForm()

    return render(request, 'mealcalorie_app/add_food_item.html', {'form': form})

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(MealEntry, id=record_id, user=request.user)
    record.delete()
    messages.success(request, "The record has been successfully deleted!")  # Add success message
    return redirect('records')  
