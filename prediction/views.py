from django.shortcuts import render
import pickle
import requests
from datetime import date
import pandas as pd

# Create your views here.
def main(request):
    data = requests.get("https://covid19.mathdro.id/api/")
    result1 = requests.get("https://coronavirus-19-api.herokuapp.com/countries").json()
    d = dict()
    for i in result1:
        d[i['country']]=i['todayCases']
    world = dict(sorted(d.items(), key=lambda item: item[1],reverse=True)[1:51])

    country = []
    cases = []
    deaths = []
    recovered =[]
    todayDeaths = []

    for i in result1:
        if i['country'] in world.keys():
            country.append(i['country'])
            cases.append(i['cases'])
            deaths.append(i['deaths'])
            recovered.append(i['recovered'])
            todayDeaths.append(i['todayDeaths'])
    z = zip(country,cases,deaths,recovered,todayDeaths)
    result = data.json()
    confirmed = result['confirmed']['value']
    
    recovered = result['recovered']['value']
    deaths = result['deaths']['value']
    return render(request,'prediction/main.html',{'confirmed' : confirmed, 'deaths' : deaths  ,'recovered' :recovered , 'world' : z})

def Predict(request):
    return render(request,'prediction/Predict.html')

def News(request):
    today = date.today()
    d3 = today.strftime("%y-%m-%d")
    data = requests.get("https://newsapi.org/v2/everything?q=covid-cases&from={}&pageSize=100&sortBy=publishedAt&apiKey=cd6ba9fe4f644dc692dee61ce9c7718d".format(d3))
    res = data.json()
    res = res['articles']
    description = []
    title = []
    url=[]
    publishedAt = []
    for i in res:
        if i['urlToImage']==None:
            continue
        else:
            description.append(i['urlToImage'])
            title.append(i['title'])
            url.append(i['url'])
            publishedAt.append(i['publishedAt'][:10])
        
    z = zip(description,title,url,publishedAt)
    return render(request,'prediction/News.html',{'world' : z})

def Detection(request):
    return render(request,'prediction/Detection.html')

def PredictionResult(request):
    pkl_path = "Symptom.pkl"
    with open(pkl_path, 'rb') as f:
        model = pickle.load(f)
    Cough = { 'Yes' : 1 , 'No' :0 }
    Fever = { 'Male' : 1 , 'Female' : 0 }
    Drug = { 0 : 'Negative' , 2 : 'Positive' , 1 :'Other' }
    l=[]
    l.append(Cough[request.GET['Age']])
    l.append(Cough[request.GET['Sex']])
    l.append(Cough[request.GET['BP']])
    l.append(Cough[request.GET.get('Cholestrol', '')])
    l.append(Cough[(request.GET['Na_to_k'])])
    l.append(Fever[(request.GET['Gender'])])
    print(l)
    test2= pd.DataFrame([l],columns= ['cough', 'fever', 'sore_throat', 'shortness_of_breath', 'head_ache', 'gender'],dtype=float)
    res=model.predict(test2)[0]
    

    return render(request,'prediction/PredictionResult.html',{'res':Drug[res]})

    