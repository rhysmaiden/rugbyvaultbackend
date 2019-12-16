import wikipedia
import os
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()



page_image = wikipedia.page("Michael Hooper rugby")
print(page_image.images[0])
