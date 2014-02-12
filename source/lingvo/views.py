#coding: utf-8
from collections import defaultdict
from operator import itemgetter
import nltk
import re
from django.shortcuts import render_to_response, get_object_or_404
from models import article
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
def dictionary(request, id=False):
    """
    TODO add forms and validation
    """
    if request.method == 'POST':
        if id:
            dict = get_object_or_404(Dictonary, pk=id)
        else:
            dict = Dictonary()
        dict.name = request.POST['name']
        dict.dict = " ".join(set(prepeare_words(request.POST['dict']).split()))
        dict.save()
    else:
        if id:
            dict = get_object_or_404(Dictonary, pk=id)
        else:
            dict = False
    return render_to_response('dict.html',{'dict':dict})


def dicttop(request, id=False):
    dict = get_object_or_404(Dictonary, pk=id)
    dict_words = dict.dict.split()
    articles = article.objects.all()
    arts = []
    for a in articles:
        arts.append({"article":a,"sum":get_count(a, dict_words)})
    arts = sorted(arts, key=itemgetter('sum'),reverse=True)
    return render_to_response('dicttop.html', {"articles":arts[0:10]})


def prepeare_words(text):
    text = re.sub('[,!.;:\'?\-"]', ' ', text)
    words = nltk.word_tokenize(text.lower())
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    words = [lmtzr.lemmatize(w) for w in words]
    return " ".join(words)


def get_count(a, dict_words):
    words = prepeare_words(a.article).split()
    summ = 0
    for w in dict_words:
        summ += words.count(w)
    return summ