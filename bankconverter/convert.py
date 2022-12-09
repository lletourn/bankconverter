#!/usr/local/bin/python2.7
# encoding: utf-8
'''
convert -- shortdesc

convert is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import accesd
import datetime
import rbc
import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2016-06-27'
__updated__ = '2016-06-27'

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--date", dest="start_date", help="start date [default: %(default)s]")
        parser.add_argument("-b", "--bank", dest="bank_type", help="bank type[default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="files", help="files to folder(s) with source file(s) [default: %(default)s]", metavar="file", nargs='+')

        # Process arguments
        args = parser.parse_args()

        files = args.files
        start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")

        bank = None
        if(args.bank_type == "accesd"):
            bank = accesd.AccesD()
        elif(args.bank_type == "rbc"):
            bank = rbc.RBC()
        else:
            raise(RuntimeError("Unknown bank type"))
            

        for f in files:
            bank.add(f);

        bank.entries.sort(key=lambda entry: entry[0])
        
        prev_date = None
        cur_date = start_date
        a_week = datetime.timedelta(days=7)
        while(cur_date < bank.entries[0][0]):
            prev_date = cur_date
            cur_date = cur_date + a_week

        cur_date = prev_date
        for entry in bank.entries:
            if(entry[0] > cur_date):
                while(entry[0] > cur_date):
                    prev_date = cur_date
                    cur_date = cur_date + a_week
                    print("\n{:%Y-%m-%d}".format(prev_date))

            if(entry[1]):
                print("{:%Y-%m-%d}\t{:%Y-%m-%d}\t{}\t{}\t".format(prev_date, entry[0], entry[2], entry[3]))
            else:
                print("{:%Y-%m-%d}\t{:%Y-%m-%d}\t{}\t\t{}".format(prev_date, entry[0], entry[2], entry[3]))
        return 0

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0

if __name__ == "__main__":
    sys.exit(main())
