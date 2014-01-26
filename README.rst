====================================
Fotto, the friendly Photo Sharepoint
====================================

Fotto allows you to manage your pictures. In a secure and self-hosted way,
this means you have 100% control about your data. Fotto is no Flickr replacement,
nor it offers the feature set you probably are used to have.

Fotto is different.

* Fotto allows you to create *collections* of on your pictures. Every collection is connected
  to an URL, which exaclty delivers the images you want the visitor to see. 
  Other images are kept in privacy.

* A collection can be generated statically with a predefined set of images, or
  dynamically by means of categories and tags.

* A collection can be disabled at any time, rendering the URLs to this view
  useless.

* Collections can be kept in private, or they may be published. Private collections mean
  that no one knows the URL, except the people you shared the URL with. A public
  collection is listed in your profile and has a nice URL. Even without listing that
  collection, it should no longer be considered private since nice URLs are predictable
  as well.

Quickstart
==========

After cloning the repository, set up the working environment.

.. code::

    $ mkvirtualenv fotto
    $ pip install -r requirements.txt
    $ python fixtures.py img1.jpg img2.jpg ...

    $ ./manage.py runserver

Now, open your browser and navigate to 
``http://localhost:5000/collection/generic-view/0``. You should see the first of
your image now. See ``views.py`` for other URLs to play with.
