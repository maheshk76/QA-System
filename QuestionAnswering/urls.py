from django.urls import path
from QuestionAnswering import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
      url('about',views.about),
      url('documentation',views.documentation),
      url('details',views.details),
      url('openmic',views.openmic),
      url('playsnd',views.playsnd),
      url('getwords',views.getwords),
      url('contact',views.contact),
      url('saveans',views.saveans),
      url('askquestion',views.askquestion),
    url('',views.HomePageView.as_view()), 
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)