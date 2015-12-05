# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class GuestBook(ndb.Model):
    ime = ndb.StringProperty(default = "Neznanec")
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty(required=True)
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
