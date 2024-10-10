"""
URL configuration for bookAslotbakend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from sessioncrud.views import BusinessSignupView
from sessioncrud.views import BusinessLoginView
from sessioncrud.views import CustomerSignupView, CustomerLoginView
from sessioncrud.views import SessionListView, CreateSessionView
from sessioncrud.views import UpdateSessionWithCustomerView, UpdateSessionByBusinessView


urlpatterns = [
    path('business/signup/', BusinessSignupView.as_view(), name='business-signup'),
    path('business/login/', BusinessLoginView.as_view(), name='business-login'),
    path('customer/signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('sessions/', SessionListView.as_view(), name='session_list'),
    path('sessions/create/', CreateSessionView.as_view(), name='create_session'),
    path('sessions/update/with-customer/<int:session_uid>/', 
         UpdateSessionWithCustomerView.as_view(), 
         name='update-session-with-customer'),
    path('sessions/update/by-business/<int:session_uid>/', 
         UpdateSessionByBusinessView.as_view(), 
         name='update-session-by-business'),
]

