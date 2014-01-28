from fotto import db, exifdata, imageinfo
from fotto import thumbnail
from mongoengine import signals
import logging
from flask import url_for

Q = db.Q


class User(db.Document):
    email = db.EmailField(unique=True, required=True)
    name = db.StringField(required=True, max_length=60)

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)


class ImageVersion(db.Document):
    version_hash = db.StringField(required=True, max_length=100)
    image_data = db.FileField(required=True)

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        document.image_data.delete()

signals.pre_delete.connect(ImageVersion.pre_delete, sender=ImageVersion)


class Image(db.Document):
    owner = db.ReferenceField(User, required=True)
    tags = db.ListField(db.StringField(max_length=50))
    caption = db.StringField(max_length=400)
    name = db.StringField(max_length=60)
    image_data = db.FileField(required=True)

    versions = db.ReferenceField(ImageVersion, reverse_delete_rule=db.CASCADE)

    def set_image(self, fh):
        info = imageinfo(fh)
        self.image_data.put(fh, **info)

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
    def image_infos(self):
        for index, image in enumerate(self.images):
            url = url_for('view_image', selector='id',
                          seq_num=index, collection_id=self.id)
            aspect = image.image_data.aspect_ratio
            yield dict(url=url, aspect_ratio=aspect)

    meta = {'allow_inheritance': True}


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

