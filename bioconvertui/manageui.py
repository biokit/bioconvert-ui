#!/usr/bin/env python
import os
import sys
import time
import webbrowser
from urllib import request
from urllib.error import URLError

import bioconvertui
from importlib import reload
from threading import Thread


class OpenWhenReady(Thread):

    def __init__(self, delay, url):
        Thread.__init__(self)
        self.delay = delay
        self.url = url

    def run(self):
        failed = True
        while failed:
            try:
                request.urlopen(self.url)
                webbrowser.open(self.url)
                time.sleep(self.delay)
                failed = False
            except URLError:
                pass


def main(argv=None):
    if (argv is None):
        argv = sys.argv
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, BASE_DIR)
    reload(bioconvertui)
    # os.environ.setdefault("PYTHONPATH", os.path.dirname(BASE_DIR)+':'+BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioconvertui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    port = argv[2] if len(argv) == 3 and argv[1] == "-p" else "8090"
    url = "127.0.0.1:%s" % port
    OpenWhenReady(delay=0.1, url="http://%s/" % url).start()
    execute_from_command_line([argv[0], "migrate", "--noinput", "-v", "0"])
    execute_from_command_line([argv[0], "collectstatic", "--noinput", "-v", "0"])
    execute_from_command_line([argv[0], "runserver", url, "--noreload", "--insecure", "-v", "0"])


if __name__ == "__main__":
    main()
