from django.urls import path, include

urlpatterns = [
    path('', include('banque.urls')),
    path('banque/', include('banque.urls'))
]
