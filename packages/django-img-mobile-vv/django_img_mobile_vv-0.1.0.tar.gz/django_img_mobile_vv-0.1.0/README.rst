Django Image Mobile
==================
Django app designed to be able to use lower quality images for the mobile version of your site. 
(This package was created quickly and for later use in my company :3)

Installation
============
Install django_img_mobile_vv, you'll have to make sure that user-agents is installed first::

1. Install ``django_img_mobile_vv``, you'll have to make sure that `user-agents`_ is installed first::

    pip install pyyaml ua-parser user-agents 

2. Configure ``settings.py``:

   .. code-block:: python

    INSTALLED_APPS = (
        # Other apps...
        'django_img_mobile_vv',
    ) 
    # Prefix to a small file, for example a large 'image.jpg' and a small one would be 'image-min.jpg'
    # I use a service https://imagecompressor.com/ to optimize the size of images 
    STATIC_IMG_PREFIX = '-min'
    
Usage
=====

Middleware
----------

Add ``UserAgentMiddleware`` in ``settings.py``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # other middlewares...
        'django_img_mobile_vv.middleware.UserAgentMiddleware',
    )

A ``user_agent`` required to get information about what type of device the user is using
  
     # add load tag  static_mobile
     {% load static_mobile %}
     # old static image
     {% static 'img/girl2.png' %}
     # new static image with small image
     {% static_img 'img/girl2.png' %}
     
