from __future__ import absolute_import, unicode_literals, print_function, division

import os

import sublime_plugin
import sublime

from .command_thread import GitTextCommand

OLARK_GITHUB_PREFIX = "https://github.com/olark"


class MakeOlarkGithubLink(GitTextCommand, sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()

        projdir = "olark\\projects\\"
        if projdir not in file_name:
            return

        split_path = file_name[file_name.find(projdir) + len(projdir):].split(os.path.sep)

        def git_command_done(result):
            if result == "HEAD":
                self.run_command(['git', 'rev-parse', 'HEAD'], git_command_done)

                return

            github_path = '/'.join([OLARK_GITHUB_PREFIX, split_path[0], 'blob', result] + split_path[1:])

            current_selection = self.view.sel()[0]
            if current_selection.size():
                row1, _ = self.view.rowcol(current_selection.begin())
                row2, _ = self.view.rowcol(current_selection.end())

                if row1 == row2:
                    github_path += "#L%d" % row1
                else:
                    github_path += "#L%d-L%d" % (row1, row2)

            items = [[
                github_path,
                "Click to copy this to the clipboard"
            ]]

            def copy_to_cc(idx):
                if idx != -1:
                    sublime.set_clipboard(items[idx][0])

            self.view.window().show_quick_panel(
                items,
                copy_to_cc,
                sublime.MONOSPACE_FONT,
                0,
                )

        self.run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], git_command_done)
