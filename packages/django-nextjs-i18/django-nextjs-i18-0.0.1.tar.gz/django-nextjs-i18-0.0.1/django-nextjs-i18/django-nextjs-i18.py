from django.views.generic import TemplateView
from django.urls import path
from django_arg_path import arg_path



class i18_language_list():
    def __init__(self, languages='',default='',others=[], *args, **kwargs):
        self.args=args
        language=[]
        if others:
            language=[[lang+'/', lang, f"_{lang}"] for lang in others]
        if languages:
            kw_lang=[]
            for val in languages:
                kw_lang.append([val['url'],val['arg'],val['name']])
            language=language+kw_lang
        if default:
            language.append(['',default,'_'+default])
        self.languages=language

    def method_path(self, route, view, name, *args, **kwargs):
        return [ arg_path(slug[1],slug[0]+route,view=view, name=name+slug[2], *args, **kwargs) for slug in self.languages]

    def template_path(self, route, tname, name, *args, **kwargs):
        return [ path(slug[0]+route,view=TemplateView.as_view(template_name=slug[1]+tname), name=name+slug[2], *args, **kwargs) for slug in self.languages]

    def urlpatterns(self, langlist):
        urlpatterns=[lang for langarray in langlist for lang in langarray ]
        return urlpatterns