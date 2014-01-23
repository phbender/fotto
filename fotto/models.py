from fotto import db
from mongoengine import signals
import logging

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

class View(db.Document):
    images = db.ListField(db.ReferenceField(Image))
    name = db.StringField(required=True, max_length=60)
    slug = db.StringField(required=True, max_length=60)
    owner = db.ReferenceField(User, required=True)

    def __unicode__(self):
        return self.name

