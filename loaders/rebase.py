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
