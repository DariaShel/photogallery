import os

from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

from photosite.models import Years

# Create your views here.
@login_required
def HelloPage(request):
	return render(request,'folders.html')

@login_required
def List(request,path=settings.ROOT_PATH):
	args = {}
	args['rp']=path

	if os.path.isdir(path):
		cat_list = os.listdir(path)

		col = 3 #  столбцы
		row = int(len(cat_list)/col) # строки

		q = []

		for i in range(len(cat_list)//col):
			q.append(cat_list[i*col:(i+1)*col])	  	

		args['list']=q

		return render(request,'list.html', args)

	else:
		return render(request,'file.html', args)	

@login_required
def Image(request,path=settings.ROOT_PATH):
	args = {}
	args['rp']=path
	response = HttpResponse()
	response["Content-Type"] = 'image/jpeg'
	im = open(path, 'br')
	response.write(im.read())	
	im.close()
	return response

def LoginView(request):
	args = {}
	args.update(csrf(request))

	try:
		username = request.POST['username']
		password = request.POST['password']
	except KeyError:
		return render(request, 'photo_login.html', args)
    
	next_url = request.GET.get('next',reverse("list"))

	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect(next_url)
		else:
			args['system_message']={'text':'This account is not active!','type':'alert'}
			return handler403(request,args)
   
	else:
		args['system_message']={'text':'User does not exist or the password is incorrect!','type':'alert'}
		return handler403(request,args)

    #return handler403(request,args)
   

def LogoutView(request):
	logout(request)
	args = {}
	return redirect(reverse('hello'))

def handler403(request,args):
	response = render(request, 'photo_login.html', args)
	response.status_code = 403
	return response