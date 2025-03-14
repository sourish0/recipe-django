"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import recipe_list,recipe_delete,recipe_update,login_page,signin_page,logout_page


urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('delete_recipe/<int:pk>/', recipe_delete, name='delete_recipe'),
    path('update_recipe/<int:pk>/', recipe_update, name='recipe_update'),
    path('login/', login_page, name='login'),
    path('signin/', signin_page, name='signin'),
    path('logout/', logout_page, name='logout'),
]
