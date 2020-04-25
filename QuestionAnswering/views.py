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
from nltk.corpus import words
import nltk
import re
from QuestionAnswering.QA_Model.interact import GetEvidence
from QuestionAnswering.prepare_content import prepare_content_QA
import time
from django_ajax.decorators import ajax
import os
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
nltk.download('words')
r=sr.Recognizer()
answer=""
wh_q_list=['what','when','where','whose','which','who','whom','why','how','in','on','is','was','are','will','can','from']
def contact(request):
    return render(request,'contact.html',context=None)
def documentation(request):
    return render(request,'Documentation.html',context=None)
def about(request):
    return render(request,'About.html',context=None)
def details(request):
    one_paragraph=""
    c={}
    corpus=[]
    refrences=[]
    start_timer=time.time()
    try:
        c.update(csrf(request))
        source=request.POST.get('Que').lower()
        print(source)
        sq = wikipedia.search(source,results=3)
        c.update({'title':source})
        corpus.append(source)
        for i,j in enumerate(sq):
            print(i,wikipedia.page(j).url)
            tokenize_page_words = (wikipedia.page(j).content).replace('=','') 
            imp_words=' '.join([word for word in tokenize_page_words.split()])
            corpus.append(imp_words)
            refrences.append(wikipedia.page(j).url.replace("https://en.wikipedia.org/","")) 
        refrences= list(dict.fromkeys(refrences))
        c.update({'refrences':refrences})
        first_word=source.split()[0]
        first_word=first_word.lower()
        if(first_word not in wh_q_list):
            answer=wikipedia.summary(source,sentences=1)
        else:
            one_paragraph=prepare_content_QA(corpus)
            if(len(one_paragraph)==0):
                return render(request,'details.html',None)
            answer = GetEvidence(one_paragraph,source)
        c.update({'data1':answer})
        myobj = gTTS(text=answer, lang='en', slow=False)
        if os.path.exists('answer.mp3'):
            os.remove("answer.mp3")
        myobj.save("answer.mp3")
        print("Answer:",answer)
        end_timer=time.time()
        c.update({'ti':format(round(end_timer - start_timer,2))})
        print('Total Time: {:.4f}s'.format(end_timer - start_timer)) 
        return render(request,'details.html',c)    
    except Exception as e:
        print("Exception:",e)
        print('type is:', e.__class__.__name__)
        return render(request,"details.html",None)

class HomePageView(TemplateView):
    def get(self,request,**kwargs):  
        return render(request,'index.html',context=None)

@ajax
def askquestion(request):
    phnumber=request.GET.get('phnumber')
    mailid=request.GET.get('mailaddress')
    mes=request.GET.get('mes')
    finmessage="Phone Number :"+phnumber+"\nMy EmailAddress :"+mailid+"\n\nMessage :"+mes
    message = MIMEMultipart("alternative")
    message["Subject"] = "QA_System Application Notifications"
    sender_email="bankingsys12@gmail.com"
    receiver_email= "mnkantariya173@gmail.com"
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(finmessage, "plain")
    port = 465
    password ="ASqw12!@"
    message.attach(part1)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
        server.login("bankingsys12@gmail.com", password)
        server.sendmail(sender_email,receiver_email,message.as_string())

@ajax
def saveans(request):
    question=request.GET.get('question')
    suggested_answer=request.GET.get('answer')
    tempdictionary={}
    if(question=="" or suggested_answer==""):
        return {'result':-11}
    tempdictionary[question]=suggested_answer
    with open('QuestionAnswering/QA_Model/SuggestedAnswers.json', 'a+') as outfile:
        json.dump(tempdictionary, outfile)
    return {'result':1}

@ajax
def getwords(request):
    word_list = words.words()
    return {'result':word_list}
   
@ajax
def playsnd(request):
    playsound('answer.mp3')
    return {'result':"success"}
@ajax
def openmic(request):
    with sr.Microphone() as source:
        audio=r.listen(source)  
    print("Listening...")
    try:
        print("Asked:"+r.recognize_google(audio))
    except (sr.WaitTimeoutError,sr.UnknownValueError,sr.RequestError):
        er='NO'
        return {'result':er}
    que=r.recognize_google(audio)
    return {'result': que}

