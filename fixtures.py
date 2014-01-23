from fotto.models import *

import sys

User.objects.delete()
Image.objects.delete()
View.objects.delete()

me = User(name="Hui Booh", email="huibooh@castle.net")
me.save()

names = "house dog sheep cattle milk bear car tyre boat snow castle ghost shepherd".split()

f = open(sys.argv[1])

v = View(owner=me, name="A generic view", slug="generic-view")

for n in names:
    f.seek(0)
    i = Image(name=n, owner=me, caption="a totally random %s" % n)
    i.image_data.put(f, content_type="image/jpeg")
    i.save()

    v.images.append(i)

v.save()

