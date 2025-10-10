"""
Settings and configuration for Xodex.

- Reads from XODEX_SETTINGS_MODULE environment variable.
- Supports dynamic and manual configuration, validation, and runtime overrides.
- Caches settings for fast access.
- Provides explicit settings tracking and validation utilities.
- Supports reloading and resetting configuration at runtime.
- Warns on missing or invalid settings.
- Singleton pattern ensures only one configuration instance.

Usage:
    from xodex.conf import settings
"""

import importlib
import os
import warnings

from xodex.conf import xsettings
from xodex.core.exceptions import ImproperlyConfigured
from xodex.utils.singleton import Singleton

ENVIRONMENT_VARIABLE = "XODEX_SETTINGS_MODULE"


class Settings:
    """Holder for user configured settings."""

    SETTINGS_MODULE = None

    def __init__(self, settings_module):
        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module
        self._explicit_settings = set()

        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(xsettings):
            if setting.isupper():
                setattr(self, setting, getattr(xsettings, setting))

        module = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = ("SUPPORTED_LANGUAGES", "WINDOW_SIZE")
        dict_settings = ("CUSTOM_SETTINGS", "KEY_BINDINGS", "LOGGING")

        for setting in dir(module):
            if setting.isupper():
                setting_value = getattr(module, setting)
                if setting in tuple_settings and not isinstance(setting_value, (list, tuple)):
                    warnings.warn(
                        f"The {setting} setting must be a list or a tuple.",
                        stacklevel=2,
                    )
                    continue
                if setting in dict_settings and not isinstance(setting_value, dict):
                    warnings.warn(f"The {setting} setting must be a dict.", stacklevel=2)
                    continue
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return f"<Settings '{self.SETTINGS_MODULE}'>"


class Configuration(Singleton):
    """
    Xodex Configuration Singleton

    Loads settings from a Python module specified by the XODEX_SETTINGS_MODULE
    environment variable, or from the default configuration module. Supports
    runtime overrides, validation, and explicit settings tracking.
    """

    def __init__(self):
        super().__init__()
        self._settings = None

    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time settings are needed, if the user hasn't
        configured settings manually.
        """
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise ImproperlyConfigured("Settings are not configured")

        self._settings = Settings(settings_module)

    def __repr__(self):
        return f"<Configuration '{self.settings_module}'>"

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self._settings_cache."""
        if (_settings := self._settings) is object:
            self._setup(name)
            _settings = self._settings
        value = getattr(_settings, name)
        self.__dict__[name] = value
        return value

    def __setattr__(self, name, value):
        """Set the value of a setting and cache it in self._settings_cache."""
        if name == "_settings":
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete a setting and clear it from cache if needed."""
        super().__delattr__(name)
        self.__dict__.pop(name, None)

    @property
    def configured(self):
        """Return True if the settings have already been configured."""
        return self._settings is not None

    def configure(self, default_settings=xsettings, **options):
        """
        Manually configure the settings at runtime.

        Args:
            **options: Setting names and values to override.
        """
        if self._settings:
            raise RuntimeError("Settings already configured.")
        settings = Settings(default_settings)
        for name, value in options.items():
            if not name.isupper():
                raise TypeError(f"Setting {name} must be uppercase.")
            setattr(settings, name, value)
        self._settings = settings


settings = Configuration()
