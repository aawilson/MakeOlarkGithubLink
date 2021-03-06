from __future__ import absolute_import, unicode_literals, print_function, division

import sys

"""This module collates the Git commands from the submodule

...it's a python 2 / 3 compatibility workaround, mostly.
"""

# Sublime doesn't reload submodules. This code is based on 1_reloader.py
# in Package Control, and handles that.

mod_prefix = 'make_olark_github_link'

# ST3 loads each package as a module, so it needs an extra prefix
if sys.version_info >= (3,):
    bare_mod_prefix = mod_prefix
    mod_prefix = 'MakeOlarkGithubLink.' + mod_prefix
    from imp import reload

mods_load_order = [
    '',
    '.command_thread',
    '.link_command',
]

reload_mods = []

for mod in sys.modules:
    if any([mod.startswith('make_olark_github_link'), mod.startswith('MakeOlarkGithubLink')]) and sys.modules[mod] is not None:
        reload_mods.append(mod)

reloaded = []

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
        reloaded.append(mod)

if reloaded:
    print("MakeOlarkGithubLink: reloaded submodules", reloaded)

# Now actually import all the commands so they'll be visible to Sublime
try:
    # Python 3
    from .make_olark_github_link.link_command import MakeOlarkGithubLink

except (ImportError, ValueError):
    # Python 2
    from make_olark_github_link.link_command import MakeOlarkGithubLink


__all__ = [
    MakeOlarkGithubLink,
]
