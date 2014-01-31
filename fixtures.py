from fotto.models import *
from fotto import exif

import sys

User.objects.delete()
Image.objects.delete()
Collection.objects.delete()

me = User(name="Hui Booh", email="huibooh@castle.net")
me.save()

v = ListCollection(owner=me, name="A generic view", slug="generic-view", public=True)

for n in sys.argv[1:]:
    f = open(n, 'r')
    ed = exif.exifdata(f)
    f.seek(0)
    tags = [i.strip() for i in ed["Subject"].split(',')]
    i = Image(name=ed.get("Title", "untitled"), owner=me, caption=ed.get("Description", "-"))
    i.set_image(f)
    for t in tags:
        i.tags.append(t)
    i.save()

    print i

    v.images.append(i)

v.save()

tag_coll = TagCollection(owner=me, name="Ostsee", slug="ostsee", public=True)
tag_coll.tags.append('ostsee')
tag_coll.tags.append('ham')

tag_coll.save()

