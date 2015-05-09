#!/usr/bin/env python

import web
from jinja2 import Environment, FileSystemLoader
from fitparse import Activity
import json
import glob
import os
import string

fit_files_path = '/app/data'
template_path = '/app/templates'

urls = (
    '/', 'list_files',
    '/file/(.*)', 'get_file',
    '/gmaphtml/(.*)', 'gmaphtml',
)

app = web.application(urls, globals())


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)


def get_fit_files():
    files = glob.glob('%s/*fit' % (fit_files_path))
    ret = [os.path.basename(f) for f in files]
    return sorted(ret)

records_cache = {}
template_cache = {}


def get_records(f):
    filename = '%s/%s' % (fit_files_path, f)
    activity = Activity(filename)
    activity.parse()
    records = activity.get_records_by_type('record')
    return records


def read_template(name):
    if template_cache.has_key(name):
        return template_cache[name]
    filename = '%s/%s.html' % (template_path, name)
    f = open(filename, 'r')
    d = f.read()
    f.close()
    template_cache[name] = d
    return d


def get_parsed_records(f):
    records = get_records(f)
    ret = []
    num = 0
    first_runtime = None
    for r in records:
        if num == 0:
            first_runtime = r.get_data('timestamp')
        d = {}
        valid_field_names = r.get_valid_field_names()
        for f in valid_field_names:
            fd = r.get_data(f)
            d[f] = fd
            if f == 'timestamp':
                d['runtime'] = int((fd - first_runtime).total_seconds())
                d[f] = str(fd)
        d['record'] = num
        num += 1
        ret.append(d)
    return ret


def gmap_data(filename):
    name_map = {'position_long': 'lng', 'position_lat': 'lat'}
    records = get_records(filename)
    ret = []
    for r in records:
        d = {}
        d2 = {'lat': None, 'lng': None}
        valid_field_names = r.get_valid_field_names()
        for f in valid_field_names:
            d[f] = r.get_data(f)
        for k, v in name_map.iteritems():
            if d.has_key(k):
                d2[v] = float(d[k]) / (2 ** 31 / 180)
        if d2['lat'] == None or d2['lng'] == None:
            continue
        ret.append(d2)
    # r2 = {'lines':[{"colour":"#FF0000", "width":2, "points": ret }]}
    # return r2
    return ret


def gmap_first_record(filename):
    g = gmap_data(filename)
    lat_default = 60.2050000
    long_default = 24.736000
    if len(g) > 0:
        return [g[0]['lat'], g[0]['lng']]
    return [lat_default, long_default]


def check_valid_file(filename):
    all_files = get_fit_files()
    if not filename in all_files:
        raise web.notfound()


class list_files:

    def GET(self):
        return render_template('files.html', files=get_fit_files(),)


class get_file:

    def GET(self, filename):
        all_files = get_fit_files()
        if not filename in all_files:
            raise web.notfound()
        web.header('Content-Type', 'application/json')
        return json.dumps(get_parsed_records(filename), indent=2)


class gmaphtml:

    def GET(self, filename):
        check_valid_file(filename)
        t = read_template('gmap')
        d = gmap_first_record(filename)
        points = []
        for p in gmap_data(filename):
            js = """new google.maps.LatLng(%s, %s)""" % (p['lat'], p['lng'])
            points.append(js)

        data = {'gmap_start_point_lat': d[0], 'gmap_start_point_lng': d[
            1], 'filename': '/gmap/%s' % filename, 'data': string.join(points, ',')}
        return t % data


if __name__ == "__main__":
    app.run()
