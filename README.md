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
```
Or, if using the gamzia package:
``` python
from gamzia.timer import Timer
```
``` python
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

#### Misc

Running the following:
``` bash
python timer.py
```

...will execute the Timer unit test cases.

### Colours

Colours provides ansi colour codes for formatting text strings with colour adornments. 

**NOTE: In Windows 10, ANSI colour is NOT supported in DOS CMD nor PowerShell terminals, and therefore cannot be used. However, compatibility is kept by instead substituting empty strings ("") for the ANSI code, so coloured text strings will render properly under an ANSI Unix terminal but will not cluter / break a Windows terminal. Not all stlyes are supported by terminals; YMMV.**

Colours are identified with a 3-4 letter foreground code (cxx), background code (bxx), or style code (sxx).  Colours can be turned off (reverting to terminal default) with "coff" (Colour OFF), "boff" (Background OFF), the generic "off" (foreground & background off). Styles need to be turned off individually.

NOTE: ANSI colouring supports 16 colours as listed below.

NOTE: You can have 1 active foreground colour, 1 active background colour, and multiple active styles (for example, bold and underline).

#### Usage examples:
``` python
from colours import Colours as C
```
Or, if using from gamzia folder, use:
``` python
from gamzia.colours import Colours as C
```
``` python
print(f"{C.clc}This is in light cyan.{C.off} This is back to normal.")
print(f"{C.cly}{C.bdr}This is light yellow foreground on a dark red background.")

s=f"{C.clb}This is blue text and this is {C.clg}{C.bdg}green on dark green.")
print("With colour: "+s)
print("Without colour: "+Colours.cstrip(s))
```

Note that to effectively use text colouring, you simply insert the text format string in the appropriate location in the string to enable it.
One does not need to turn off the colour before applying a new colour; the previous colour/background/style remains in effect until overwritten or turned off.

#### Methods

| Method | Parameters | Summary |
|:-----|:--------|:-------|
| cstrip | Colour formatted string | This is the only method in the class. It strips all ANSI colour codes out of a string, returning the 'clean' string. It is a static method so can be called without a class instance, ie: Colours.cstrip()|

##### Foreground (Text) Colour Strings
| String | Meaning |
|:------ | :------ |
| cbl | Foreground colour black |
| cdr | Foreground colour dark red |
| cdg | Foreground colour dark green |
| cdy | Foreground colour dark yellow / brown |
| cdb | Foreground colour dark blue |
| cdm | Foreground colour dark magenta |
| cdc | Foreground colour dark cyan |
| cdgy | Foreground colour dark gray |
| clgy | Foreground colour light gray |
| clr | Foreground colour light red |
| clg | Foreground colour light green |
| cly | Foreground colour light yellow |
| clb | Foreground colour light blue |
| clm | Foreground colour light magenta |
| clc | Foreground colour light cyan |
| cwh | Foreground colour light white |
| **coff** | Foreground colour **off** |

##### Background (Reverse) Colour Strings
| String | Meaning |
|:------ | :------ |
| bbl | Background colour black |
| bdr | Background colour dark red |
| bdg | Background colour dark green |
| bdy | Background colour dark yellow / brown |
| bdb | Background colour dark blue |
| bdm | Background colour dark magenta |
| bdc | Background colour dark cyan |
| bdgy | Background colour dark gray |
| blgy | Background colour light gray |
| blr | Background colour light red |
| blg | Background colour light green |
| bly | Background colour light yellow |
| blb | Background colour light blue |
| blm | Background colour light magenta |
| blc | Background colour light cyan |
| bwh | Background colour light white |
| **boff** | Background colour **off** |

##### Style (Effect) Colour Strings
| String | Meaning |
|:------ | :------ |
| sbo | Style Bold |
| sdi | Style Dim |
| sun | Style Underline |
| sbl | Style Blink |
| sre | Style Reverse |
| shi | Style Hidden |
| sbof | Style Bold Off |
| sdif | Style Dim Off |
| sunf | Style Underline Off |
| sblf | Style Blink Off |
| sref | Style Reverse Off |
| shif | Style Hidden Off |
| **soff** | Style effect **off** |

##### Other (Macro) Colour Strings
| String | Meaning |
|:------ | :------ |
| off | Foreground & Background off |
| no | Foreground light yellow, background dark red |
| yes | Foreground light green, background dark green |
| old | Foreground light yellow, background dark blue |
| retro | Foreground white, background black |
| paper | Foreground black, background white |

#### Misc

Running the following:
``` bash
python colours.py
```

...will execute the Colours unit test cases.


