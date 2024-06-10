from django.db import models

class UserFinance(models.Model):
    name = models.CharField(max_length=150)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - ({self.birthday})'