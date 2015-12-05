#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from site_handlers import *
from app_handlers import *


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
    webapp2.Route('/projects/forenzik', ForenzikHandler),
    webapp2.Route('/projects/guest-book', GuestBookHndler),
    webapp2.Route('/projects/guest-book/pregled', GuestBookVnosHandler),
    webapp2.Route('/projects/guest-book/pregled-vseh', SeznamVsehVnosovHnadler),

], debug=True)





