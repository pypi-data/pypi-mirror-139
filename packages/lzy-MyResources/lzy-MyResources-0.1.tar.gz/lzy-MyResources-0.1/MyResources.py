import os
import sys


def MyResources(resources_path, resources_file='resources',Slash=False):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('')
    if Slash:
        return F"/".join(os.path.join(base_path, os.path.join(resources_file, resources_path)).split('\\'))
    else:
        return os.path.join(base_path, os.path.join(resources_file, resources_path))