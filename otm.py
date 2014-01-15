#!/usr/bin/env python2

description = 'otm - display static memory of an elf file in a treemap'

"""
Copyright (C) 2014  Ludwig Ortmann <ludwig@spline.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from os import path
import subprocess
import random
import re
import argparse


from pprint import pprint

import pylab
from matplotlib.patches import Rectangle

class Treemap:
    def __init__(self, tree):
        self.ax = pylab.subplot(111,aspect='equal')
        pylab.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.iterate(tree)

    def iterate(self, node, lower=[0,0], upper=[1,1], axis=0):
        axis = axis % 2
        self.draw_rectangle(lower, upper, node)
        width = upper[axis] - lower[axis]
        ns = node.get_size()
        #print node.name, "w:", width
        #print "node has", len(node.children)

        for child in node.children:
            #print "child:", child.name
            cs = child.get_size()
            upper[axis] = (lower[axis] + ((width * float(cs)) / ns))
            lo = list(lower)
            up = list(upper)
            self.iterate(child, lo, up, axis + 1)
            lower[axis] = upper[axis]

    def draw_rectangle(self, lower, upper, node):
        #print lower, upper
        r = Rectangle( lower, upper[0]-lower[0], upper[1] - lower[1],
                   edgecolor='k',
                   facecolor= node.get_color(),
                   label=node.name)
        self.ax.add_patch(r)

        rx, ry = r.get_xy()
        rw = r.get_width()
        rh = r.get_height()
        cx = rx + rw/2.0
        cy = ry + rh/2.0
        if isinstance(node, PathNode):
            t = node.name
            if rw * 3 < rh:
                t += ", "
            else:
                t += "\n"
            t += str(node.size) + ", " + node.stype
            c='w'
            if rw < rh:
                o = "vertical"
            else:
                o = "horizontal"

        else:
            t = node.name
            if node.isfile:
                c='k'
                o = 45
            else:
                return
        self.ax.annotate(
                t,
                (cx,cy),
                color=c,
                weight='bold', ha='center', va='center',
                rotation=o
                )

class PathTree():
    def __init__(self, name, path_dict):

        self.children = list()
        self.name = name
        self.size = None
        self.isfile = False

        print name

        subdirectories = list()
        for p in path_dict:
            if p == '':
                #print "content", p
                self.add_children(path_dict[p])
                self.isfile = True
            else:
                #print "entry", p
                subdirectories.append(p)

        cdict = dict()
        for pathname in subdirectories:
            parts = pathname.split("/", 1)
            if len(parts) == 1:
                x = parts[0]
                rest = ""
            else:
                x,rest = parts

            if not x in cdict:
                cdict[x] = dict()
            cdict[x][rest] = path_dict[pathname]
            #print "adding", pathname, "to", x

        for k in cdict:
            #pprint(v, indent=2)
            self.children.append(PathTree(k, cdict[k]))

        #print "size:", self.get_size()

    def __repr__(self):
        return self.name

    def add_children(self, sym_list):
        for symbol in sym_list:
            self.children.append(PathNode(*symbol))

    def get_size(self):
        if self.size is None:
            self.size = 0
            for c in self.children:
                self.size += c.get_size()
        return self.size

    def get_color(self):
        return (random.random(),random.random(),random.random())


class PathNode(PathTree):

    def __init__(self, name, line, size, stype):
        self.children = []
        print "\t", name, stype
        self.name = name
        self.size = size
        self.line = line
        self.isfile = False
        self.stype = stype


def parse_elf(filename, minimum_size=None, symbol_type_list=None,
        function_path_regex_in=None, function_name_regex_in=None,
        object_path_regex_in=None, object_name_regex_in=None,
        function_path_regex_ex=None, function_name_regex_ex=None,
        object_path_regex_ex=None, object_name_regex_ex=None,
        ):
    """parse elf file into a {path: [(symbol, linenumber, size)]} dictionary"""

    output = subprocess.check_output([
                "nm",
                "--radix=d",
                "-S",
                "-l",
                "--size-sort",
                filename])

    "addr size type name [path:line]"
    addressses = [x.split() for x in output.splitlines()]

    paths = dict()
    for foo in addressses:
        size = foo[1]
        stype = foo[2]
        symbolname = foo[3]
        if len(foo) > 4:
            pathname,lineno = foo[4].split(":")
        else:
            pathname,lineno = '??','?'
        size = int(size)
        if minimum_size and size < minimum_size:
            continue
        pathname = path.normpath(pathname)
        if pathname[0] == '/':
            pathname = pathname[1:]

        if stype in "tT":
            ppati = function_path_regex_in
            npati = function_name_regex_in
            ppate = function_path_regex_ex
            npate = function_name_regex_ex
        elif stype in 'bB':
            ppati = object_path_regex_in
            npati = object_name_regex_in
            ppate = object_path_regex_ex
            npate = object_name_regex_ex
        else:
            ppat = None
            npat = None

        if ppati and not re.search(ppati, pathname):
            continue
        if npati and not re.search(npati, symbolname):
            continue
        if ppate and re.search(ppate, pathname):
            continue
        if npate and re.search(npate, symbolname):
            continue
        if symbol_type_list and stype not in symbol_type_list:
            continue

        if not pathname in paths:
            paths[pathname] = list()
        paths[pathname].append((symbolname, lineno, size, stype))

    return paths

def arg_parser():
    p = argparse.ArgumentParser(description=description)

    p.add_argument("filename", default="a.out", nargs='?',
            help="the elf file to parse")

    p.add_argument("-d","--documentation",
            action="store_true", default=argparse.SUPPRESS,
            help="print additional documentation and exit")

    p.add_argument("-fp", "--function-path-regex-in", default=None,
            help="regular expression for function path inclusion")
    p.add_argument("-op","--object-path-regex-in", default=None,
            help="regular expression for object path inclusion")
    p.add_argument("-fn", "--function-name-regex-in", default=None,
            help="regular expression for function name inclusion")
    p.add_argument("-on","--object-name-regex-in", default=None,
            help="regular expression for object name inclusion")

    p.add_argument("-Fp", "--function-path-regex-ex", default=None,
            help="regular expression for function path exclusion")
    p.add_argument("-Op","--object-path-regex-ex", default=None,
            help="regular expression for object path exclusion")
    p.add_argument("-Fn", "--function-name-regex-ex", default=None,
            help="regular expression for function name exclusion")
    p.add_argument("-On","--object-name-regex-ex", default=None,
            help="regular expression for object name exclusion")

    p.add_argument("-t","--symbol-type-list", default=None,
            help="list of symbol types to include")
    p.add_argument("-m","--minimum-size", type=int, default=1,
            help="mininum size for all types")

    return p

def exit_doc():
    print """
Regular expression examples:
    display only functions that come from net or core:
        --function-path-regex-in "net|core"

    display only objects that nm could not look up
        --obj-path-regex "\?\?"

    do not display objects that end on _stack
        --object-name-regex-ex "_stack$"

    When combining these options, exclusion takes precedence over
    inclusion:

    display only objects from main.c filtering out stacks:
        -op "main\.c" -On "_stack$|_stk$"


Symbol type list:
    include text and BSS section symbols check the nm manpage for
    details:
        --symbol-type-list tTbB


Minumum size:
    The minimum-size argument is taken as an inclusion hurdle, i.e.
    symbols below that size are not taken into consideration at all.
"""
    sys.exit()

if __name__ == '__main__':
    args = arg_parser().parse_args()
    if hasattr(args,"documentation"):
        exit_doc()

    if not path.isfile(args.filename):
        sys.exit("file does not exist: " + args.filename)

    elf = parse_elf(**vars(args))
    tree = PathTree("root", elf)
    Treemap(tree)
    pylab.show()
