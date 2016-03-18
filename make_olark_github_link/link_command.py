from __future__ import absolute_import, unicode_literals, print_function, division

import os

import sublime_plugin
import sublime

from .command_thread import GitTextCommand

OLARK_GITHUB_PREFIX = "https://github.com/olark"


def _do_nothing():
    pass


def _split_with_ambiguous_pathsep(path):
    folders = []

    while True:
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break

    folders.reverse()

    # os.path.split preserves the \ or / in a windows root path, which we're not interested in
    #  for comparative purposes
    if ':' in folders[0]:
        folders[0] = folders[0][:-1]

    return folders


def _path_parts_without_prefix(path, prefix):
    # Try with foreslash pathsep first, because it's not a legal character in Windows paths
    normalized_prefix_parts = _split_with_ambiguous_pathsep(prefix)
    normalized_path_parts = _split_with_ambiguous_pathsep(path)

    if len(normalized_prefix_parts) <= 1:
        return normalized_prefix_parts

    last_folder = normalized_prefix_parts[-1]
    normalized_pathsep_path = '/'.join(normalized_path_parts)
    normalized_pathsep_prefix = '/'.join(normalized_prefix_parts + [''])

    if len(prefix) > len(path):
        raise ValueError('Prefix was longer than path: %s %s' % (path, prefix))

    return [last_folder] + normalized_pathsep_path[len(normalized_pathsep_prefix):].split('/')


class MakeOlarkGithubLink(GitTextCommand, sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view:
            return

        file_name = self.view.file_name()

        path_callback = self.make_path_callback(file_name)

        self.run_command(['git', 'rev-parse', '--show-toplevel'], path_callback)

    def make_path_callback(self, file_name):
        def remove_prefix_from_path(result):
            result = result.strip()
            if result.startswith('fatal'):
                self.view.window().show_quick_panel(
                    ['(you do not appear to be in a git project)'],
                    _do_nothing,
                    0,
                    0,
                    )
                return

            parts = _path_parts_without_prefix(file_name, result)

            rev_parse_callback = self.make_rev_parse_callback(parts)

            self.run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], rev_parse_callback)

        return remove_prefix_from_path

    def make_rev_parse_callback(self, parts):
        def git_command_done(result):
            result = result.strip()

            if result == "HEAD":
                self.run_command(['git', 'rev-parse', 'HEAD'], git_command_done)

                return

            github_path = '/'.join([OLARK_GITHUB_PREFIX, parts[0], 'blob', result] + parts[1:])

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

        return git_command_done
