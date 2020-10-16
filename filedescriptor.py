#!/usr/bin/python

# FileDescriptor
# A serializable class for sending meta data about a file across
# a socket connection.
# Karim Sultan September 17 2020
# Designed for fbomb server.

# 200922 KSU Switched to "clean" JSON for cross-platform usage.
# 201015 KSU Added meta data population method; previously this was done
#            externally.

from __future__ import annotations
import types
import os
import time
import json
import hashlib
from enum import Enum
import sys
argv=sys.argv
argc=len(argv)

class FILEMODE(str, Enum):
   ASCII="ASCII"
   BINARY="BINARY"

class HASHTYPE(str, Enum):
   SHA128 = "SHA128"
   SHA224 = "SHA224"
   SHA256 = "SHA256"
   SHA384 = "SHA384"
   SHA512 = "SHA512"
   MD5 = "MD5"

class FileDescriptor:
   def __init__(self):
      self.filename=""
      self.hash=""
      self.length=0
      self.timestamp=""

      # Is of type Enum HASHTYPE
      self.hashtype=HASHTYPE.SHA256
      # Is of type Enum FILEMODE
      self.filemode=FILEMODE.BINARY

   def serialize(self):
      # old - using jsonpickle. Works easily but makes convoluted JSON.
      #s=jsonpickle.encode(self)
      #return(s)

      # new - "clean" json string. Just uses a dictionary.
      # Method toDictionary() uses reflection  to create itself.
      d=self.toDictionary()
      return(json.dumps(d))

   # This is a factory method so it must be static
   # We use futures to put some constraints on method signature.
   @staticmethod
   def deserialize(data) -> FileDescriptor():
      # old - using jsonpickle. Works easily but makes convoluted JSON.
      # This meant it was not easily portable across other languages.
      #object=jsonpickle.decode(data)
      #return (object)

      # Use reflection to fill JSON instance, return FileDescriptor object
      x=FileDescriptor()
      d=json.loads(data)
      for key,value in d.items():
         if (hasattr(x, key)):
            setattr(x, key, value)
      return(x)

   # Populate class attributes with file info required by FBomb protocol.
   # Returns True if successful, False otherwise
   def populate(self, filename):
      try:
         if not os.path.isfile(filename):
            return (False)
         self.filename=filename

         # Fill what we can, use defaults otherwise.
         self.filemode=FILEMODE.BINARY
         self.length=os.path.getsize(self.filename)
         self.timestamp=time.ctime(os.path.getctime(self.filename))
         self.hashtype=HASHTYPE.SHA256
         self.hash=hashlib.sha256(open(self.filename,"rb").read()).hexdigest()
      except Exception as err:
         return (False)
      return (True)

   # Uses reflection to serialize value attributes to a dictionary.
   # Skips any methods or functions or private scoped attributes.
   def toDictionary(self):
      d={}
      s=dir(self)
      i=0
      while True:
         if s[i].startswith("__") and s[i].endswith("__"):
            # Attribute is an internal, remove
            s.pop(i)
         elif (isinstance(getattr(self, s[i]), types.MethodType) or
               "function" in str(type(getattr(self, s[i])))):
            # Attribute is a method/function, remove
            s.pop(i)
         else:
            # Attribute is a value attribute, continue
            i+=1
         if (i>=len(s)):
            break
      for key in s:
         d[key]=getattr(self, key)
      return (d)

   # Generic method to make a string representation of class instance
   # value attributes (public fields).
   def toString(self):
      s=""
      d=self.toDictionary()
      for key, value in d.items():
         s+=f"{key}={value}\n"
      return(s)

#*************************************************************************

# Main serves as a test method, and illustrates the usage of the
# FileDescriptor class.
# The serialized bytes data can be sent across the wire to a server,
# and this metadata can be reconstituted on the remote end.
def main():
   # Process command line
   if (argc<2):
      print (f"Syntax: [script] <file>")
      exit()

   # Sanitize / initialize
   fd=FileDescriptor()
   result=fd.populate(argv[1])
   if not result:
      print (f"Filename {fd.filename} is not a valid file, or other error occured.")
      exit()

   print ("FD Object Data:")
   print (fd.toString())
   print ("Serializing...")
   data=fd.serialize()
   print ()
   print (f"Serialized data is {len(data)} bytes. JSON Data:")
   print (data)
   print ()
   print ("Deserializing... FD Object Data:")
   newfd = fd.deserialize(data)
   print(newfd.toString())
   print ("Done")


if (__name__ == "__main__"):
   main()

