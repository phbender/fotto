====================================
Fotto, the friendly Photo Sharepoint
====================================

Fotto allows you to manage your pictures. In a secure and self-hosted way,
this means you have 100% control about your data. Fotto is no Flickr replacement,
nor it offers the feature set you probably are used to have.

Fotto is different.

* Fotto allows you to create *views* on your pictures. Every view is connected
  to an URL, which exaclty delivers the images you want the visitor to see. 
  Other images are kept in privacy.

* A view can be generated statically with a predefined set of images, or
  dynamically by means of categories and tags.

* A view can be disabled at any time, rendering the URLs to this view
  useless.

* Views can be kept in private, or they may be published. Private views mean
  that no one knows the URL, except the people you shared the URL with. A public
  view is listed in your profile and has a nice URL. Even without listing that
  view, it should no longer be considered private since nice URLs are predictable
  as well.

Quickstart
==========

After cloning the repository, set up the working environment.

  $ mkvirtualenv fotto
  $ pip install -r requirements.txt
  $ python fixtures.py /path/to/a/dummy_image.jpg

  $ ./manage.py runserver

Now, open your browser and navigate to 
``http://localhost:5000/views/generic-view/4``. You should see the dummy
image now. See ``views.py`` for other URLs to play with.
