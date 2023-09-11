"""UserManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from users import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("test/", views.test),
    path("group/list/", views.group_list),
    path("group/add/", views.group_add),
    path("group/edit/<int:group_id>", views.group_edit),
    path("group/delete/<int:group_id>/", views.group_delete),
    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/edit/<int:user_id>/", views.user_edit),
    path("user/delete/<int:user_id>/", views.user_delete),
]
