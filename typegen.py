# Grab script to find all fonts on system and store them in a config file

import os


os.chdir("C:\\Users\\Fauzaanu\\AppData\\Local\\Microsoft\\Windows\\Fonts")
fonts = os.listdir()

# change directory to current directory
os.chdir(path=os.getcwd())

f = open("manualtype.xml", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
f.write("<!DOCTYPE typemap [\n")
f.write("<!ELEMENT typemap (type)+>\n")
f.write("<!ELEMENT type (#PCDATA)>\n")
f.write("<!ELEMENT include (#PCDATA)>\n")
f.write("<!ATTLIST type name CDATA #REQUIRED>\n")
f.write("<!ATTLIST type fullname CDATA #IMPLIED>\n")
f.write("<!ATTLIST type family CDATA #IMPLIED>\n")
f.write("<!ATTLIST type foundry CDATA #IMPLIED>\n")
f.write("<!ATTLIST type weight CDATA #IMPLIED>\n")
f.write("<!ATTLIST type style CDATA #IMPLIED>\n")
f.write("<!ATTLIST type stretch CDATA #IMPLIED>\n")
f.write("<!ATTLIST type format CDATA #IMPLIED>\n")
f.write("<!ATTLIST type metrics CDATA #IMPLIED>\n")
f.write("<!ATTLIST type glyphs CDATA #REQUIRED>\n")
f.write("<!ATTLIST type version CDATA #IMPLIED>\n")

f.write("<!ATTLIST include file CDATA #REQUIRED>\n")
f.write("]>\n")
f.write("<!--\n")
f.write("  ImageMagick Windows font configuration.\n")
f.write("-->\n")
f.write("<typemap>\n")

for font in fonts:
    
    if font.endswith(".ttf") or font.endswith(".TTF"):
        # write the font name to the type.xml file
        f.write("  <type name=\"" + font + "\" fullname=\"" + font + "\" family=\"" + font + "\" weight=\"400\" style=\"normal\" stretch=\"normal\" glyphs=\"C:\\Windows\\Fonts\\" + font + "\"/>\n")
    
f.write("</typemap>\n")
f.close()


