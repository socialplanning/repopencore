"""
forked from
 https://svn.openplans.org/svn/build/openplans_hooks/
"""

def add_request_header(header_name, value, environ):
    environ[header_name] = value
    # make sure it propagates to subrequests
    if 'paste.recursive.include' in environ:
        orig = environ['paste.recursive.include'].original_environ
        orig[header_name] = value

import re

# XXX TODO: this regex is too permissive i think
_project_regex = re.compile(r'/projects/+([^/]+)')

def parse_project(environ):
    """
    For the main site, find the project name and put the
    /projects/PROJECTNAME portion of the path onto SCRIPT_NAME
    """
    path_info = environ.get('PATH_INFO', '')
    script_name = environ.get('SCRIPT_NAME', '')
    match = _project_regex.search(path_info)
    if match:
        script_name += match.group(0)
        project = match.group(1)

        # XXX TODO: no need for this here i think?
        #if not path_info[match.end():] and environ['REQUEST_METHOD'] in ('GET', 'HEAD'):
        #    # No trailing slash, i.e., "/project/foo"
        #    new_url = construct_url(environ, path_info=environ['PATH_INFO']+'/')
        #    raise httpexceptions.HTTPMovedPermanently(
        #        headers=[('Location', new_url)])

        path_info = '/' + path_info[match.end():].lstrip('/')
        return project, path_info, script_name
    return None, path_info, script_name

class App(object):
    def __init__(self, app, header):
        self.app = app
        self.header = header

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

def factory(loader, global_conf, **local_conf):
    default_app = local_conf['opencore']
    default_app = loader.get_app(default_app)
    default_app = App(default_app, '')

    tasktracker = local_conf['tasktracker']
    tasktracker = loader.get_app(tasktracker)

    from deliverance.middleware import DeliveranceMiddleware, FileRuleGetter
    tasktracker = DeliveranceMiddleware(tasktracker, FileRuleGetter('/home/egj/opencore/egj.openplans.org/builds/20081204/opencore/src/repopencore/deliverance.xml'))

    tasktracker = App(tasktracker, 'tasktracker')

    other_apps = [('/tasks', tasktracker)]
    return URLDispatcher(default_app,
                         *other_apps)

class URLDispatcher(object):
    def match_path_info(self, path_info, script_name):
        for path in self.apps:
            if path_info == path or path_info.startswith(path+'/'):
                script_name += path
                path_info = path_info[len(path):]
                assert not path_info or path_info.startswith('/')
                return (self.apps[path], path_info, script_name)

        return (False, path_info, script_name)

    def __init__(self, default_app, *apps):
        self.default_app = default_app
        self.apps = {}
        for path, app in apps:
            self.apps[path] = app

    def __call__(self, environ, start_response):
        project, new_path_info, new_script_name = parse_project(environ)
        if not project:
            return self.default_app(environ, start_response)

        add_request_header('HTTP_X_OPENPLANS_PROJECT', project, environ)

        app_to_dispatch_to, new_path_info, new_script_name = \
            self.match_path_info(new_path_info, new_script_name)
        if not app_to_dispatch_to:
            return self.default_app(environ, start_response)

        environ['PATH_INFO'], environ['SCRIPT_NAME'] = (
            new_path_info, new_script_name)

        # XXX TODO: look up what uses this, and, where, and how, and why, 
        #           and what it should look like
        if not environ.has_key('HTTP_X_OPENPLANS_APPLICATION'):
            add_request_header('HTTP_X_OPENPLANS_APPLICATION',
                               app_to_dispatch_to.header,
                               environ)

        return app_to_dispatch_to(environ, start_response)
