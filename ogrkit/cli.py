#!/usr/bin/env python

import argparse
import sys

class OGRKitUtility(object):
    description = ''
    epilog = ''
    override_flags = ''

    def __init__(self, args=None, output_file=None):
        """
        Perform argument processing and other setup for a CSVKitUtility.
        """
        self._init_common_parser()
        self.add_arguments()
        self.args = self.argparser.parse_args(args)

        self._install_exception_handler()

        if output_file is None:
            self.output_file = sys.stdout
        else:
            self.output_file = output_file

    def add_arguments(self):
        """
        Called upon initialization once the parser for common arguments has been constructed.

        Should be overriden by individual utilities.
        """
        raise NotImplementedError('add_arguments must be provided by each subclass of CSVKitUtility.')

    def main(self):
        """
        Main loop of the utility.

        Should be overriden by individual utilities and explicitly called by the executing script.
        """
        raise NotImplementedError(' must be provided by each subclass of CSVKitUtility.')

    def _init_common_parser(self):
        """
        Prepare a base argparse argument parser so that flags are consistent across different shell command tools.
        If you want to constrain which common args are present, you can pass a string for 'omitflags'. Any argument
        whose single-letter form is contained in 'omitflags' will be left out of the configured parser. Use 'f' for 
        file.
        """
        self.argparser = argparse.ArgumentParser(description=self.description, epilog=self.epilog)
        
        self.argparser.add_argument('input', metavar='INPUT', type=str,
            help='The datasource to operate on.')
        self.argparser.add_argument('output', metavar='OUTPUT', type=str,
            help='The datasource to write to. Existing files will be deleted')

        if 'v' not in self.override_flags:
            self.argparser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                                help='Print detailed tracebacks when errors occur.')

    def _install_exception_handler(self):
        """
        Installs a replacement for sys.excepthook, which handles pretty-printing uncaught exceptions.
        """
        def handler(t, value, traceback):
            if self.args.verbose:
                sys.__excepthook__(t, value, traceback)
            else:
                print value

        sys.excepthook = handler
