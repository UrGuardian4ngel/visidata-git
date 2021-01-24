from visidata import *
from enum import Enum

__all__ = ['open_git_rebase_todo', 'RebaseTodoSheet']


@VisiData.api
def open_git_rebase_todo(vd, p):
    return RebaseTodoSheet(p.name, source=p)


class RebaseTodoSheet(TableSheet):
    rowtype = 'commits'  # rowdef: Commit
    columns = [
        ColumnAttr('command'),  # TODO: Replace with enum.
        ColumnAttr('commit', width=9),
        ColumnAttr('message'),
    ]
    nKeys = 1

    def iterload(self):
        for line in self.source:
            # Ignore blank lines and comments
            if not line or line.startswith('#'):
                continue

            yield Commit.from_line(line)

    @property
    def command_choices(self):
        return [
            {'key': 'pick', 'desc': 'use commit'},
            {'key': 'reword', 'desc': 'use commit, but edit the commit message'},
            {'key': 'edit', 'desc': 'use commit, but stop for amending'},
            {'key': 'squash', 'desc': 'use commit, but meld into previous commit'},
            {'key': 'fixup', 'desc': 'like "squash", but discard this commit\'s log message'},
            {'key': 'exec',
                'desc': 'run command (the rest of the line) using shell'},
            {'key': 'break',
                'desc': 'stop here (continue rebase later with "git rebase --continue")'},
            {'key': 'drop', 'desc': 'remove commit'},
            {'key': 'label', 'desc': 'label current HEAD with a name'},
            {'key': 'reset', 'desc': 'reset HEAD to a label'},
            {'key': 'merge', 'desc': 'create a merge commit using the original merge commit''s message'},
        ]


RebaseTodoSheet.addCommand('x', 'set-command',
                           'cursorCol.setValuesTyped(selectedRows or [cursorRow], chooseOne(command_choices))',
                           'cycle through available commands')


class Commit(object):
    commit = ''
    message = ''
    command = ''

    def __init__(self, commit, message, command):
        self.commit = commit
        self.message = message
        self.command = command

    @staticmethod
    def from_line(line):
        command, commit, message = line.split(' ', 2)
        return Commit(commit, message, command)
