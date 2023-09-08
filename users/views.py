from django.shortcuts import render
from users import models


# Create your views here.
def test(request):
    return render(request, "test.html")


def group_list(request):
    groups = models.Group.objects.all()
    return render(request, "group_list.html", {"groups": groups})
