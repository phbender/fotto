from fotto import db, exif
from mongoengine import signals
import logging
from StringIO import StringIO
from flask import url_for

Q = db.Q

class User(db.Document):
    email = db.EmailField(unique=True, required=True)
    name = db.StringField(required=True, max_length=60)

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)

class Image(db.Document):
    owner = db.ReferenceField(User, required=True)
    tags = db.ListField(db.StringField(max_length=50))
    caption = db.StringField(max_length=400)
    name = db.StringField(max_length=60)
    image_data = db.FileField(required=True)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        pass

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        """Important: clean up image data"""
        logging.debug("deleting %s" % document)
        document.image_data.delete()


    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return "(unnamed)"

signals.pre_delete.connect(Image.pre_delete, sender=Image)
signals.pre_save.connect(Image.pre_save, sender=Image)

class Collection(db.Document):
    name = db.StringField(required=True, max_length=60)
    slug = db.StringField(required=True, max_length=60)
    owner = db.ReferenceField(User, required=True)
    public = db.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def image_urls(self):
        for index, image in enumerate(self.images):
            yield url_for('view_image', selector='id', seq_num=index, collection_id=self.id)

    meta = {'allow_inheritance' : True }

class ListCollection(Collection):
    images = db.ListField(db.ReferenceField(Image))

class TagCollection(Collection):

    tags = db.ListField(db.StringField(max_length=60))

    @property
    def images(self):
        q_obj = Q()
        for t in self.tags:
            q_obj |= Q(tags=t)

        return Image.objects(q_obj)

