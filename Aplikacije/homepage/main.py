#!/usr/bin/env python

import os
import jinja2
import webapp2
import datetime
from gl_mesto_handlers import *
import random

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

# Kontroler za kalkulator
class KalkulatorHandler(BaseHandler):
    def get(self):
        return self.render_template("kalkulator.html")

    def post(self):
        err_msg = "Obvezen je vnos stevil in operacije \n Pazi pa Deljenje z 0 ni dovoljeno"
        params = {"deljenje_err":err_msg}
        try:
            num1 = float(self.request.get("stevilo1"))
            num2 = float(self.request.get("stevilo2"))
            operacija = self.request.get("operacija")

            if operacija == "+":
                rezultat = num1 + num2
            elif operacija == "-":
                rezultat = num1 - num2
            elif operacija == "*":
                rezultat = num1 * num2
            elif operacija == "/":
                rezultat = num1 / num2
            params = {"rezultat":rezultat}
            return self.render_template("kalkulator.html", params=params)
        except:
            return self.render_template("kalkulator.html", params=params)

# Kontroler za pretvornik enot
class PretvornikHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")

    def post(self):
        err_msg = "Pazi v vnosno polje bvezno vnesi stevilo, namesto decimalne veijice uporabi piko ."
        params = {"err":err_msg}
        try:
            number = float(self.request.get("vrednost"))
            pretvorba = self.request.get("nacin_pretvorbe")

            if pretvorba == "m-cm":
                 izracun = number * 100
                 opis = "Pretvorba vrednosti %.2f  metrov  v centimetre znese:" %number
            elif pretvorba == "cm-m":
                 izracun = number *0.01
                 opis = "Pretvorba vrednosti %.2f  centimetrov v metre znese:" %number
            elif pretvorba == "km-milja":
                 izracun = number * 0.621371
                 opis = "Pretvorba vrednosti %.2f  kilometrov v  milje znese:" %number
            elif pretvorba == "h-min":
                izracun = number * 60
                opis = "Pretvorba vrednosti %.2f  ur v  minute znese:" %number
            elif pretvorba == "h-s":
                izracun = number * 3600
                opis = "Pretvorba vrednosti %.2f  ur v  sekunde znese:" %number
            elif pretvorba == "s-h":
                izracun = number *0.000278
                opis = "Pretvorba vrednosti %.2f  s v  ure znese:" %number
            elif pretvorba == "kmh-ms":
                izracun = number * 0.277778
                opis = "Pretvorba vrednosti %.2f  km/h v  m/s znese:" %number

            izracun = round(izracun,2)
            params = {"izracun":izracun, "opis":opis}
            return self.render_template("pretvornik.html", params=params)
        except:
            return self.render_template("pretvornik.html", params=params)

# Kontroler skrito stevilo aplikacija
class SteviloHandler(BaseHandler):
    def get(self):
        return self.render_template("skrito_stevilo.html")

    def post(self):
        vnos_error = "Obvezno vnesi stevilo preden pritisnes gumb!"
        try:
            vneseno_stevilo = int(self.request.get("vnos_stevilo"))
            skrito_stevilo = 25  # najbolj skrito stevilo

            # spremnljivke za parametre
            sporocilo = ""
            bravo = ""

            if vneseno_stevilo == skrito_stevilo:
                bravo = "Bravo uganil si skrito stevilo"
            else:
                sporocilo = "Napaka! Poskusi ponovno "

            params = {"message":sporocilo, "bravo":bravo}
            return self.render_template("skrito_stevilo.html", params=params)
        except:
            params = {"vnos_err":vnos_error}
            if ValueError:
                return self.render_template("skrito_stevilo.html", params=params)

# kontroler za aplikacijo  ugani glavno mesto   objekt in funcije so v
# datoteki gl_mesto_handlers.py

class PrestolnicaHandler(BaseHandler, GlavnoMesto):
    def get(self):
        city = random.choice(seznam)
        mesto = city.ime
        drzava = city.drzava
        slika = city.slika

        params ={"mesto":mesto,"drzava":drzava, "img":slika}
        return self.render_template("gl_mesto.html",params=params)

    def post(self):
        vnos = self.request.get("vnos_mesto")


# Route - navigacija po spletnem mestu
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/activities', ActivitiesHandler),
    webapp2.Route('/contact', ContactHandler),
    webapp2.Route('/projects', ProjectsHandler),
    webapp2.Route('/projects/kalkulator', KalkulatorHandler),
    webapp2.Route('/projects/pretvornik', PretvornikHandler),
    webapp2.Route('/projects/stevilo', SteviloHandler),
    webapp2.Route('/projects/prestolnica',PrestolnicaHandler),

], debug=True)





