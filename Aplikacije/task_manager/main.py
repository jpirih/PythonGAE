#!/usr/bin/env python
import os
import jinja2
import webapp2
import datetime
import cgi
from models import Task


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

# osnovna stran aplikacije
class MainHandler(BaseHandler):
    def get(self):
        seznam = Task.query(Task.izbrisan == False).fetch()
        params = {'seznam':seznam}
        return self.render_template("hello.html", params=params)

# dodajanje opravila

class VnosHandler(BaseHandler):
    def get(self):
        return self.render_template('vnos_opravila.html')

    def post(self):
        try:
            naloga = self.request.get('naloga')
            prioriteta = self.request.get('prioriteta')
            opis = self.request.get('opis')
            datum = self.request.get('termin')
            izvajalec = self.request.get('izvajalec')

            if datum == "":
                danes = datetime.datetime.now()
                termin_d = datetime.datetime.strftime(danes,'%d.%m.%Y %H:%M:%S')
                termin = datetime.datetime.strptime(termin_d, '%d.%m.%Y %H:%M:%S')
            else:
                termin = datetime.datetime.strptime(datum,'%d.%m.%Y %H:%M:%S')


            opravilo = Task(naloga=naloga, prioriteta=prioriteta, opis=opis, termin=termin, izvajalec=izvajalec)
            opravilo.put()
            return self.redirect_to('osnovna-stran')
        except ValueError:
            err = "Datum in ura obezno v formatu d.m.YYYY H:M:S Lahko pa je prazno"
            params = {'err':err}
            return self.render_template('vnos_opravila.html', params=params)

# kontroler za urejanje in zakljucevanje opravil
class UrediHandler(BaseHandler):
    def get(self, opravilo_id):
        opravilo = Task.get_by_id(int(opravilo_id))
        params = {'opravilo':opravilo}
        return self.render_template('podrobnosti_opravila.html', params=params)

    def post(self, opravilo_id):
        opravilo = Task.get_by_id(int(opravilo_id))
        finished = self.request.get('finished')
        opis = self.request.get('opis')
        opravilo.opis = opis

        if  finished == 'da':
            opravilo.finished = True
            opravilo.put()
        elif finished == 'x':
            opravilo.izbrisan = True
            opravilo.put()
        else:
            opravilo.put()

        return self.redirect_to('osnovna-stran')



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="osnovna-stran"),
    webapp2.Route('/dodaj-opravilo', VnosHandler),
    webapp2.Route('/opravilo/<opravilo_id:\d+>', UrediHandler)
], debug=True)


