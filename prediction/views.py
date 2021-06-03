from django.shortcuts import render
import pickle
# Create your views here.
def main(request):
    return render(request,'prediction/main.html')

def Predict(request):
    return render(request,'prediction/Predict.html')

def Detection(request):
    return render(request,'prediction/Detection.html')

def PredictionResult(request):
    pkl_path = "Drug.pkl"
    with open(pkl_path, 'rb') as f:
        model = pickle.load(f)
    Sex = { 'F' : 0 , 'M' :1 }
    BP = { 'HIGH' : 0 , 'LOW' : 1 ,'NORMAL' : 2 }
    Cholestrol = { 'HIGH' : 0 , 'LOW' : 1 ,'NORMAL' : 2 }
    Drug = {0 :'DrugY', 2 : 'drugX', 3 : 'drugA', 1 : 'drugC', 4 : 'drugB'}
    l=[]
    l.append(request.GET['Age'])
    l.append(Sex[request.GET['Sex']])
    l.append(BP[request.GET['BP']])
    l.append(Cholestrol[request.GET.get('Cholestrol', '')])
    l.append(float(request.GET['Na_to_k']))
    
    res=model.predict([l])[0]
    

    return render(request,'prediction/PredictionResult.html',{'res':Drug[res]})

    