from django.db import models


FEDERAL_DISTRICTS = (
    ("Центральный федеральный округ", "Центральный федеральный округ"),
    ("Северо-Западный федеральный округ", "Северо-Западный федеральный округ"),
    ("Южный федеральный округ", "Северо-Западный федеральный округ"),
    ("Северо-Кавказский федеральный округ", "Северо-Западный федеральный округ"),
    ("Приволжский федеральный округ", "Северо-Западный федеральный округ"),
    ("Уральский федеральный округ", "Северо-Западный федеральный округ"),
    ("Сибирский федеральный округ", "Северо-Западный федеральный округ"),
    ("Дальневосточный федеральный округ", "Северо-Западный федеральный округ")
)

class Region(models.Model):
    title = models.CharField(max_length=60, unique=True, blank=True, default='')
    federal_district = models.CharField(max_length=30, choices=FEDERAL_DISTRICTS)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
