#!/usr/bin/env python
import os
import jinja2
import webapp2
import datetime



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
        cas = datetime.datetime.strftime(datum, "%H:%M:%S")
        params = {'datum':danes,"cas":cas}
        return self.render_template("index.html",params=params)

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")


class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")


class ActivitiesHandler(BaseHandler):
    def get(self):
        return self.render_template("activities.html")


class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")


class ProjectsHandler(BaseHandler):
    def get(self):
        return self.render_template("projects.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/activities', ActivitiesHandler),
    webapp2.Route('/contact', ContactHandler),
    webapp2.Route('/projects', ProjectsHandler),
], debug=True)


