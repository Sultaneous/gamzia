# Gamzia Utility Library for Python 3.7+

This is a module for Python, containing various specialized utilities.  This document will describe the contents and provide examples of usage.

## Import

To use a module in your Python program, simply use the following import syntax:

(Example to use the colours module; see below for details)
(Americans: Note the Canadian "our" spelling of colour)

```python
from gamzia.colours import Colours as C

from gamzia.datastructures import Stack

from gamzia.timer import Timer
```
etc...

## Modules

| Module | Classes | Summary |
| :------ | :------- | :------- |
| colours | Colours | Contains ANSI colour codes for adding colour to text |
| timer | Timer | A high performance timer, stopwatch style, for timing code execution and the like |
| accountmanager | AccountManager | An SQLITE based user/password manager, using salted hashes, for authentication purposes. |
| datastructures | Stack, Queue, BinaryTree | Contains popular computer science data structures |
| filedescriptor | FileDescriptor | Used by FBOMB protocol client/servers to get file metadata |

## API Documentation

### Timer

The timer module provides the Timer class, a simple to use high performance timer.

#### Usage examples:
``` python
from timer import Timer

my_timer=Timer()
my_timer.start()
# ... do logic here...
my_timer.stop()

# Report seconds used to 4 decimal places
print (f"Time taken: {my_timer.elapsed():.4f}")
```

#### Methods
| Method | Parameters | Summary |
|:-----|:--------|:-------|
| Timer() | None | Constructor |
| start() | None | Starts the timer |
| stop() | None | Stops the timer |
| peek() | None | Returns the current elapsed time in seconds without stopping the timer.  Returns 0 if timer hasn't been started. |
| elapsed() | None | Returns the final elapsed time in seconds.  Assumes timer is stopped.  Stops timer if it is still running. Use peek() to get time interval without stopping timer. |

