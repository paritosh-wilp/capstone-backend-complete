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
from sessioncrud.views import SessionListCreateView, SessionDetailView
from sessioncrud.views import SessionByBusinessView
from sessioncrud.views import UpdateSessionByBusinessView
from sessioncrud.views import UpdateSessionByCustomerView
from sessioncrud.views import SessionByCustomerView
from sessioncrud.views import SessionByBusinessMailView
from sessioncrud.views import SessionByCustomerMailView


urlpatterns = [
    path('business/signup/', BusinessSignupView.as_view(), name='business-signup'),
    path('business/login/', BusinessLoginView.as_view(), name='business-login'),
    path('customer/signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),
    path('sessions/business/list/<int:business_id>/', SessionByBusinessView.as_view(), name='list-session-by-business'),
    path('sessions/business/<int:business_id>/', UpdateSessionByBusinessView.as_view(), name='update-sessions-by-business'),
    path('sessions/business/<int:business_id>/<int:session_id>/', UpdateSessionByBusinessView.as_view(), name='update-session-by-business'),
    path('sessions/customer/list/<int:customer_id>/', SessionByCustomerView.as_view(), name='list-session-by-customer'),
    path('sessions/customer/<int:customer_id>/<int:session_id>/', UpdateSessionByCustomerView.as_view(), name='update-session-by-customer'), 
    path('sessions/business-mail/<str:business_mail>/', SessionByBusinessMailView.as_view(), name='session-by-business-mail'),
    path('sessions/customer-mail/<str:customer_mail>/', SessionByCustomerMailView.as_view(), name='session-by-customer-mail'),
]

