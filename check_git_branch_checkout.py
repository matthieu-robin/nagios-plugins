#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2016-07-25 14:57:36 +0100 (Mon, 25 Jul 2016)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check a Git working copy is in the right branch.

Port of Perl version originally written for puppetmasters to make sure prod
and staging environment dirs had the right branches checked out in them

See also check_git_branch_checkout.pl

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import os
import re
import sys
import traceback
import git
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import qquit, log_option, validate_directory
    from harisekhon import NagiosPlugin
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.1'


class CheckGitBranchCheckout(NagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckGitBranchCheckout, self).__init__()
        # Python 3.x
        # super().__init__()

    def add_options(self):
        self.add_opt('-d', '--directory', action='store', help='Directory path to git working copy')
        self.add_opt('-b', '--branch', action='store', help='Branch to expect working copy checkout to be')

    def run(self):
        self.no_args()
        directory = self.get_opt('directory')
        directory = os.path.abspath(directory)
        expected_branch = self.get_opt('branch')
        validate_directory(directory)
        if expected_branch is None:
            self.usage('expected branch not defined')
        if not re.match(r'^[\w-]+$', expected_branch):
            self.usage('Invalid branch name given, must be alphanumeric')
        log_option('expected branch', expected_branch)
        repo = git.Repo(directory)
        current_branch = repo.active_branch.name
        if current_branch == expected_branch:
            qquit('OK', "branch '{0}' currently checked out in directory '{1}'"
                  .format(current_branch, directory))
        else:
            qquit('CRITICAL', "branch '{0}' checked out, expecting '{1}' in directory '{2}'"
                  .format(current_branch, expected_branch, directory))


if __name__ == '__main__':
    CheckGitBranchCheckout().main()