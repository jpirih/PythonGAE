#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import datetime
from gl_mesto_handlers import *
from forenzik_logika import *
import random
from models import GuestBook
import re

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
        except ValueError:
            params = {"vnos_err":vnos_error}
            return self.render_template("skrito_stevilo.html", params=params)

# kontroler za aplikacijo  ugani glavno mesto   objekt in funcije so v
# datoteki gl_mesto_handlers.py

class PrestolnicaHandler(BaseHandler):
    def get(self):
        city = random.choice(seznam)
        mesto = city.ime
        drzava = city.drzava
        slika = city.slika

        params ={"mesto":mesto,"drzava":drzava, "img":slika}
        return self.render_template("gl_mesto.html",params=params)

    def post(self):
        vneseno_mesto = self.request.get("vnos_mesto")
        vneseno_mesto = vneseno_mesto.lower()
        izbrano_mesto = self.request.get("mesto")

        # spremenljivke za parametre
        bravo = ""
        napaka = ""

        if checkAnswer(izbrano_mesto,vneseno_mesto):
            bravo = "Res je"
        else:
            napaka = " Napaka !!"

        slika = "/assets/img/kekec.JPG"
        slika_narobe = "/assets/img/klicaj.jpg"
        parametri = {"pravilno":bravo, "narobe":napaka, "img_prav": slika, "img_narobe": slika_narobe}
        return self.render_template("gl_mesto.html", params=parametri)

# Kontroler za aplikacijo Forenzik
class ForenzikHandler(BaseHandler):
    def get(self):

        return self.render_template("forenzik.html")
# funkcija preveri katere lastnosti vsebuje dna - vnesen v obrazec

    def post(self):
        dna = self.request.get("vnos_dna").upper()
        # seznam_vseh_lastnosti import iz forenzik_logika.py
        lastnosti = seznam_vseh_lastnosti

        lastnosti_cloveka = []

        for lastnost in lastnosti:
            if lastnost in dna:
                lastnosti_cloveka.append(lastnosti[lastnost])

        params = {"lastnosti":lastnosti_cloveka}
        return self.render_template("forenzik.html", params=params)

# -------------- KNJIGA GOSTOV ------------

# Kontroler za GuestBook aplikacijo
class GuestBookHndler(BaseHandler):
    def get(self):
        return  self.render_template("guest_book.html")

# Pregled vnesenih podatkov in shranjevanje v Bazo
class GuestBookVnosHandler(BaseHandler):
    err = ""
    def post(self):
        ime = self.request.get("ime")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")


        msg= GuestBook(ime=ime, email=email, sporocilo=sporocilo)
        params = {'msg':msg}

        # preveri ali je vneseno polje ime in sporocilo
        if (msg.ime ==  "") and not (msg.sporocilo == "" or msg.sporocilo[0] == " "):
            msg.ime = "Neznanec"
            msg.put()
            return self.render_template("vnos.html", params=params)
        elif msg.sporocilo ==  "" or msg.sporocilo[0] == " ":
            err = "Vnos sporocila je obvezen!"
            params= {"err": err}
            return  self.render_template("guest_book.html", params=params)
        else:
            msg.put()
            return self.render_template("vnos.html", params=params)

# Kontroler seznam vnosov
class SeznamVsehVnosovHnadler(BaseHandler):
    def get(self):
        seznam = GuestBook.query().fetch()
        params = {"seznam":seznam}
        return self.render_template("pregled.html", params=params)





