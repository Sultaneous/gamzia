#!/usr/bin/python

# FileDescriptor
# A serializable class for sending meta data about a file across
# a socket connection.
# Karim Sultan September 17 2020
# Designed for fbomb server.
# 200922 KSU Switched to "clean" JSON for cross-platform usage.
from __future__ import annotations
import types
import os
import time
import json
#import jsonpickle
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
      # We could use reflection to populate it, but toDictionary() has what we need.
      d=self.toDictionary()
      return(json.dumps(d))

   # This is a factory method so it must be static
   @staticmethod
   def deserialize(data) -> FileDescriptor():
      # old - using jsonpickle. Works easily but makes convoluted JSON.
      #object=jsonpickle.decode(data)
      #return (object)
      x=FileDescriptor()
      d=json.loads(data)
      for key,value in d.items():
         if (hasattr(x, key)):
            setattr(x, key, value)
      return(x)

   # Uses reflection to serialize value attributes to a dictionary.
   # Skips any methods or functions or internals.
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
   fd.filename=argv[1]
   if not os.path.isfile(fd.filename):
      print (f"Filename {fd.filename} is not a valid file.")
      exit()
   fd.filemode=FILEMODE.BINARY
   fd.length=os.path.getsize(fd.filename)
   fd.timestamp=time.ctime(os.path.getctime(fd.filename))
   fd.hashtype=HASHTYPE.SHA256
   fd.hash=hashlib.sha256(open(fd.filename,"rb").read()).hexdigest()

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


if __name__ == "__main__":
   main()

