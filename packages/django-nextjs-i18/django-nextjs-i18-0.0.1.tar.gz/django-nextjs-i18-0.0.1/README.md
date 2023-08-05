This is a django implementation of next js exported i18next files. The package helps you use exported next js i18next multilanguage files without writing any url or views with django on its backend. Useage is simple.

1. Implement next js i18next multilanguage with static props. For example we are using 'en', 'ru', 'es', 'it','fr','ar' and 'ar' languages in i18next.
2. Export next js file in a banch inside backend project then direct django staticfiles directory to out folder.
3. Import the package and write the languages that you exported in nextjs-i18 as written below.

```sh

# urls.py
from django-nextjs-i18 import i18_language_list


i18=i18_language_list(default='en',others=['ru','es','it','fr','ar'])
template_path=i18.template_path

app_name='home'

urlpatterns = [
# Home
    template_path('', '.html', name='home'),
# FAQ
    template_path('faq/', '/faq.html', name='faq'),
# Terms And Conditions
    template_path('termsandconditions/', '/termsandconditions.html', name='terms_and_conditions'),
# About
    template_path('about', '/about.html', name='about'),
]

urlpatterns=i18.urlpatterns(urlpatterns)

```

This code generates 6 urls for each template_path that you write in urlpatterns. So you can enter 127.0.0.1:8000 for default('en' in this example) language. Then 127.0.0.1:8000/ru for 'ru' - Russian version and 127.0.0.1:8000/es for 'es' - Spanish version. and etc.

You can also use method_path for more custom views

```sh

def myfunctionview(request, static_path):
    print(static_path) # It will create 6 views and urls in our case(en, ru es,'it','fr','ar') but you can create as many as you want
    return render(request, static_path+'/home.html')

method_path=i18.template_path

urlpatterns = [
# Home
    method_path('', myfunctionview, name='home'),
]

```
