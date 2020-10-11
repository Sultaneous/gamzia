#!/usr/bin/python

# Karim Sultan May 2020
# Timer class - acts as performance stopwatch.
# Use as follows within code:

# KSU 201010 Made field attributes private.  Made elapsed() stop
#            the timer if it is still running.  Added sanity checks.
#            Added test cases.  Added some robustness.

# from timer import Timer
# timer = Timer()
# timer.start()
# ... do measurable stuff ...
# timer.stop()
# print(f"Time taken: {timer.elapsed} seconds.")

from time import perf_counter
import time

# Small timer class to handle performance timing
class Timer():
   def __init__(self):
      self.__timeStart=0
      self.__timeStop=0
      self.__timeElapsed=0
      self.__running=False

   def start(self):
      self.__timeStop=self.__timeElapsed=0
      self.__running=True
      self.__timeStart=perf_counter()

   def stop(self):
      self.__timeStop=perf_counter()
      self.__running=False

   def elapsed(self):
      # Stop if not stopped
      if (self.isRunning):
         self.stop()

      # Sanity on stop without start
      if (self.__timeStart==0):
         return(0)

      self.__timeElapsed = self.__timeStop - self.__timeStart
      return (self.__timeElapsed)

   def peek(self):
      if (self.isRunning()):
         return (perf_counter()-self.__timeStart)
      else:
         return (0)

   def isRunning(self):
      return(self.__running)

#End of class
###########################################################################

def UnitTestPeek():
   # Setup
   rounds=4
   print("Testing peek without start; should show 0s.:")
   print(f"Testing start, peek; should show time in ~1s intervals, to ~{rounds}:")

   # Test
   timer=Timer()
   timer.start()
   x=0
   for i in range (rounds):
      time.sleep(1)
      p=timer.peek()
      print(f"Time from start to now: {p:.2f}\r", end='', flush=True)
   x=int(p)
   print()

   # Assert
   try:
      assert x==rounds, f"Required {rounds}, got {x}."
      return (True)
   except AssertionError as err:
      print(f"TEST FAILED: {err}")
      return (False)

def UnitTestStopNoStart():
   # Setup
   print()
   print("Testing break case: stop without start.  Should show 0s.")

   # Test
   timer=Timer()
   timer.stop()
   e=timer.elapsed()
   print (f"Stop without start: {e:.4f} seconds.")

   # Assert
   try:
      assert int(e)==0, f"Required 0, got {int(e)}."
      return (True)
   except AssertionError as err:
      print(f"TEST FAILED: {err}")
      return (False)

def UnitTestStartNoStop():
   # Setup
   print()
   print("Testing break case: start without stop.  Should return ~2s interval.")

   # Test
   timer=Timer()
   timer.start()
   time.sleep(2)
   e=timer.elapsed()
   print (f"Start without stop: {e:.4f} seconds.")

   # Assert
   try:
      assert int(e)==2, f"Required 0, got {int(e)}."
      return (True)
   except AssertionError as err:
      print(f"TEST FAILED: {err}")
      return (False)


# Unit Testing
def doUnitTests():
   # Register unit tests
   passed=0
   unittests=[]
   unittests.append(UnitTestPeek)
   unittests.append(UnitTestStopNoStart)
   unittests.append(UnitTestStartNoStop)

   # Execute unit tests
   for test in  unittests:
      if (test()):
         passed+=1
         print("PASSED.")

   print()
   print (f"Results: passed {passed} / {len(unittests)} unit tests.")
   print ("Testing complete.")
   print()


if (__name__=="__main__"):
   doUnitTests()

