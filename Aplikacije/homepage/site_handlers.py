#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import datetime
from models import Uporabnik


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        datum = datetime.datetime.now()
        danes = datetime.datetime.strftime(datum,"%d.%m.%Y")
        tocen_cas = datum + datetime.timedelta(hours=1)
        cas = datetime.datetime.strftime(tocen_cas, "%H:%M:%S")
        params = {'datum':danes,"cas":cas}
        return self.render_template("index.html",params=params)

class AboutHandler(BaseHandler):

    def get(self):
        return self.render_template("about.html")

# kontroler Blog
class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")

# kontroler Aktivnosti
class ActivitiesHandler(BaseHandler):
    def get(self):
        return self.render_template("activities.html")

# Kontroler kontakt
class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

# kontroler za  zavihek projekti
class ProjectsHandler(BaseHandler):
    def get(self):
        return self.render_template("projects.html")

# kontroler registracija novega uporabnika
class RegistracijaHandler(BaseHandler):
    def get(self):
        return self.render_template('registracija.html')

    def post(self):
        ime = self.request.get('ime')
        priimek = self.request.get('priimek')
        email = self.request.get('email')
        geslo = self.request.get('geslo')
        ponovno_geslo = self.request.get('ponovno_geslo')

        if geslo == ponovno_geslo:
            Uporabnik.ustvari(ime=ime, priimek=priimek, email=email, original_geslo=geslo)
            return self.redirect_to('login')

# kontroler za  prijavo uporabnikov
class LoginHndler(BaseHandler):
     def get(self):
         return self.render_template('login.html')

     def post(self):
         email = self.request.get('email')
         geslo = self.request.get('geslo')
         uporabnik = Uporabnik.query(Uporabnik.email == email).get()
         if Uporabnik.preveri_geslo(original_geslo=geslo, uporabnik=uporabnik):
             return self.write('uporabnik je Logiran')
         else:
             return self.write('Uporabnik ni logirtan')
