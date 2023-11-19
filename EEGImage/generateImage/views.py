from django.http import HttpResponse
from django.template import loader
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


from django.shortcuts import render
import random
import time

def start_page(request):
    return render(request, 'start_page.html')

def countdown_page(request):
    # Simulate a 5-second countdown
    # for i in range(5, 0, -1):
    #     time.sleep(1)

    # Generate a random image (replace this with your logic)
    random_image_url = "https://picsum.photos/id/237/200/300"  # Example URL

    return render(request, 'countdown_page.html', {'random_image_url': random_image_url})
