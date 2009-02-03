#!/usr/bin/env python
#
# transform_sql.py -- create a header file with the appropriate SQL variables
# from an SQL file
# The output file is named by adding ".h" onto the input file name.
#


import os
import re
import sys


def usage_and_exit(msg):
  if msg:
    sys.stderr.write("%s\n\n" % msg)
  sys.stderr.write("usage: %s [sqlite_file]\n" % \
    os.path.basename(sys.argv[0]))
  sys.stderr.flush()
  sys.exit(1)


def main(input_filename, output_filename):
  input = open(input_filename, "r").read()
  output = open(output_filename, "w")

  var_name = os.path.basename(input_filename).replace('.', '_')
  var_name = var_name.replace('-', '_')

  output.write('/* This file is automatically generated from %s.\n' %
                                               os.path.basename(input_filename))
  output.write(' * Do not edit it directly, but edit the source file and ')
  output.write('rerun autogen.sh */\n\n')

  output.write('#define %s \\\n' % var_name.upper())

  regex = re.compile(r"/\*.*?\*/", re.MULTILINE|re.DOTALL)
  input = regex.sub('', input)
  for line in input.split('\n'):
    line = line.replace('\n', '')
    line = line.replace('"', '\\"')

    if line and not len(line.strip()) == 0:
      output.write('  "' + line + '"\\\n')

  output.write('  ""\n')

  output.close()


if __name__ == '__main__':
  if len(sys.argv) != 2:
    usage_and_exit("Incorrect number of arguments")
  main(sys.argv[1], sys.argv[1] + ".h")
