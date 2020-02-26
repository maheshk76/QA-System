from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
import speech_recognition as sr
import wikipedia
import codecs
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gtts import gTTS
from playsound import playsound
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from django_ajax.decorators import ajax
from nltk.corpus import words
import nltk
import re
nltk.download('words')
r=sr.Recognizer()
def about(request):
    return render(request,'About.html',context=None)
def details(request):
    c={}
    c.update(csrf(request))
    source=request.POST.get('Que')
    print(source)
    #stopWords = set(stopwords.words("english"))
    refrences=[]#list of referenced links
    try:
        sq = wikipedia.search(source,results=5)
        data1=wikipedia.summary(source,sentences=1)
        print(data1)
        myobj = gTTS(text=data1, lang='en', slow=False)
        myobj.save("data.mp3")
        for i,j in enumerate(sq):
            print(i,wikipedia.page(j).url)
            c.update({'data1':data1})
            c.update({'title':source})
            refrences.append(wikipedia.page(j).url)  
            c.update({'refrences':refrences})             
        return render(request,'details.html',c)    
    except Exception:
        c.update({'exceptions':'ValueError'})
    return render(request,"details.html",c)
class HomePageView(TemplateView):
    def get(self,request,**kwargs):  
        return render(request,'index.html',context=None)
@ajax
def getwords(request):
    word_list = words.words()
    return {'result':word_list}
   
@ajax
def playsnd(request):
    playsound('data.mp3')
    flag="ok"
    return {'result':flag}
@ajax
def openmic(request):
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)  
    try:
        print(":"+r.recognize_google(audio))
    except sr.UnknownValueError:
        er='NO'
        return {'result':er}
    que=r.recognize_google(audio)
    print(que)
    return {'result': que}

