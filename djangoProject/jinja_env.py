from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    #print(vars(staticfiles_storage.__dict__['_wrapped']))
    env = Environment(**options)
    #print(staticfiles_storage.url('main/js/formCheck.js'))
    env.globals.update(
        {'static': staticfiles_storage.url, 'url': reverse}
    )
    return env
