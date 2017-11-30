# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from backend.crawler import Crawler


class CrawlSite(object):
    def __init__(self, name='crawl'):
        self.name = name

    def render(self, request, template_name, context):
        return render(request, template_name, context)

    def check_url(self, target_url):
        result = True
        validator = URLValidator(schemes=['http', 'https'])
        try:
            validator(target_url)
        except ValidationError:
            result = False

        return result

    def index(self, request):
        template = 'crawl/index.html'
        context = {}
        if request.method == 'POST':
            target_url = request.POST['targetUrl']
            if not self.check_url(target_url):
                context = {'target_url': target_url, 'error': 'Invalid URL! Please start with http:// or https://'}
            else:
                if not target_url.endswith('/'):
                    target_url += '/'
                context = {'target_url': target_url, 'urls': Crawler().crawl(target_url)}

        return self.render(request, template, context)
