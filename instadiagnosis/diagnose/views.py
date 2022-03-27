from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from .prediction.ml_models import predict_brain_tumor, predict_covid_noncovid

from .forms import ImageForm
from .models import Scan


def login(request):
    return render(request, 'diagnose/login.html')


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
