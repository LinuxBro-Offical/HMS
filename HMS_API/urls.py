"""
URL configuration for HMS Backend API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tenants/', include('tenants.urls')),
    path('api/users/', include('users.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/encounters/', include('encounters.urls')),
    path('api/billing/', include('billing.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/clinical-decision-support/', include('clinical_decision_support.urls')),
    path('api/laboratory/', include('laboratory.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/telemedicine/', include('telemedicine.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/patient-portal/', include('patient_portal.urls')),
    path('api/compliance/', include('compliance.urls')),
    path('api/integrations/', include('integrations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
