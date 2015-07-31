#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import abc


class Plugin(metaclass=abc.ABCMeta):
    """
    Interface to which all "exported" MemoryOracle "runner side"
    plugins must abide.
    """

    @classmethod
    def plugin_depends_on(cls, depends):
        """
        Mark this Plugin as a dependency of the Plugin
        depends.

        The depends argument can be an iterator of dependencies or
        a single dependency.
        """
        pass

    @staticmethod
    def plugin_initialize():
        """
        Do whatever startup is required for this plugin to be available to
        users as instances.
        """
        pass
#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import memoryoracle.runner.plugin.interface


class LauncherPlugin(metaclass=abstract_python_plugin_system.Plugin):
    """
    Interface to which all Launcher plugins must abide.
    """
    pass
#!/usr/bin/env python
# -*- encoding UTF-8 -*-


import memoryoracle.runner.plugin.master.interface


class InferiorPlugin(metaclass=abstract_python_plugin_system.Plugin):
    """
    Interface to which all Inferior plugins must abide.
    """
    pass


