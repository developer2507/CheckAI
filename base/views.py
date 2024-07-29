from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from openai import OpenAI
import os
from .models import File, UserProfile
from .forms import FileUploadForm, StatusUpdateForm


#api_key = 'sk-proj-B9Lkg4kBtmm7RpuJ9XF1T3BlbkFJpek9QRi8zq3VJBJPde7J'
# Create your views here.
def homePage(request):
    
    if request.user.is_authenticated:
        return redirect('panel')
    
    return render(request, 'home.html')


def checkPage(request):
    context = {}

    # Set your OpenAI API key
    api_key = ''

    model_engine = "gpt-3.5-turbo"
    max_tokens = 150

    if request.method == 'POST':
        data = request.POST.get('prompt')
        prompt =  f"Check this and give a review: {data.strip()}" 

        # Set the OpenAI API key globally
        client = OpenAI(api_key=api_key)

        # Create a list of messages where each message is a dict with role and content
        messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]

        # Make API calls using client.chat.completions.create
        response = client.chat.completions.create(
            model=model_engine,
            messages=messages,
            max_tokens=max_tokens
        )

        # Last response from the model
        chatResponse = response.choices[0].message.content

        context = {'chatResponse': chatResponse, 'prompt': prompt}
    

    return render(request, 'check.html', context)
    


def loginPage(request):

    message_error = ""

    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            message_error = "User does not exist"

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('panel')
        else:
            message_error = "Username or Password is wrong"
        

    return render(request, 'login.html', {'error': message_error})


def logoutUser(request):
    logout(request)
    return redirect('home')


# @login_required
def panel(request):
    # If the user is authenticated
    if request.user.is_authenticated:
        
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.status == 'S':
            files = File.objects.all()
            return render(request, 'student_home.html', {'files': files})
        elif user_profile.status == 'T':
            if request.method == 'POST':
                form = FileUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    file_obj = form.save(commit=False)
                    file_obj.uploaded_by = request.user
                    file_obj.save()
                    return redirect('panel')
            else:
                form = FileUploadForm()
            return render(request, 'teacher_home.html', {'form': form})
    else:
        return redirect('home')
        


@login_required
def download_file(request, file_id):
    file_obj = File.objects.get(pk=file_id)
    file_path = file_obj.file.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/force-download")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response