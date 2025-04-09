from django.shortcuts import render, redirect
from .forms import MealEntryForm
from .models import FoodItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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