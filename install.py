#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import os
import tempfile
from subprocess import Popen, PIPE
from optparse import OptionParser
from ConfigParser import SafeConfigParser
import logging

log = logging.getLogger('dotfiles_installer')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Installer(object):

    def __init__(self,
                 config_file="",
                 src_folder="",
                 backup_dir="",
                 replace_existing=True,
                 dryrun=False):
        """Initializes

        :param config_file: (str)
        :param src_folder: (str)
        :param backup_dir: (str)
        :param replace_existing: (bool)
        """
        self.config_file = os.path.abspath(config_file)
        self.src_folder = (os.path.abspath(src_folder) if src_folder
                           else os.path.normpath(
                               os.path.join(os.path.dirname(self.config_file),
                                            '../dotfiles')))
        self.backup_dir = (os.path.abspath(backup_dir) if backup_dir
                           else tempfile.mkdtemp())
        self.replace_existing = replace_existing
        self.conf = SafeConfigParser()
        self.conf.read(config_file)
        self.dryrun = dryrun

    def install_environment(self, env_file):
        env = SafeConfigParser()
        if not env.read(env_file):
            raise ValueError("Failed to read env config '%s'" % env_file)
        if self.replace_existing:
            log.warning("we will backup into %s" % self.backup_dir)
        for p, ok in env.items('install'):
            if ok:
                self.install_section(p)

    def install_section(self, section):
        """Install given section
        """
        path = os.path.normpath(os.path.abspath(
            os.path.join(self.src_folder, section)))

        for src, dest in self.conf.items(section):
            self.install_file(path, src, dest)
        return True

    def install_file(self, path, src, dest):
        """Install given file (src) to dest. If something already exists,
        backup it to self.backup_dir
        """
        cmd = "for f in {path}/{src} ; do echo {dest} ; done"
        cmd = cmd.format(path=path,
                         src=src,
                         dest=dest.replace('*', '`basename $f`'))
        p = Popen(cmd, shell=True, stdout=PIPE)
        dests = p.stdout.read().split()
        for d in dests:
            if os.path.exists(d):
                if self.replace_existing:
                    self.backup_file(d)
                else:
                    raise ValueError("%s already existing" % d)
        self.new_link(path, src, dest)
        return True

    def new_link(self, path, src, dest):
        """Make a new link in dest, pointing to src
        """
        cmd = "for f in {path}/{src} ; do ln -s $f {dest} ; done"
        cmd = cmd.format(path=path,
                         src=src,
                         dest=dest.replace('*', '`basename $f`'))
        log.debug(cmd)
        if not self.dryrun:
            p = Popen(cmd, shell=True)
            p.wait()
        return True

    def backup_file(self, path):
        """Backup given path (about to be replaced) to the given backup dir
        """
        cmd = "mv {path} {backup_path}"
        cmd = cmd.format(path=path, backup_path=self.backup_dir)
        log.debug(cmd)
        if not self.dryrun:
            p = Popen(cmd, shell=True)
            p.wait()
        return True


def parse_options():
    """Parse options from command line
    """
    parser = OptionParser(usage="%prog [options]")
    parser.add_option('-c', '--conf',
                      default="",
                      help="Installation configuration file (where to install things)")
    parser.add_option('-e', '--env',
                      default="",
                      help="Environment configuration file (what to install)")
    parser.add_option('-b', '--backup',
                      default="",
                      help="Backup directory")
    parser.add_option('-r', '--replace',
                      action='store_true',
                      help="Should we replace existing paths?")
    parser.add_option('-d', '--dryrun',
                      action='store_true',
                      help="Don't execute commands")
    return parser.parse_args()


def main():
    """Main function
    """
    options, args = parse_options()

    installer = Installer(options.conf,
                          src_folder="",
                          backup_dir=options.backup,
                          replace_existing=options.replace,
                          dryrun=options.dryrun)
    installer.install_environment(options.env)


if __name__ == '__main__':
    main()

#EOF
