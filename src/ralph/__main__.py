#!/usr/bin/env python
import os
import sys

def ubuntu_1020872_workaround():
    """Workaround for spurious "Error opening file for reading: Permission
    denied" printed to stderr while importing _imaging due to libjpeg not being
    able to open /proc/self/auxv on a setcapped `python` process. Reported as
    Ubuntu bug https://bugs.launchpad.net/libjpeg-turbo/+bug/1020872.
    """
    os.dup2(2, 3)
    stderr = os.fdopen(2, 'a')
    stderr.close()
    e = None
    try:
        import _imaging
    except Exception as e:
        pass
    finally:
        os.dup2(3, 2)
        sys.__stderr__ = sys.stderr = os.fdopen(2, 'a')
    if e:
        raise e

def main():
    if sys.platform.startswith('linux'):
        ubuntu_1020872_workaround()

    os.environ["DJANGO_SETTINGS_MODULE"] = "ralph.settings"

    from django.core.management import execute_from_command_line

    sys.argv[0] = os.path.dirname(__file__)
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
