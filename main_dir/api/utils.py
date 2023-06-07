import random


def random_location():
    from .models import Location
    queryset = Location.objects.all()
    if queryset:
        return random.choice(queryset)
    return None
