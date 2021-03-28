from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from App_Login.forms import SignUpForm, CreateStudentForm, FacultyForm


# Create your views here.
def signup_system(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            passwd = form.cleaned_data.get('password1')
            this_user = authenticate(username=username, password=passwd)
            if this_user is not None:
                login(request, this_user)
                return HttpResponseRedirect(reverse('App_Login:faculty-signup'))
    return render(request, 'App_Login/signup.html', context={'form': form})


@login_required
def faculty_signup(request):
    form = FacultyForm()
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            faculty_form = form.save(commit=False)
            faculty_form.user = request.user
            faculty_form.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/facultyForm.html', context={'form': form})


def login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse('App_Attendance:Home'))
    return render(request, 'App_Login/login-form.html', context={'form': form})


def logout_system(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))
