#coding: utf-8
from django.shortcuts import render_to_response
from lingvo.models import article
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def main(request):
    if 'keywords' in request.POST:
        keywords = request.POST['keywords']
        a = article.search.query(keywords).set_options(passages=True, passages_opts={
            'before_match': "<span class='highlight'>",
            'after_match': '</span>',
            'chunk_separator': ' ... ',
            'around': 1000000000
         })
    else:
        keywords = ''
        a = None
    return render_to_response('index.html', { 'article': a, 'keywords': keywords })