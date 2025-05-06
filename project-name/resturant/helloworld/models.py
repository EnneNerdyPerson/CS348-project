from django.db import models

# Create your models here.
class States(models.Model):
    name = models.CharField(max_length=30, primary_key=True, default="None")
    REGIONS = {
        "new england": "New England", 
        "mid-atlantic": "Mid-Atlantic", 
        "midwest": "Midwest",
        "south atlantic": "South Atlantic", 
        "south central": "South Central", 
        "mountain": "Mountain",
        "pacific": "Pacific"
    }
    region = models.CharField(max_length=15, choices=REGIONS, default="midwest")

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=["region", ], name="region_idx"),
        ]

class City(models.Model):
    id = models.BigIntegerField(primary_key=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["state"], name="city_state_idx"),
        ]

class Landmark(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key= True, default="None")
    TYPES = {
        "C": "Cultural",
        "H": "Historical",
        "N": "Natural",
    }
    type = models.CharField(max_length=1, choices=TYPES, default="O")
    price = models.DecimalField(decimal_places=2, max_digits=6)
    opening_time = models.DecimalField(decimal_places=2, max_digits=4)
    closing_time = models.DecimalField(decimal_places=2, max_digits=4)

    class Meta:
        indexes = [
            models.Index(fields=["opening_time"], name="start_time_land"),
            models.Index(fields=["closing_time"], name="end_time_land"),
            models.Index(fields=["type"], name="type_land"),
        ]


class Resturant(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key= True)
    cusine = models.CharField(max_length=30)
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    price_point = {
        "$": "cheap", #<= 10 per person
        "$$": "reasonable", #<= 20 per person
        "$$$": "expensive", #<= 100 per person
        "$$$$": "very expensive", #> 100 per person
    }
    price = models.CharField(max_length=5, choices=price_point, default="-")
    opening_time = models.DecimalField(decimal_places=2, max_digits=4)
    closing_time = models.DecimalField(decimal_places=2, max_digits=4)

    class Meta:
        indexes = [
            models.Index(fields=["opening_time"], name="start_time_rest"),
            models.Index(fields=["closing_time"], name="end_time_rest"),
            models.Index(fields=["price"], name="price_rest"),
            models.Index(fields=["rating"], name="rate_rest"),
        ]


class Activity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, primary_key= True)
    description = models.CharField(max_length=200, default="")
    TYPE_OPTION = {
        "O": "outdoor",
        "I": "indoor",
    }
    type = models.CharField(max_length=1, choices=TYPE_OPTION, default="O")

