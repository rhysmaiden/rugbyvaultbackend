import wikipedia
import os
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Player

players = Player.objects.all()

x=0

for p in players:

    x+=1

    print(str(x) +"/" + str(len(players)))

    #Move to send of for loop later
    if p.picture == 'x' or "flag" in p.picture.lower():
        p.picture = "http://www.bakingtradeshow.com.au/wp-content/uploads/2016/03/blank-profile-male.png"
        p.save()
        continue
    else:
        continue




    try:
        page_image = wikipedia.page(p.name + " rugby")

        p.picture = page_image.images[0]
        p.save()
    except:
        continue
