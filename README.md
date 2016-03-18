A dead-simple plugin to make a github link. Adds a command to the palette called Make Olark Github Link, which when executed will show you the generated link and let you copy it to your clipboard.

## TO USE THIS

1. Clone this into your Sublime local packages directory. You can find it through Preferences -> Browse Packages in Sublime.
2. There will be a command added to your palette and to the available commands. You can either use it directly from the palette (`ctrl/command + shift + P`, "Make Olark Github Link"), or bind it to a key (Preferences -> Key Bindings (User), make a JSON array if it doesn't exist already, then add `{ "keys": ["<some command sequence>"], "command": "make_olark_github_link" }` as an item in that array. It should be decently smart about detecting whether you're in a git repo or no.

## TODO

1. Remove all the stuff from the GitCommand code I copypasta'd that isn't actually used in this project.
2. Make it so this will generate a link to any repo, or multiple origins (with some massaging if those other origins can't be assumed to have http endpoint links)
