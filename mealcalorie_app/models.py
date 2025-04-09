from django.db import models
from django.contrib.auth.models import User

# Model to store food items and their calorie values
class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    calories_per_unit = models.FloatField(help_text="Calories per gram or per unit")

    def __str__(self):
        return f"{self.name} ({self.calories_per_unit} cal)"

# Model to store user meal entries
class MealEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity in grams or number")
    quantity_type = models.CharField(max_length=10, choices=[('grams', 'Grams'), ('number', 'Number')])
    date_time = models.DateTimeField()
    total_calories = models.FloatField(editable=False, help_text="Total calories for this meal entry")

    def save(self, *args, **kwargs):
        # Calculate total calories before saving
        self.total_calories = self.food_item.calories_per_unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} ({self.quantity} {self.quantity_type})"