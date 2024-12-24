from django.urls import path
from .import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('about',views.about, name = 'about'),
    path('blog',views.blog, name = 'blog'),
    path('contact',views.contact, name = 'contact'),
    path('service',views.service, name = 'service'),
    path('testimonail',views.testimonail, name = 'testimonail'),
    path('login/',views.login, name = 'login'),
    path('signup/',views.signup, name = 'signup'),
    path('login/signup',views.signup, name = 'singup'),
    path('predict',views.predict, name = 'predict'),
    path('data',views.data,name='data'),
    path('logout',views.logout,name='logout'),
]