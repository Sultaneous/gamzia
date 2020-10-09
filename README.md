# Gamzia Utility Library for Python 3+

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
| ------ | ------- | ------- |
| colours | Colours | Contains ANSI colour codes for adding colour to text |
| timer | Timer | A high performance timer, stopwatch style, for timing code execution and the like |
| accountmanager | AccountManager | An SQLITE based user/password manager, using salted hashes, for authentication purposes. |
| datastructures | Stack, Queue, BinaryTree | Contains popular computer science data structures |
| filedescriptor | FileDescriptor | Used by FBOMB protocol client/servers to get file metadata |

