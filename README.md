A dead-simple plugin to make a github link. Adds a command to the palette called Make Olark Github Link, which when executed will show you the generated link and let you copy it to your clipboard.

## TO USE THIS

1. Clone this into your Sublime local packages directory. You can find it through Preferences -> Browse Packages in Sublime.
2. In the link_command.py, change `projdir = "olark\\projects\\"` into whatever string uniquely identifies your projects directory (the level just above the actual git repos). It'd be relatively easy for me to just get this from git, probably, I just haven't yet.
3. There will be a command added to your palette and to the available commands. You can either use it directly from the palette (`ctrl/command + shift + P`, "Make Olark Github Link"), or bind it to a key (Preferences -> Key Bindings (User), make a JSON array if it doesn't exist already, then add `{ "keys": ["<some command sequence>"], "command": "make_olark_github_link" }` as an item in that array.

## TODO

1. Remove all the stuff from the GitCommand code I copypasta'd that isn't actually used in this project.
2. Make it intelligent about finding the project directory.
