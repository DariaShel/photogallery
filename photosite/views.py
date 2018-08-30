import os
import io
from PIL import Image
from PIL.ExifTags import TAGS

from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

from photosite.models import Favorites
# Create your views here.

@login_required
def List(request,path=settings.ROOT_PATH,fav=None):
	args = {}
	args['rp']=path
	if path==settings.ROOT_PATH:
		head = path
	else:
		(head, tail)=os.path.split(path)
	args['back']=head

	cat_list = os.listdir(path)
	col = settings.FOTO_COLS #  столбцы
	row = int(len(cat_list)/col) # строки

	q = []
	l=[]
	

	if os.path.isdir(path) and cat_list:
		j=0
		for i in cat_list:
			x={}
			if i.find('.jpg')<0 and i.find('.JPG')<0 and i.find('.jpeg')<0:
				x = dict(name=i, type='fold')
			else:
				if fav is None:
					p=os.path.join(path,i)
					u=request.user
					try:
						favrow=Favorites.objects.get(uid=u, path=p)
						fav=1
						title=favrow.title if favrow.title else i
					except Exception as err:
						fav=0
						title=i
					
				x = dict(name=i, type='img', num=j, fav=fav, title=title)
				j+=1
			l.append(x)
		if len(l)%col != 0:
			for i in range(len(l)//col+1):
				if i==len(l)//col:
					q.append(l[i*col:(i+1)*col-(col-len(l)%col)])
				else:
					q.append(l[i*col:(i+1)*col])
		else:
			for i in range(len(l)//col):
				q.append(l[i*col:(i+1)*col])
		if len(q[-1])<col:
			while len(q[-1])!=col:
				q[-1].append(dict(name='empty', type='empty'))
		args['list']=q

		return render(request,'list.html', args)

	elif cat_list:
		return render(request,'file.html', args)	
	else:
		return render(request,'base.html', args)	

@login_required
def Pic(request,path=settings.ROOT_PATH):
	args = {}
	args['rp']=path
	response = HttpResponse()
	response["Content-Type"] = 'image/jpeg'
	im = open(path, 'br')
	response.write(im.read())	
	im.close()
	return response

@login_required
def Preview(request,path=settings.ROOT_PATH):
	args = {}
	args['rp']=path
	response = HttpResponse()
	response["Content-Type"] = 'image/jpeg'
	im = Image.open(path)
	exif_orientation = 0
	try:
		exif = im._getexif()
	except:
		exif = None
	if exif != None:
		for tag, value in exif.items():
			decoded = TAGS.get(tag, tag)
			if isinstance(decoded,str):
				if decoded.lower() == 'orientation':
					exif_orientation = value
					break
	if exif_orientation == 3: im=im.rotate(180,expand=True)
	if exif_orientation == 6: im=im.rotate(270,expand=True)
	if exif_orientation == 8: im=im.rotate(90,expand=True)
	#im.thumbnail((settings.PREVIEW_SIZE, settings.PREVIEW_SIZE))
	preview = io.BytesIO()
	im.save(preview, 'JPEG')
	response.write(preview.getvalue())
	return response

@login_required
def Thumb(request,path=settings.ROOT_PATH):
	args = {}
	args['rp']=path
	response = HttpResponse()
	response["Content-Type"] = 'image/jpeg'

	thumb = Image.open(path)
	exif_orientation = 0
	try:
		exif = thumb._getexif()
	except:
		exif = None
	if exif != None:
		for tag, value in exif.items():
			decoded = TAGS.get(tag, tag)
			if isinstance(decoded,str):
				if decoded.lower() == 'orientation':
					exif_orientation = value
					break
	if exif_orientation == 3: thumb=thumb.rotate(180)
	if exif_orientation == 6: thumb=thumb.rotate(270)
	if exif_orientation == 8: thumb=thumb.rotate(90)
	thumb.thumbnail((settings.THUMB_SIZE, settings.THUMB_SIZE))
	(x,y)=thumb.size
	if x>y:
		z=(x-y)/2
		new=thumb.crop((z,0,x-z,y))
	else:
		z=(y-x)/2
		new=thumb.crop((0,z,x,y-z))
	tfile = io.BytesIO()
	new.save(tfile, 'JPEG')
	response.write(tfile.getvalue())
	return response	

@login_required
def SetFav(request, path, value='2'):
	try:
		f=Favorites.objects.get(uid=request.user, path=path)
	except:
		f=None

	if (value=='1') and (f==None):
		Favorites.objects.create(uid=request.user, path=path)

	if (value=='0') and (f!=None):
		f.delete()
	# fav = int(request.GET.get('fav',''))
	print(path)
	response = HttpResponse()
	response["Content-Type"] = 'text/html'
	response.write(value)
	return response

	# return List(request,path,fav)

@login_required
def PageFav(request):
	f = Favorites.objects.filter(uid=request.user)
	args = {}
	col = settings.FOTO_COLS
	l = []
	q = []
	j=0
	for i in f:
		title=i.title if i.title else os.path.basename(i.path)
		x = dict(path=i.path,name=title,num=j)
		j+=1
		l.append(x)

	if len(l)%col != 0:
		for i in range(len(l)//col+1):
			if i==len(l)//col:
				q.append(l[i*col:(i+1)*col-(col-len(l)%col)])
			else:
				q.append(l[i*col:(i+1)*col])
	else:
		for i in range(len(l)//col):
			q.append(l[i*col:(i+1)*col])
	if len(q[-1])<col:
		while len(q[-1])!=col:
			q[-1].append(dict(name='empty', type='empty'))
	args['list']=q

	return render(request,'favorites.html', args)



def LoginView(request):
	args = {}
	args.update(csrf(request))

	try:
		username = request.POST['username']
		password = request.POST['password']
	except KeyError:
		return render(request, 'photo_login.html', args)
    
	next_url = request.GET.get('next',reverse('list'))

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
	return redirect(reverse('list'))

def handler403(request,args):
	response = render(request, 'photo_login.html', args)
	response.status_code = 403
	return response