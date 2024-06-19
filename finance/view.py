# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import FinanceView
from userFinance.models import UserFinance

def finance_data(request):
    user_id = request.GET.get('user', None)
    if user_id:
        finances = FinanceView.objects.filter(user_id=user_id)
    else:
        finances = FinanceView.objects.all()

    users = UserFinance.objects.all()
    labels = [user.name for user in users]

    datasets = []
    for finance in finances:
        user_data = {
            'label': finance.valueInsert,  # Pode ajustar para outro campo relevante, como 'description'
            'data': [float(finance.money) if finance.user_id == user.id else 0 for user in users],
            'backgroundColor': 'rgba(54, 162, 235, 0.6)'  # Pode personalizar as cores conforme necessário
        }
        datasets.append(user_data)

    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets
    })

def finance_chart(request):
    users = UserFinance.objects.all()
    return render(request, 'finance_chart.html', {'users': users})
