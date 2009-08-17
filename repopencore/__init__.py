def install_myghty_fork():
    import subprocess
    return subprocess.call(['easy_install',
                            'http://svn.sccs.swarthmore.edu/egj/myghty_import_hack'])

def install_tasktracker():
    import subprocess
    return subprocess.call([
            'easy_install',
            'https://svn.openplans.org/svn/TaskTracker/trunk'])

def start_server():
    """
    runs a Paste server within a zopectl shell
    """
    import sys
    zopectl, args = sys.argv[1], sys.argv[2:]

    import subprocess
    return subprocess.call([zopectl, 'shell', 'paster', 'serve'] + args)

def make_config(args=None):
    """
    generates a Paste configuration file for running opencore, and prints it to STDOUT
    """
    if args is None:
        import sys
        args = sys.argv[1:]

    if len(args) < 2 or args[0] == "--help":
        print "usage: mkopencoreconfig SERVER_PORT ZOPE_CONF_LOCATION"
        return 1

    server_port, zope_conf = args[0], args[1]

    if not zope_conf.startswith('/'):
        import os
        zope_conf = os.getcwd() + os.sep + zope_conf

    from pkg_resources import resource_filename

    ini_tmpl = resource_filename('repopencore', 'opencore.ini_tmpl')

    ini_tmpl = open(ini_tmpl).read()
    ini_tmpl = ini_tmpl % locals()

    print ini_tmpl
    
def make_config_with_tt(args=None):
    """
    generates a Paste configuration file for running opencore, and prints it to STDOUT
    """
    if args is None:
        import sys
        args = sys.argv[1:]

    if len(args) < 2 or args[0] == "--help":
        print "usage: mkopencoreconfig SERVER_PORT ZOPE_CONF_LOCATION SHARED_SECRET_FILEPATH ADMIN_INFO_FILEPATH BASE_DIR"
        return 1

    server_port, zope_conf, \
        shared_secret_file, admin_info_file, here = \
        args[0:5]

    if not zope_conf.startswith('/'):
        import os
        zope_conf = os.getcwd() + os.sep + zope_conf
    if not shared_secret_file.startswith('/'):
        import os
        shared_secret_file = os.getcwd() + os.sep + shared_secret_file
    if not admin_info_file.startswith('/'):
        import os
        admin_info_file = os.getcwd() + os.sep + admin_info_file
    if not here.startswith('/'):
        import os
        here = os.getcwd() + os.sep + here

    from pkg_resources import resource_filename

    ini_tmpl = resource_filename('repopencore', 'opencore_with_tt.ini_tmpl')

    percent = "%"  # need to get a '%' into the resulting paste template

    ini_tmpl = open(ini_tmpl).read()
    ini_tmpl = ini_tmpl % locals()

    print ini_tmpl
    
