#!/usr/bin/python

'''
    Copyright 2009, The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License. 
    You may obtain a copy of the License at 

        http://www.apache.org/licenses/LICENSE-2.0 

    Unless required by applicable law or agreed to in writing, software 
    distributed under the License is distributed on an "AS IS" BASIS, 
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
    See the License for the specific language governing permissions and 
    limitations under the License.

    This version is modified by Autosun Li
    Usage:
    * Logcat Reader
       Run coloredlogcat.py with standard input (only accept format with threadtime)
       e.g. $ coloredlogcat.py < Log_file.log
    * Realtime capture log:
       Run coloredlogcat.py without parameters.
       e.g. $ coloredlogcat.py [-o output_file] [tag_list]
       ( It will be same as the following command )
       $ adb logcat -v threadtime [-s tag_list] [| tee output_file] | coloredlogcat.py
'''

# script to highlight adb logcat output for console
# written by jeff sharkey, http://jsharkey.org/
# piping detection and popen() added by other android team members


import os, sys, re, StringIO
import fcntl, termios, struct, getopt

# Native show message, default off
native = 0

# unpack the current terminal width/height
data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234')
HEIGHT, WIDTH = struct.unpack('hh',data)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def format(fg=None, bg=None, bright=False, bold=False, dim=False, reset=False):
    # manually derived from http://en.wikipedia.org/wiki/ANSI_escape_code#Codes
    codes = []
    if reset: codes.append("0")
    else:
        if not fg is None: codes.append("3%d" % (fg))
        if not bg is None:
            if not bright: codes.append("4%d" % (bg))
            else: codes.append("10%d" % (bg))
        if bold: codes.append("1")
        elif dim: codes.append("2")
        else: codes.append("22")
    return "\033[%sm" % (";".join(codes))


def indent_wrap(message, indent=0, width=80):
    wrap_area = width - indent
    messagebuf = StringIO.StringIO()
    current = 0
    firstline = int(1)
    while current < len(message):
        if firstline == 1:
            # 12 bytes of color length
            next = min(current + wrap_area + 12, len(message))
            firstline = int(0)
        else:
            next = min(current + wrap_area, len(message))
        messagebuf.write(message[current:next])
        if next < len(message) and native == 0:
            messagebuf.write("\n%s" % (" " * indent))
        current = next
    return messagebuf.getvalue()


LAST_USED = [RED,GREEN,YELLOW,MAGENTA,CYAN]
KNOWN_TAGS = {
    "dalvikvm": BLUE,
    "Process": BLUE,
    "ActivityManager": CYAN,
    "ActivityThread": CYAN,
}

def allocate_color(tag):
    # this will allocate a unique format for the given tag
    # since we dont have very many colors, we always keep track of the LRU
    if not tag in KNOWN_TAGS:
        KNOWN_TAGS[tag] = LAST_USED[0]
    color = KNOWN_TAGS[tag]
    try:
        LAST_USED.remove(color)
    except:
        print("Remove color exception")
    LAST_USED.append(color)
    return color


RULES = {
    #re.compile(r"([\w\.@]+)=([\w\.@]+)"): r"%s\1%s=%s\2%s" % (format(fg=BLUE), format(fg=GREEN), format(fg=BLUE), format(reset=True)),
}

TIME_WIDTH = 20
PROCESS_WIDTH = 14 # 8 or -1
LABEL_WIDTH = 20
TAGTYPE_WIDTH = 3
HEADER_SIZE = TAGTYPE_WIDTH + 1 + PROCESS_WIDTH + 1 + LABEL_WIDTH + 1 + TIME_WIDTH + 1

TAGTYPES = {
    "V": "%s%s%s " % (format(fg=WHITE, bg=BLACK), "V".center(TAGTYPE_WIDTH), format(reset=True)),
    "D": "%s%s%s " % (format(fg=WHITE, bg=BLUE), "D".center(TAGTYPE_WIDTH), format(reset=True)),
    "I": "%s%s%s " % (format(fg=BLACK, bg=GREEN), "I".center(TAGTYPE_WIDTH), format(reset=True)),
    "W": "%s%s%s " % (format(fg=BLACK, bg=YELLOW), "W".center(TAGTYPE_WIDTH), format(reset=True)),
    "E": "%s%s%s " % (format(fg=WHITE, bg=RED), "E".center(TAGTYPE_WIDTH), format(reset=True)),
    "F": "%s%s%s " % (format(fg=BLACK, bg=RED, bright=True), "F".center(TAGTYPE_WIDTH), format(reset=True)),
}

retag = re.compile("^(\d*-\d*)\s+(\d*:\d*:\d*\.\d*)\s+(\d*)\s+(\d*)\s+([A-Z])\s+([\w\-\.]*)\s*:\s(\s*\w*)(.*)$")

# analysis argv parameters
opts, args = getopt.getopt(sys.argv[1:], "o:N")

adb_args = "adb logcat -v threadtime"
if len(args) != 0:
    adb_args += " -s"
for arg in args:
    adb_args += " " + arg

for opt, para in opts:
    if opt == "-o":
        adb_args += " | tee " + para

for opt, para in opts:
    if opt == "-N":
        native = 1

# if someone is piping in to us, use stdin as input.  if not, invoke adb logcat
if os.isatty(sys.stdin.fileno()):
    input = os.popen(adb_args)
else:
    input = sys.stdin

while True:
    try:
        line = input.readline()
    except KeyboardInterrupt:
        break

    match = retag.match(line)
    if not match is None:
        date, time, owner, tid, tagtype, label, tag, message = match.groups()
        linebuf = StringIO.StringIO()

        # time info
        if TIME_WIDTH > 0:
            date = (date + " " + time).strip().center(TIME_WIDTH)
            linebuf.write("%s%s%s " % (format(fg=BLACK, bg=BLACK, bright=True), date, format(reset=True)))

        # center process info
        if PROCESS_WIDTH > 0:
            owner = (owner + "." + tid).strip().center(PROCESS_WIDTH)
            linebuf.write("%s%s%s " % (format(fg=BLACK, bg=BLACK, bright=True), owner, format(reset=True)))

        # write out label colored edge
        label = label.strip()
        color = allocate_color(label)
        label = label[-LABEL_WIDTH:].rjust(LABEL_WIDTH)
        linebuf.write("%s%s %s" % (format(fg=color, dim=False), label, format(reset=True)))

        # write out tagtype colored edge
        if not tagtype in TAGTYPES: break
        linebuf.write(TAGTYPES[tagtype])

        # color tag
        colored_tag = StringIO.StringIO()
        color = allocate_color(tag)
        colored_tag.write("%s%s%s" % (format(fg=color, dim=False), tag, format(reset=True)))

        # insert line wrapping as needed
        message = indent_wrap(colored_tag.getvalue() + message, HEADER_SIZE, WIDTH)

        # format tag message using rules
        for matcher in RULES:
            replace = RULES[matcher]
            message = matcher.sub(replace, message)

        linebuf.write(message)
        line = linebuf.getvalue()
        print line
    else:
        print line,

    if len(line) == 0: break

