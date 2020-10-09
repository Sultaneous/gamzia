#!/usr/bin/python

# Karim Sultan May 2020
# Timer class - acts as performance stopwatch.
# Use as follows within code:

# from timer import Timer
# timer = Timer()
# timer.start()
# ... do measurable stuff ...
# timer.stop()
# print(f"Time taken: {timer.elapsed} seconds.")

from time import perf_counter

# Small timer class to handle performance timing
class Timer():
   timeStart = timeStop = timElapsed = 0
   running = False

   def __init__(self):
      self.timeStart=0
      self.timeStop=0
      self.timeElapsed=0
      self.running=False

   def start(self):
      self.running=True
      self.timeStart=perf_counter()

   def stop(self):
      self.timeStop=perf_counter()
      self.running=False

   def elapsed(self):
      if (self.timeStop<self.timeStart):
         self.timeElapsed = perf_counter() - self.timeStart
      else:
         self.timeElapsed = self.timeStop - self.timeStart
      return (self.timeElapsed)

   def peek(self):
      if (self.isRunning()):
         return (perf_counter()-self.timeStart)
      else:
         return (0)

   def isRunning(self):
      return(self.running)
#End of class
###########################################################################
