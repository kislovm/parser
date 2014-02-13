#coding: utf-8
from collections import Counter
import json
from operator import itemgetter
import nltk

from django.shortcuts import render_to_response, get_object_or_404
from models import article
from django.views.decorators.csrf import csrf_exempt
from source.lingvo import lmtzr, cache_function
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
        dict.dict = " ".join(set(prepeare_words(request.POST['dict'])))
        dict.save()
    else:
        if id:
            dict = get_object_or_404(Dictonary, pk=id)
        else:
            dict = False
    return render_to_response('dict.html', {'dict': dict})


def dicttop(request, id=False):
    sort_directions = ["sum_all", "len_all", "len_unique", "sum_unique", 'relation_all','relation_unique']
    sort_direction = request.GET.get('dir',"sum_all")
    if sort_direction not in sort_directions:
        sort_direction = "sum_all"
    dict = get_object_or_404(Dictonary, pk=id)
    dict_words = dict.dict.split()
    articles = article.objects.all()
    arts = sorted([get_count(a, dict_words) for a in articles], key=itemgetter(sort_direction), reverse=True)
    return render_to_response(
        'dicttop.html',
        {
            'articles': arts[0:10],
            'dict': json.dumps(dict_words),
            'sort_direction': sort_direction,
            'sort_directions': sort_directions
        }
    )

def prepeare_words(text):
    tikenizer = nltk.RegexpTokenizer(r'\w+')
    words = tikenizer.tokenize(text.lower())
    return [lmtzr.lemmatize(w, 'v') for w in words]

def get_count(a, dict_words):
    words = prepeare_words(a.article)
    unque_words = set(words)
    sum_all = sum([words.count(w) for w in dict_words])
    len_all = len(words)
    len_unique = len(unque_words)
    sum_unique = len_unique - len(unque_words - set(dict_words))
    return {
        "article": a,
        "sum_all": sum_all,
        "len_all": len_all,
        "len_unique": len_unique,
        "sum_unique": sum_unique,
        'relation_all': float(sum_all) / float(len_all),
        'relation_unique': float(sum_unique) / float(len_unique)
    }