from django.http import HttpResponse
from django.template import loader
import requests

# Create your views here.
def index(request):
    # Render the index.html template
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None, request))
    
def generate(request):
    # Get the input string from the form
    input_string = request.POST.get('input_string')
    # Call the graphic_art tool with the input string

    # response = requests.post('https://bing.com/graphic_art', data={'prompt': input_string})
    # Get the image url from the response
    # image_url = response.json().get('image_url')

    # Render the generate.html template with the image url
    template = loader.get_template('generate.html')
    # image url should be the url of the image returned from the graphic_art tool
    context = {'image_url': 'https://picsum.photos/id/237/200/300',
               'text' : input_string}
    return HttpResponse(template.render(context, request))
