from django.db import models
from userFinance.models import UserFinance

class FinanceView(models.Model):
    valueInsert = models.CharField(default="Valor depositado", max_length=200)
    user = models.ForeignKey(
        UserFinance, 
        on_delete=models.PROTECT, 
        related_name='userFinanceList')
    
    money = models.DecimalField(decimal_places=2, max_digits=1000)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.valueInsert
    
    
