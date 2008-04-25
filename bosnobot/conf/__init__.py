"""
Settings and configuration for bosnobot. This is based heavily on django.conf.
"""
import os

from bosnobot.conf import global_settings

ENVIRON_VARIABLE = "BOSNOBOT_SETTINGS_MODULE"

class LazySettings(object):
    def __init__(self):
        self._target = None
    
    def __getattr__(self, name):
        if self._target is None:
            self._import_settings()
        return getattr(self._target, name)
    
    def _import_settings(self):
        try:
            settings_module = os.environ[ENVIRON_VARIABLE]
            if not settings_module:
                raise KeyError
        except KeyError:
            raise ImportError("settings cannot be imported.")
        self._target = Settings(settings_module)

class Settings(object):
    def __init__(self, settings_module):
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))
        self.SETTINGS_MODULE = settings_module
        try:
            mod = __import__(self.SETTINGS_MODULE, {}, {}, [""])
        except ImportError, e:
            raise ImportError, "Could not import settings '%s': %s" % (self.SETTINGS_MODULE, e)
        for setting in dir(mod):
            if setting == setting.upper():
                setattr(self, setting, getattr(mod, setting))

settings = LazySettings()
