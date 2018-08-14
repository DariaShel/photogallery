from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def HelloPage(request):
#	args = {}

#	if not request.user.is_authenticated:
#		return render(request, 'photo_login.html', args)

	return render(request,'folders.html')

def LoginView(request):
	args = {}
	args.update(csrf(request))

	try:
		username = request.POST['username']
		password = request.POST['password']
	except KeyError:
		return render(request, 'photo_login.html', args)
    
	next_url = request.GET.get('next',reverse("hello"))

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