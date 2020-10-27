#!/usr/bin/python

# Karim Sultan May 2020
# Timer class - acts as performance stopwatch.
# Use as follows within code:

# KSU 201010 Made field attributes private.  Made elapsed() stop
#            the timer if it is still running.  Added sanity checks.
#            Added test cases.  Added some robustness.
# KSU 201025 Added units to elapsed(). Updated test cases.  Fixed a previously
#            uknown and  rather insidious bug in timer.stop() which didn't check
#            if it had already been stopped, and would update elapsed time errantly.
# KSU 201028 Added support for nanoseconds and microseconds in timer.elapsed().
#            Updated unit test for elapsed time accordingly.
#            NOTE: The µ utf-8 character in windows is ALT-230.

# Usage:
# from timer import Timer
# timer = Timer()
# timer.start()
# ... do measurable stuff ...
# timer.stop()
# print(f"Time taken: {timer.elapsed()} seconds.")

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
      # Exit if we already stopped this timer
      if (self.__running==True):
         self.__timeStop=perf_counter()
         self.__running=False

   def elapsed(self, unit="s"):
      # Acceptable units
      units={"ns": -3, "nano":-3, "nanoseconds":-3, "µs": -2, "micro":-2, "microseconds": -2, "ms":-1,"millis":-1, "milliseconds":-1, 
             "s":0, "sec":0, "seconds":0, "m":1, "min":1, "minutes":1, "h":2, "hrs":2, "hours":2, "d":3, "days":3}

      # Sanity
      if (not unit in units.keys()):
         unit="s"
         
      # Stop if not stopped
      if (self.isRunning):
         self.stop()

      # Sanity on stop without start
      if (self.__timeStart==0):
         return(0)

      # Calculates units
      self.__timeElapsed = self.__timeStop - self.__timeStart
      nanoseconds=self.__timeElapsed*1000*1000*1000
      microseconds=self.__timeElapsed*1000*1000
      milliseconds = self.__timeElapsed*1000
      minutes = self.__timeElapsed / 60
      hours = minutes / 60
      days = hours / 24

      if units[unit]==-3:
         value=nanoseconds
      elif units[unit]==-2:
         value=microseconds
      elif units[unit]==-1:
         value=milliseconds
      elif units[unit]==1:
         value=minutes
      elif units[unit]==2:
         value=hours
      elif units[unit]==3:
         value=days
      else:
         value=self.__timeElapsed
      return (value)

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
      print(f"Time from start to now: {p:.2f}")
   x=int(p)

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
      assert 1==1, f"Should always pass"
      return (True)
   except AssertionError as err:
      print(f"TEST FAILED: {err}")
      return (False)

def UnitTestUnits():
   # Setup
   print()
   print("Testing units for elapsed time...")

   # Test
   timer=Timer()
   timer.start()
   time.sleep(2)
   timer.stop()
   print (f"Units -> nanoseconds: {timer.elapsed('ns'):,.4f}")
   print (f"Units -> microseconds: {timer.elapsed('µs'):,.4f}")
   print (f"Units -> milliseconds: {timer.elapsed('ms'):,.4f}")
   # Deliberately use break case here, should default to seconds
   print (f"Units -> seconds: {timer.elapsed('asdf'):,.4f}")
   print (f"Units -> minutes: {timer.elapsed('min'):,.4f}")
   print (f"Units -> hours: {timer.elapsed('hours'):,.4f}")
   print (f"Units -> days: {timer.elapsed('d'):,.5f}")

   # Assert
   try:
      assert 1==1, f"Should always pass"
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
   unittests.append(UnitTestUnits)

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

