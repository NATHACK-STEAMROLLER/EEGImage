from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Image
import subprocess
import os
import random
import time
import requests
# # Create your views here.
# def index(request):
#     # Render the index.html template
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render(None, request))
    
# def generate(request):
#     # Get the input string from the form
#     input_string = request.POST.get('input_string')
#     # Call the graphic_art tool with the input string

#     # response = requests.post('https://bing.com/graphic_art', data={'prompt': input_string})
#     # Get the image url from the response
#     # image_url = response.json().get('image_url')

#     # Render the generate.html template with the image url
#     template = loader.get_template('generate.html')
#     # image url should be the url of the image returned from the graphic_art tool
#     context = {'image_url': 'https://picsum.photos/id/237/200/300',
#                'text' : input_string}
#     return HttpResponse(template.render(context, request))




def start_page(request):
    return render(request, 'start_page.html')

def countdown_page(request):
    # Simulate a 5-second countdown
    # for i in range(5, 0, -1):
    #     time.sleep(1)

    command = 'cd ../visualizing; ./start.sh'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)

    path = '~/EEGImage/EEGImage/generateImage/static/cur_img.txt'
    expanded = os.path.expanduser(path)
    # with open(expanded, 'r') as f:
    #    cur_img_name = f.readline()
    # Generate a random image (replace this with your logic)


    return render(request, 'countdown_page.html')

def image_processing(request):
    return render(request, 'image_processing.html')


def image_display(request):
    # image_url = "{% static 'v1_txt2img.png' %}"  # Example URL
    #
    # # add to database
    # image = Image(image_url=image_url)
    # image.save()
    return render(request, 'image_display.html')#, {'random_image_url': image_url})


def history(request):
    images = Image.objects.all().values()
    template = loader.get_template('history.html')
    context = {'images': images}
    return HttpResponse(template.render(context, request))
