#!/usr/bin/python3

# Colours module by Karim Sultan April 2015.

# Version KAS 150412
# This script defines a set of constants for foreground colors,
# background colors, and console text styles to be used in Python
# console scripts.
#
# KSU 201010 Added macro modes + test case.
#
# To use this script in python:
#
# In your python script, near the top, add:
# import colour
#
# Example:
# s = Col.cdr + "Warning!" + Col.coff
# s = Col.sre + Col.cly + Col.bdr + "Error! Error!" + Col.soff + Col.coff + Col.boff
#
# Use the Color Off constant "coff", the Background Color Off
# constant "boff" and the Style Off constant "soff" to clear
# formatting:
# s = Col.coff + Col.soff + Col.boff +"Back to normal"
#
# Codes are abbreviated for quick insertion.  Abbreviation format:
# 1st:   c: color         b: background color           s: style
# 2nd:   l: light         d: dark
# rest:  color / style
import os

class Colours:
   # No support for ANSI in Windows, so disable.
   if (os.name=="Windows" or os.name=="nt"):
      # Foreground (Text) Colors
      cbl=""       # Color Black
      cdr=""       # Color Dark Red
      cdg=""       # Color Dark Green
      cdy=""       # Color Dark Yellow
      cdb=""       # Color Dark Blue
      cdm=""       # Color Dark Magenta
      cdc=""       # Color Dark Cyan
      clgy=""      # Color Light Gray

      cdgy=""      # Color Dark Gray
      clr=""       # Color Light Red
      clg=""       # Color Light Green
      cly=""       # Color Light Yellow
      clb=""       # Color Light Blue
      clm=""       # Color Light Magenta
      clc=""       # Color Light Cyan
      cwh=""       # Color White

      # Turns off all formatting
      coff=""       # Color Off

      # Background Colors
      bbl=""       # Background Color Black
      bdr=""       # Background Color Dark Red
      bdg=""       # Background Color Dark Green
      bdy=""       # Background Color Dark Yellow
      bdb=""       # Background Color Dark Blue
      bdm=""       # Background Color Dark Magenta
      bdc=""       # Background Color Dark Cyan
      blgy=""      # Background Color Light Gray
  
      bdgy=""     # Background Color Dark Gray
      blr=""      # Background Color Light Red
      blg=""      # Background Color Light Green
      bly=""      # Background Color Light Yellow
      blb=""      # Background Color Light Blue
      blm=""      # Background Color Light Magenta
      blc=""      # Background Color Light Cyan
      bwh=""      # Background Color White

      # Turns off only the background color
      boff=""      # Background Color Off

      # Macro strings 
      # Master off switch turns off color and bacground in one mnemonic
      off=coff+boff
      no=cly+bdr
      yes=clg+bdg
      old=cly+bdb
      retro=cwh+bbl
      paper=cbl+bwh

      # Styles
      sbo=""        # Style Bold
      sdi=""        # Style Dim
      sun=""        # Style Underline
      sbl=""        # Style Blink
      sre=""        # Style Reverse
      shi=""        # Style Hidden

      sbof=""      # Style Bold Off
      sdif=""      # Style Dim Off
      sunf=""      # Style Underline Off
      sblf=""      # Style Blink Off
      sref=""      # Style Reverse Off
      shif=""      # Style Hidden Off

   # Linux supports ANSI
   else:
      # Foreground (Text) Colors
      cbl="\033[30m"       # Color Black
      cdr="\033[31m"       # Color Dark Red
      cdg="\033[32m"       # Color Dark Green
      cdy="\033[33m"       # Color Dark Yellow
      cdb="\033[34m"       # Color Dark Blue
      cdm="\033[35m"       # Color Dark Magenta
      cdc="\033[36m"       # Color Dark Cyan
      clgy="\033[37m"      # Color Light Gray

      cdgy="\033[90m"      # Color Dark Gray
      clr="\033[91m"       # Color Light Red
      clg="\033[92m"       # Color Light Green
      cly="\033[93m"       # Color Light Yellow
      clb="\033[94m"       # Color Light Blue
      clm="\033[95m"       # Color Light Magenta
      clc="\033[96m"       # Color Light Cyan
      cwh="\033[97m"       # Color White

      # Turns off all formatting
      coff="\033[0m"       # Color Off

      # Background Colors
      bbl="\033[40m"       # Background Color Black
      bdr="\033[41m"       # Background Color Dark Red
      bdg="\033[42m"       # Background Color Dark Green
      bdy="\033[43m"       # Background Color Dark Yellow
      bdb="\033[44m"       # Background Color Dark Blue
      bdm="\033[45m"       # Background Color Dark Magenta
      bdc="\033[46m"       # Background Color Dark Cyan
      blgy="\033[47m"      # Background Color Light Gray

      bdgy="\033[100m"     # Background Color Dark Gray
      blr="\033[101m"      # Background Color Light Red
      blg="\033[102m"      # Background Color Light Green
      bly="\033[103m"      # Background Color Light Yellow
      blb="\033[104m"      # Background Color Light Blue
      blm="\033[105m"      # Background Color Light Magenta
      blc="\033[106m"      # Background Color Light Cyan
      bwh="\033[107m"      # Background Color White

      # Turns off only the background color
      boff="\033[49m"      # Background Color Off

      # Macro strings 
      # Master off switch turns off color and bacground in one mnemonic
      off=coff+boff
      no=cly+bdr
      yes=clg+bdg
      old=cly+bdb
      retro=cwh+bbl
      paper=cbl+bwh

      # Styles
      sbo="\033[1m"        # Style Bold
      sdi="\033[2m"        # Style Dim
      sun="\033[4m"        # Style Underline
      sbl="\033[5m"        # Style Blink
      sre="\033[7m"        # Style Reverse
      shi="\033[8m"        # Style Hidden

      sbof="\033[21m"      # Style Bold Off
      sdif="\033[22m"      # Style Dim Off
      sunf="\033[24m"      # Style Underline Off
      sblf="\033[25m"      # Style Blink Off
      sref="\033[27m"      # Style Reverse Off
      shif="\033[28m"      # Style Hidden Off

   # Lists of colour and backgrounds
   listcall = [f"{cbl}", f"{cdr}", f"{cdg}", f"{cdy}", f"{cdb}", f"{cdm}", f"{cdc}", f"{clgy}",
   f"{clr}", f"{clg}", f"{cly}", f"{clb}", f"{clm}", f"{clc}", f"{cwh}", f"{cdgy}", f"{coff}"]

   listball = [f"{bbl}", f"{bdr}", f"{bdg}", f"{bdy}", f"{bdb}", f"{bdm}", f"{bdc}", f"{blgy}",
   f"{blr}", f"{blg}", f"{bly}", f"{blb}", f"{blm}", f"{blc}", f"{bwh}", f"{bdgy}", f"{boff}"]

   listsall = [f"{sbo}", f"{sdi}", f"{sun}", f"{sbl}", f"{sre}", f"{shi}",
   f"{sbof}", f"{sdif}", f"{sunf}", f"{sblf}", f"{sref}", f"{shif}"]

   listmall = [f"{no}", f"{yes}", f"{old}", f"{retro}", f"{paper}", f"{off}"]

   # Static method to remove colour codes from a formatted string
   # This could probably be done more compactly with a regex, but this way
   # was super quick and easy.  :)
   @staticmethod
   def cstrip(label):
      for c in Colours.listcall:
         label=label.replace(c, "")
      for b in Colours.listball:
         label=label.replace(b, "")
      for s in Colours.listsall:
         label=label.replace(s, "")
      return (label)
#End of class
#**************************************************************************
   
# Test method.  No need for unit tests with this Class
def doTest():
   C = Colours()
   if (C.clc==""):
      print ("This OS does not support ANSI colour in terminals.")
      print ("Test will execute, but output should be clean and colourless.")
      print()

   print()
   print ("Foreground Colour Test: ", end='')
   for c in C.listcall:
      if not c==C.coff:
         print (f"{c}W{C.coff}", end='', flush=True)
   print()

   print ("Background Colour Test: ", end='')
   for b in C.listball:
      if not b==C.boff:
         print (f"{b}W{C.boff}", end='', flush=True)
   print()

   print()
   print ("Macro format tests:")
   for m in C.listmall:
      if not m==C.off:
         print (f"{m}Colours Module is colourful.{C.off}")
   print()

   print(f"Style test: (Note not all styles work on all terminals){C.clc}")
   print(f"{C.sbo}This is BOLD.{C.sbof}")
   print(f"{C.sdi}This is DIM.{C.sdif}")
   print(f"{C.sun}This is UNDERLINE.{C.sunf}")
   print(f"{C.sre}This is REVERSE.{C.sref}")
   print(f"{C.sbl}This is BLINK.{C.sblf}")
   print(f"{C.shi}This is HIDDEN.{C.shif}{C.off}")

   print()
   print("Colour grid:")
   for i in range (17):
      print(f"{i:^5}", end='')
   print()
   x=1
   for c in C.listcall:
      if not c==C.coff:
         print (f"{x:^5}", end='')
         x+=1
      for b in C.listball:
         if not c==C.coff and not b==C.boff:
            print (f"{c}{b}  W  {C.off}", end='', flush=True)
      print()
   print()

if (__name__=="__main__"):
   doTest()
