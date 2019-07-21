#!/usr/bin/env python3

##### DESCRIPTION ###########################################################
# Paper test generator for testing candidates.
#
##### USAGE #################################################################
# Run ./test-generator.py.
#
##### LICENSE ###############################################################
# Copyright 2018 Maciej Korzeń
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
##### AUTHOR ################################################################
# Maciej Korzen
# maciek@korzen.org, mkorzen@gmail.com
# http://www.korzen.org/

from random import shuffle, randint
import time
import traceback
from pathlib import Path
from tabulate import tabulate
import uuid
import re
#from bs4 import BeautifulSoup
import getopt
import sys

#print("test-generator")

p = Path('test1')
myuuid1 = uuid.uuid4()
mydebug = False

def myreadfile(f1):
    return Path(f1).read_text()

def process_answer_dir(basedir1Path, child):
    if mydebug:
        print("DEBUG: process_answer_dir: basedir1Path:({}), cild({})".format(basedir1Path, child))
    mydir1Path = basedir1Path / child
    files1 = sorted(mydir1Path.glob('*'))
    shuffle(files1)
    hash1 = []
    for filename1 in files1:
        if mydebug:
            print("DEBUG: process_answer_dir: filename1:({})".format(filename1))
        ans1 = myreadfile(filename1)
        if mydebug:
            print("DEBUG: process_answer_dir: filename1:({}): answer:({})".format(filename1, ans1))
        hash1.append([child, ans1])
    if mydebug:
        print("DEBUG: process_answer_dir: list of answers:({})".format(hash1))
    return hash1

def read_answer_files(p):
    if mydebug:
        print("DEBUG: read_answer_files({})".format(p))
    #with q.open() as f: print(f.readline())
    basedir1Path = Path('./{}/answers'.format(p))
    dirs1 = sorted(basedir1Path.glob('*'))
    shuffle(dirs1)
    all_answers = []
    for child in dirs1:
        if mydebug:
            print("DEBUG: read_answer_files(): child.name:({})".format(child.name))
        local_answers = process_answer_dir(basedir1Path, child.name)
        if mydebug:
            print("DEBUG: read_answer_files(): child.name:({}) local_answers:({})".format(child.name, local_answers))
        all_answers.extend(local_answers)
    shuffle(all_answers)
    if mydebug:
        print("DEBUG: read_answer_files({}): all_answers:({})".format(p, all_answers))
    return all_answers

def print_question_with_answers(qanda):
    if mydebug:
        print("DEBUG: print_question_with_answers()")
        print("DEBUG: print_question_with_answers(): qanda:({})".format(qanda))
    tab1 = []
    tab2 = []
    for i in qanda:
        if mydebug:
            #print("DEBUG: print_question_with_answers(): i:({})".format(i))
            print("DEBUG: print_question_with_answers(): question:({})".format(i['question']))
        toadd = [i['question']]
        toadd2 = [i['question']]
        for j in i['answers']:
            if mydebug:
                print("DEBUG: print_question_with_answers(): answer:({}, {})".format(j[0], j[1]))
            toadd.append("[ ]&nbsp;&nbsp;{}".format(j[1]))
            if j[0] == "1":
                toadd2.append("[X]&nbsp;&nbsp;{}".format(j[1]))
            else:
                toadd2.append("[ ]&nbsp;&nbsp;{}".format(j[1]))
        tab1.append(toadd)
        tab2.append(toadd2)
    #if mydebug:
    #    print("DEBUG: print_question_with_answers(): tab1:({})".format(tab1))
    print(tabulate(tab1, headers=['Question', 'Answer1', 'Answer2', 'Answer3', 'Answer4', 'Answer5']))
    print("")
    print("-----------------------------------------------------------------------")
    print("with solution:")
    print(tabulate(tab2, headers=['Question', 'Answer1', 'Answer2', 'Answer3', 'Answer4', 'Answer5']))

def we_have_long_answer(answers):
    if mydebug:
        print("DEBUG: we_have_long_answer():({})".format(answers))
    for a0 in answers:
        txt0 = a0[1].strip()
        txt1 = re.sub('<[^>]+>', '', txt0)
        if mydebug:
            print("DEBUG: we_have_long_answer(): before:({}) after:({})".format(txt0, txt1))
        if len(txt1) > 60:
            return True
    return False

def generate_html_row_code(cnt, data):
    long_answer_addition1 = ""
    td_width_text = ' width="20%"'
    mycolspan = " colspan=\"5\""
    if we_have_long_answer(data['answers']):
        long_answer_addition1 = "</tr><tr>"
        td_width_text = ' width="100%"'
        mycolspan = ""
    ret1 = "<table>\n"
    ret1 += "<tr>\n"
    ret1 += "<th{}>Pytanie {}. {}</th>\n".format(mycolspan, cnt, data['question'])
    ret1 += "</tr>\n"
    ret1 += "<tr>\n"
    ret2 = ret1
    answer_counter = 0
    for j in data['answers']:
        good_addition = ""
        checkbox_code = "&#9744;"
        if j[0] == "1":
                good_addition = " class=\"good\""
                checkbox_code = "&#9745;"
        if answer_counter > 3:
            long_answer_addition1 = ""
        ret1 += "<td>&#9744; {}</td>{}\n".format(j[1], long_answer_addition1)
        ret2 += "<td{}>{} {}</td>{}\n".format(good_addition, checkbox_code, j[1], long_answer_addition1)
        answer_counter += 1
    end1 = "</tr>"
    end1 += "</table>"
    ret1 += end1
    ret2 += end1
    return [ret1, ret2]

def write_html_files(qanda):
    if mydebug:
        print("DEBUG: write_html_files()")
        #print("DEBUG: write_html_files(): qanda:({})".format(qanda))
    fileheader = myreadfile(Path("header.include.html"))
    filefooter = myreadfile(Path("footer.include.html"))
    strmyuuid1 = str(myuuid1)
    fileheader = re.sub('__UUID__', strmyuuid1, fileheader)
    filefooter = re.sub('__UUID__', strmyuuid1, filefooter)
    file1content = fileheader
    file2content = fileheader
    with open("test-{}-candidate.html".format(strmyuuid1), "w", newline="\r\n") as ftc, open("test-{}-hr.html".format(myuuid1), "w", newline="\r\n") as fth:
        cnt = 1
        for i in qanda:
            row_html = generate_html_row_code(cnt, i)
            file1content += row_html[0]
            file2content += row_html[1]
            cnt += 1
        file1content += filefooter
        file2content += filefooter
        #file1content = BeautifulSoup(file1content, "html.parser").prettify()
        #file2content = BeautifulSoup(file2content, "html.parser").prettify()
        ftc.write(file1content)
        fth.write(file2content)

def process_questions(dirs):
    if mydebug:
        print("DEBUG: process_questions(): dirs:({}): start".format(dirs))
    dirs2 = []
    for dir1 in dirs:
        for entry1 in Path('./{}'.format(dir1)).glob('*'):
            if mydebug:
                print("DEBUG: process_questions(): entry1({})".format(entry1))
            dirs2.append(str(entry1))
        #dirs2.append(Path('./{}'.format(mytestdir1)).glob('*'))
    all_questions_and_answers = []
    shuffle(dirs2)
    dirs2 = dirs2[:100]
    if mydebug:
        print("DEBUG: process_questions(): dirs2:({})".format(dirs2))
    for child in dirs2:
        if mydebug:
            print("DEBUG: process_questions(): child:({})".format(child))
        myquestion = myreadfile(Path(child) / 'question')
        myanswers = read_answer_files(Path(child))
        e1 = {}
        e1['question'] = myquestion
        e1['answers'] = myanswers
        all_questions_and_answers.append(e1)
    #print(all_questions_and_answers)
    #print_question_with_answers(all_questions_and_answers)
    write_html_files(all_questions_and_answers)

#for x in p.iterdir():
#    print(str(x))
#    q = x / 'question'
#    print("q:({})".format(q))
#    read_question_file(q)

def usage():
    print("test-generator.py -d DIR1 [-d DIR2 [ -d DIR3 [...]]]")

def program_start(args):
    dirs = []
    try:
        optlist, args = getopt.getopt(args, 'd:')
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in optlist:
        if o == "-d":
            dirs.append(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    if len(dirs) < 1:
        print("Error! At lease one directory name is required.")
        usage()
        sys.exit(2)
    if mydebug:
        print("DEBUG: program_start(): dirs:({})",format(dirs))
    process_questions(dirs)

program_start(sys.argv[1:])

# vim: set shiftwidth=4 expandtab smarttab softtabstop=4:
