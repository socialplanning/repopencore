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
    
