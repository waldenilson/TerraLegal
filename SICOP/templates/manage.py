#!/usr/bin/env python
import os
import sys

#sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'env','lib','site-packages'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
