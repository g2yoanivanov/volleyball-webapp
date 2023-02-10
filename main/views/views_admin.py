from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Model
from django.http import HttpResponse
from django.shortcuts import render, redirect

import random

from main.models import *
from main.forms import *


@staff_member_required
def myadmin(request):
    return render(request, "main/admin_templates/myadmin.html")
