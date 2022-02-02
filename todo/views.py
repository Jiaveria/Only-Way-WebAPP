from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import Hadith,islamicarticle,Quiz,QuranicVerse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic.base import TemplateView
from datetime import datetime
import json
import time, random
# Create your views here.

# admin username bunty and password bunty
def index(request):
    return render(request,'index.html' )


def Blog(request):
    # THIS METHOD IS FETCHING 4 BLOGS FROM DB, 3 ARE FETCHED FOR LINKING AND 1 TO DISPLAY ON PAGE(RECENTLY POSTED ONE)
    #blogs = islamicarticle.objects.all()
    #n=islamicarticle.objects.count()
    start_3 = islamicarticle.objects.all().order_by('-article_ID')[:4:-1]
    last_3=reversed(start_3)
    first_article=islamicarticle.objects.get(article_ID=1)

    return render(request, "blog-right-sidebar.html", {"blogs": last_3 ,"blog1":first_article})


def singleblog(request,pk):# blog through recent links
    post=islamicarticle.objects.get(article_slug=pk)
    return render(request,'blog-single.html',{'allPosts':post})

def search(request): 
    query=request.GET['q']
    if (query==''):#If empty query in seach box
        return redirect('index')
    else:
        postTitle= islamicarticle.objects.filter(title__icontains=query)
        postContent= islamicarticle.objects.filter(bcontent__icontains=query)
        allPosts=postTitle.union(postContent)
        return render(request, 'searchedBlogResult.html',{'allPosts': allPosts})
    # #b=islamicarticle.objects.filter(islamicarticle.title)[:5]
    # query=request.GET['q']
    # post= islamicarticle.objects.filter(title__icontains=query)
    # #allPostsList= islamicarticle.objects.filter(title=query)
    # if post.count()==0:
    #     #messages.error(request,"No search result found")
    #     return redirect('index')
    # else:
    #     searchedBlog=post[0]
    #     return render(request, 'blog-single.html',{'allPosts': searchedBlog})


def shopInterface(request):
    return render(request,'islamoshop.html')

#fetching Hadith 
def showHadith(request):
    hadith_list1 = Hadith.objects.all()
    print(hadith_list1)
    return render(request,'hadith.html',{'hadith_list1':hadith_list1})
    

#fetching Hadith 
def showVerse(request):
    verse_list1 = QuranicVerse.objects.all()
    return render(request,'verse.html',{'verse_list1':verse_list1})
    
def contact(request):
    return render(request,'contact.html')

    
def service(request):
    return render(request,'service.html')


def homepage(request):
    return render(request,'index.html')

def attemptQuiz(request):
    questionBank = [] # list of all questions
    Question = Quiz.objects.all() #fetching question from model
    Question_list= list(Question) #converting query set to list 

    for i in range (len(Question_list)): # iterating through each object in Quiz model
        ques_dict = {} # question, options & correct ans for each question is stored in a dictionary
        op_list = []
        q = Question_list[i]
        ques_dict ['question'] = q.question
        op_list.append(q.op1)
        op_list.append(q.op2)
        op_list.append(q.op3)
        op_list.append(q.op4)
        ques_dict ['option'] = op_list
        ques_dict ['answer'] = q.correctop
        questionBank.append(ques_dict) # appending all info of a particular ques to questionBank
    
    questionBank = json.dumps(list(questionBank))
    return render(request,'quiz.html',{'ques':questionBank})