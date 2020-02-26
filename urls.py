from django.urls import path
from first import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
      url('about',views.about),
      url('details',views.details),
      url('openmic',views.openmic),
      url('playsnd',views.playsnd),
      url('getwords',views.getwords),
    url('',views.HomePageView.as_view()), 
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)