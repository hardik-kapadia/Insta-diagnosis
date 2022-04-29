from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import ImageForm, RegisterForm
from .models import Scan

from .prediction.ml_models import predict_brain_tumor, predict_covid_noncovid


def signin(request):

    if request.method == "GET":
        return render(request, 'diagnose/login.html')

    username = request.POST['username']
    password = request.POST['password']

    print(f'username: {username}, password: {password}')

    user = authenticate(request, username=username, password=password)

    print(f'user: {user}')

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        context = {'error': 'Invalid credentials'}
        return render(request, 'diagnose/login.html', context=context)


def signup(request):

    context = {}

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name)

            print(f'User created: {user}')

            return redirect('/')

        else:
            context = {'error:': 'Invalid details provided'}

    context['form'] = RegisterForm()

    return render(request, 'diagnose/register.html', context=context)

    pass


def signout(request):
    logout(request)


def home(request):

    context = {}

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            disease = form.cleaned_data.get("disease")
            scan = form.cleaned_data.get("image")

            img = scan.file

            if disease == 'covid':
                predictor = predict_covid_noncovid
            else:
                predictor = predict_brain_tumor

            prediction = predictor(img)

            user_ = None

            if request.user.is_authenticated:
                user_ = request.user

            print('user is: ', user_)

            obj = Scan.objects.create(
                disease=disease,
                scan=scan,
                user=user_,
                result=prediction
            )

            context['result'] = prediction
            context['image_name'] = scan.name

            obj.save()

            print(obj)
    else:
        form = ImageForm()

    context['form'] = form

    return render(request, 'diagnose/home.html', context=context)


@login_required(login_url='/signin/')
def profile(request):

    qs = Scan.objects.filter(user=request.user)

    print(f'qs:{qs}')

    scans_list = None

    if qs:
        scans_list = list(qs)

    print(f'list: {scans_list}')

    context = {}

    context['user'] = request.user
    context['table'] = scans_list

    return render(request, 'diagnose/profile.html', context=context)
