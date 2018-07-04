from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from youtubeJukebox.models import Video, User, Vote
from django_slack_oauth.models import SlackUser
from django.core import serializers
import json

def index(request):
	videos = Video.objects.order_by('-votes').all()
	video_json = json.dumps([item['fields'] for item in serializers.serialize('python', videos)])
	
	context = {'videos': videos, 'video_json': video_json}

	response = render (request, 'youtubeJukebox/index.html', context)
	if 'user' in request.session :
		response.set_cookie('user',request.session['user'] )
	return response

def vote(request):
	vid = request.GET['vid']
	userId = request.session['userid']
	
	user = User.objects.get(user_id=userId)
	video = Video.objects.get(videoId=vid)

	votes = Vote.objects.all().filter(user=user, video=video)
	
	if(len(votes) == 0):
		video.votes += 1
		video.save()
		vote = Vote(user=user, video=video)
		vote.save()

	return JsonResponse({
		'result': 'success',
		'votes': video.votes
	})
	

def debug_oauth_request(request, api_data):
	request.session['foo'] = 'bar'
	return request, api_data

def register_user(request, api_data):
	if api_data['ok']:
		useridList = User.objects.all()
		userList = {q.user_id for q in useridList}
		if api_data['user']['id'] not in userList :
			values = User(user=api_data['user']['name'],user_id=api_data['user']['id'])
			values.save()
			print("\nNew User added to database")
		else :
			print("\nUser already exist")
	request.session['user'] = api_data['user']['name']
	request.session['userid'] = api_data['user']['id']
	request.session['access_token'] = api_data['access_token']


	return request, api_data

def logout(request):
	del request.session['user']
	return redirect('/')