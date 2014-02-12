#coding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from lingvo.models import article
from django.views.decorators.csrf import csrf_exempt
from source.lingvo.models import Dictonary


@csrf_exempt
def main(request):
    if 'keywords' in request.POST:
        keywords = request.POST['keywords']
        a = article.search.query(keywords)
    else:
        keywords = ''
        a = None
    return render_to_response('index.html', {'article': a, 'keywords': keywords})


def dictionaries(request):
    return render_to_response('dicts.html', {'dicts': Dictonary.objects.all()})


@csrf_exempt
def dictonary(request, id=False):
    """
    TODO add forms and validation
    """
    if request.method == 'POST':
        if id:
            dict = get_object_or_404(Dictonary, pk=id)
        else:
            dict = Dictonary()
        dict.name = request.POST['name']
        dict.dict = request.POST['dict']
        dict.save()
    else:
        if id:
            dict = get_object_or_404(Dictonary, pk=id)
        else:
            dict = False
    return render_to_response('dict.html',{'dict':dict})


