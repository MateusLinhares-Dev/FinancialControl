from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from finance.view import finance_data, finance_chart
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/', include('finance.urls')),
    path('api/v1/', include('userFinance.urls')),

    path('finance/data/', finance_data, name='finance_data'),
    path('finance/chart/', finance_chart, name='finance_chart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
