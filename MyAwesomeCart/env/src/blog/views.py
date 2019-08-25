from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Post
posts = [


	{
		'author':'coreyMS',
		'title':'Blog Post 1',
		'content':'First post content',
		'date_posted':'august 27, 2018',

	},

	{
		'author':'jane Doe',
		'title':'Blog Post 2',
		'content':'second post content',
		'date_posted':'august 27, 2018',

	}

]
def home(request):
	context = {
		"posts" : Post.objects.all()
	}
	
	
	return render(request,'home.html',context)


def about(request):
	# context = {
	# 	"posts" : posts
	# }
	
	
	return render(request,'about.html')