from fotto.models import *
from fotto import exif

import sys

User.objects.delete()
Image.objects.delete()
View.objects.delete()

me = User(name="Hui Booh", email="huibooh@castle.net")
me.save()

v = View(owner=me, name="A generic view", slug="generic-view")

for n in sys.argv[1:]:
    f = open(n, 'r')
    ed = exif.exifdata(f)
    tags = [i.strip() for i in ed["Subject"].split(',')]
    i = Image(name=ed["Title"], owner=me, caption=ed["Description"])
    i.image_data.put(f, content_type="image/jpeg")
    for t in tags:
        i.tags.append(t)
    i.save()

    print i

    v.images.append(i)

v.save()

