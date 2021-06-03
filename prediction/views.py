from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request,'prediction/main.html')

def Result(request):
    return render(request,'prediction/Result.html')

def Detection(request):
    return render(request,'prediction/Detection.html')