#***************************************************************************
#*   (c) Jonathan Wiedemann (contact@freecad-france.com) 2015              *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/


'''
post proc for MAKKO FABLAB ARTILECT TOULOUSE
'''

import datetime
now = datetime.datetime.now()


# to distinguish python built-in open function from the one declared below
if open.__module__ == '__builtin__':
    pythonopen = open


def export(objectslist,filename):
    "called when freecad exports a list of objects"
    if len(objectslist) > 1:
        print "This script is unable to write more than one Path object"
        return
    obj = objectslist[0]
    if not hasattr(obj,"Path"):
        print "the given object is not a path"
    gcode = obj.Path.toGCode()
    gcode = parse(gcode)
    gfile = pythonopen(filename,"wb")
    gfile.write(gcode)
    gfile.close()


def convertG81toG1(line, lastline):
    #print line
    #print lastline
    g0, z = lastline.split(" ")
    command, args = line.split(" ",1)
    output = 'G0'
    arglist = args.split(" ")
    for arg in arglist:
        print arg
        if 'X' in arg:
            output += " " + arg
        if 'Y' in arg:
            output += " " + arg
    output += " " + z + "\n"
    output += 'G1'
    for arg in arglist:
        if not 'R' in arg:
            output += " " + arg
    output += "\n"
    output += g0 + " " + z +"\n"
    return output

def convertG83toG1(line, lastline):
    #print line
    #print lastline
    g0, z = lastline.split(" ")
    command, args = line.split(" ",1)
    output = 'G0'
    arglist = args.split(" ")
    for arg in arglist:
        print arg
        if 'X' in arg:
            output += " " + arg
        if 'Y' in arg:
            output += " " + arg
    output += " " + z + "\n"
    output = lastoutput
    output += 'G1'
    for arg in arglist:
        if not 'R' in arg:
            output += " " + arg
    output += "\n"
    output += lastoutput
    return output

def parse(inputstring):
    "parse(inputstring): returns a parsed output string"
    print "postprocessing..."

    output = ""

    # write some stuff first
    output += ";time:"+str(now)+"\n"
    #output += "G17 G20 G80 G40 G90\n"
    output += ";(Exported by FreeCAD)\n"

    lastcommand = None
    lastline = None
    # treat the input line by line
    lines = inputstring.split("\n")
    for line in lines:
        # split the G/M command from the arguments
        if " " in line:
            command,args = line.split(" ",1)
        else:
            # no space found, which means there are no arguments
            command = line
            args = ""
        # add a line number
        #output += "N" + str(linenr) + " "
        print(command)
        # only print the command if it is not the same as the last one
        if line != lastline:
            if command == 'G81' :
                output += convertG81toG1(line, lastline)
            elif command == 'G83' :
                output += convertG83toG1(line, lastline)
            elif command == 'G80' :
                pass
            #elif command == 'G90' :
            #   pass
            elif command == 'G98' :
                pass
            else:
                output += command + " "
                output += args + "\n"

        # store the latest command
        lastcommand = command
        lastline = line

    # write some more stuff at the end
    output += "M2\n"
    #output += "N" + str(linenr + 10) + " M25\n"
    #output += "N" + str(linenr + 20) + " G00 X-1.0 Y1.0\n"
    #output += "N" + str(linenr + 30) + " G17 G80 G40 G90\n"
    #output += "N" + str(linenr + 40) + " M99\n"

    print "done postprocessing."
    return output

print __name__ + " gcode postprocessor loaded."
