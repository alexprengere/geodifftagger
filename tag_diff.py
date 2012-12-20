#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module read diff on stdin and tags the output.
"""

import argparse
from sys import stdin

DELIMITER = '\t'

TYPE = 0
KEY  = 1
LAT  = 3
LNG  = 4


def compare_row(row_1, row_2):
    """Compare rows.
    """
    non_matching_cols = []

    for i, _ in enumerate(row_1):
        if row_1[i] != row_2[i]:
            non_matching_cols.append(i)

    return non_matching_cols


def tag(flow):
    """Main.
    """
    data = {}
    dups = {}

    for row in flow:
        if row.startswith('#')   or row.startswith('@@')  or \
           row.startswith('+++') or row.startswith('---') or \
           not row:
            continue

        # We properly convert the +/- to a column
        row = row[0] + '\t' + row[1:]

        row = row.rstrip().split(DELIMITER)
        key = row[KEY]

        if key not in data:
            data[key] = row
        else:
            # We store this with duplicates
            dups[key] = row
            # We study the difference
            non_matching_cols = set(compare_row(row, data[key]))

            if not non_matching_cols:
                # Same rows, should not happen
                print 'Weiiiird: %s' % row

            elif non_matching_cols & set([LAT, LNG]):
                # LAT or LNG has changed
                if non_matching_cols.issubset(set([TYPE, LAT, LNG])):
                    data[key][TYPE] = 'M'
                    dups[key][TYPE] = 'M'
                else:
                    data[key][TYPE] = 'MP'
                    dups[key][TYPE] = 'MP'

            else:
                # some properties changed, but not geographically
                data[key][TYPE] = 'P'
                dups[key][TYPE] = 'P'

    return data, dups


def output(data, dups):
    """Display final tagged flow.
    """
    for key, row in data.iteritems():

        print DELIMITER.join(row)

        if key in dups:
            print DELIMITER.join(dups[key])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Tag geographical diff.')

    parser.epilog = 'Example: diff -u *.txt | %s' % parser.prog

    parser.add_argument('-i', '--indexes',
                        help="""
                        3 arguments which are column indexes:
                        key, lat and lng. key is the column used
                        as an id for each line.
                        Default is %s %s %s.
                        """ % (KEY, LAT, LNG),
                        nargs = 3,
                        default=None)

    parser.add_argument('-d', '--delimiter',
                        help="""
                        Change default delimiter, which
                        is %s.
                        """ % DELIMITER,
                        default = DELIMITER)

    args = vars(parser.parse_args())

    DELIMITER = args['delimiter']

    if args['indexes'] is not None:
        KEY, LAT, LNG = args['indexes']

    output(*tag(stdin))

