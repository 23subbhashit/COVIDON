from django.shortcuts import render
import pickle
import requests
from datetime import date
import pandas as pd
from django.http.response import StreamingHttpResponse
from prediction.camera import VideoCamera
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode,iplot
import plotly.express as px
from plotly.offline import plot
a = 0 
# Create your views here.


def main(request):
    data = requests.get("https://covid19.mathdro.id/api/")
    result1 = requests.get("https://coronavirus-19-api.herokuapp.com/countries").json()
    d = dict()
    for i in result1:
        d[i['country']]=i['cases']
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

    # plot_div = maps.world_map()
    f= go.Figure(data=go.Choropleth(
        locations=country,
        z =cases, 
        locationmode = 'country names', 
        colorscale =px.colors.sequential.Plasma,
        colorbar_title = "NO. of players",
    ))

    f.update_layout(
        title_text = 'Number of Covid Cases From Top 50 Countries',
    )
    plot_div = plot(f, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})

    return render(request,'prediction/main.html',{'confirmed' : confirmed, 'deaths' : deaths  ,'recovered' :recovered , 'world' : z,'usa_map': plot_div})

def Predict(request):
    return render(request,'prediction/Predict.html')

def Prevention(request):
    return render(request,'prediction/Prevention.html')

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

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame') 
    
def index(request):
	return render(request, 'prediction/home.html')