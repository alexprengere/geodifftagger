#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module read diff on stdin and tags the output.
"""

import argparse

DIFF_FLOW = True
DELIMITER = '\t'
VERBOSE   = False

TAG = 0
KEY = 1
LAT = 3
LNG = 4


def compare_row(row_1, row_2):
    """Compare rows.
    """
    non_matching_cols = []

    for i, _ in enumerate(row_1):
        if row_1[i] != row_2[i]:
            non_matching_cols.append(i)

    return non_matching_cols


def tagger(flow):
    """Tag flow.
    """
    data = {}
    dups = {}
    tags = {}

    for row in flow:
        if row.startswith('#')   or row.startswith('@@')  or \
           row.startswith('+++') or row.startswith('---') or \
           not row:
            continue

        # We properly convert the +/- to a column
        if DIFF_FLOW:
            row = row[0] + DELIMITER + row[1:]

        row = row.rstrip().split(DELIMITER)
        key = row[KEY]

        if VERBOSE:
            print 'Processing key %8s, geo (%-13s, %-13s) from row %s' % \
                    (key, row[LAT], row[LNG], DELIMITER.join(row))

        if key not in data:
            data[key] = row
            tags[key] = row[TAG] if DIFF_FLOW else ''
        else:
            # We store this with duplicates
            dups[key] = row
            # We study the difference
            non_matching_cols = set(compare_row(row, data[key]))

            if not non_matching_cols:
                # Same rows, should not happen
                print 'Weiiiird: %s' % DELIMITER.join(row)

            elif non_matching_cols & set([LAT, LNG]):
                # LAT or LNG has changed
                if non_matching_cols - set([TAG, LAT, LNG]):
                    # Some field other than TAG, LAT, LNG was different
                    tags[key] = 'MP'
                else:
                    tags[key] = 'M'

            else:
                # some properties changed, but not geographically
                tags[key] = 'P'

    return data, dups, tags


def output(data, dups, tags):
    """Display final tagged flow.
    """
    for key, row in data.iteritems():

        print DELIMITER.join([tags[key]] + row)

        if key in dups:
            print DELIMITER.join([tags[key]] + dups[key])


def main():
    """Main.
    """
    global DIFF_FLOW, DELIMITER, VERBOSE, KEY, LAT, LNG

    parser = argparse.ArgumentParser(description='Tag geographical diff.')

    parser.epilog = 'Example: diff -u *.txt | %s -' % parser.prog

    parser.add_argument('flow',
        help = '''Path to the file containing the data. If set to
                       "-", the script will read the standard input
                        instead.''',
        type = argparse.FileType('r'),
        default = '-'
    )

    parser.add_argument('-i', '--indexes',
                        help="""
                        3 arguments which are column indexes:
                        key, lat and lng. key is the column used
                        as an id for each line.
                        Default is %s %s %s.
                        """ % (KEY, LAT, LNG),
                        nargs = 3,
                        type = int,
                        default=None)

    parser.add_argument('-d', '--delimiter',
                        help="""
                        Change default delimiter, which
                        is %s.
                        """ % DELIMITER,
                        default = DELIMITER)

    parser.add_argument('-n', '--no-diff',
                        help="""
                        If passed, this option indicates that we are
                        not reading a diff, so we will not convert the
                        first character (+/-/ ) into a column.
                        """,
                        action = 'store_true')

    parser.add_argument('-v', '--verbose',
                        help="""
                        Verbose output.
                        """,
                        action = 'store_true')

    args = vars(parser.parse_args())
    args = vars(parser.parse_args())

    DELIMITER = args['delimiter']
    DIFF_FLOW = not args['no_diff']
    VERBOSE   = args['verbose']

    if args['indexes'] is not None:
        KEY, LAT, LNG = args['indexes']

    output(*tagger(args['flow']))


if __name__ == '__main__':

    main()

