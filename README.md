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
| [colours](#info_colours) | Colours | Contains ANSI colour codes for adding colour to text |
| [timer](#info_timer) | Timer | A high performance timer, stopwatch style, for timing code execution and the like |
| [accountmanager](#info_accountmanager) | AccountManager | An SQLITE based user/password manager, using salted hashes, for authentication purposes. |
| [datastructures](#info_datastructures) | Stack, Queue, BinaryTree | Contains popular computer science data structures |
| [filedescriptor](#info_filedescriptor) | FileDescriptor | Used by FBOMB protocol client/servers to get file metadata |

## API Documentation

### <a id="info_timer">Timer</a>

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

# Report microseconds; could also use unit=micros
print (f"Time taken: {my_timer.elapsed("µs"):.2f}")

# Report hours; could also use unit=h
print (f"Time taken: {my_timer.elapsed("hours"):.2f}")
```

#### Methods
| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| Timer() | None | Class instance | Constructor |
| start() | None | nothing | Starts the timer |
| stop() | None | nothing | Stops the timer |
| peek() | **Optional** unit=seconds; choices are "ns\|µs\|ms\|s\|m\|h\|d" or "nanoseconds\|microseconds\|milliseconds\|seconds\|minutes\|hours\|days" | Returns the current elapsed time in seconds without stopping the timer.  Returns 0 if timer hasn't been started. | Peeks at current time elapsed on timer |
| elapsed() | **Optional** unit=seconds; choices are "ns\|µs\|ms\|s\|m\|h\|d" or "nanoseconds\|microseconds\|milliseconds\|seconds\|minutes\|hours\|days" | Returns the final elapsed time in seconds, or in the requested unit type. | Stops timer if it is still running. Use peek() to get time interval without stopping timer. |

#### Misc

Running the following:
``` bash
python timer.py
```

...will execute the Timer unit test cases.

***

### <a id="info_colours">Colours</a>

Colours provides ANSI colour codes for formatting text strings with colour adornments. 

**NOTE: In Windows 10, ANSI colour is NOT supported in DOS CMD nor PowerShell terminals, and therefore cannot be used. However, compatibility is kept by instead substituting empty strings ("") for the ANSI code, so coloured text strings will render properly under an ANSI Unix terminal but will not clutter / break a Windows terminal. Not all styles are supported by terminals; YMMV.**

Colours are identified with a 3-4 letter foreground code (cxx), background code (bxx), or style code (sxx).  Colours can be turned off (reverting to terminal default) with "coff" (Colour OFF), "boff" (Background OFF), the generic "off" (foreground & background off). Styles need to be turned off individually.

**NOTE:** ANSI colouring supports **16 colours** as listed below:

![Colour List](https://github.com/Sultaneous/gamziatools/blob/main/docs/colour_list.png)

**NOTE:** You can have 1 active foreground colour, 1 active background colour, and multiple active styles (for example, bold and underline).

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

**Note:** All format strings can be accessed statically, ie: Colours.clr, etc... and no instantiation of the Colours class is necessary.

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

##### Example of Foreground, Background Colour Combinations:

![Colour Grid](https://github.com/Sultaneous/gamziatools/blob/main/docs/colour_list.png)

***

### <a id="info_accountmanager">AccountManager</a>

The AccountManager class is intended to provide a simple way to incorporate authentication into an app. For example, in a client-server paradigm,
a login may be required prior to providing services.  Account management is a repetitive pattern that is covered with this class.

The programmer can quickly incorporate a user database with salted hash passwords.  For security reasons, the actual or "plain-text" password is not
stored. Instead, the SHA256 secure hash algorithm is used to create a hash, which is formed from the input of the user name (the salt) and the password.
This hash is stored in the database, and for future comparisons, the salted hash is first recreated and then the hashes are compared.

AccountManager uses an sqlite database, which is a local binary file.  Queries employ the use of parameterization to harden it against SQL injection
attacks.  The programmer provides the database name, hence a database can be isolated to a single app or shared among several apps.

The **sqlite3 library** must be installed first to use this class:
```bash
pip install sqlite3
```

#### Usage examples:
``` python
from accountmanager import AccountManager
```
Or, if using from gamzia folder, use:
``` python
from gamzia.accountmanager import AccountManager
```
``` python
# Create a schema / or open existing one
mgr=AccountManager("users.db")

# Add three test users
mgr.addUser("Admin","Adminpassword")
mgr.addUser("Guest","Anonymous")
mgr.addUser("Test","debug")

# Load all users
print(mgr.listUsers())

# Create a saltedhash to compare input with DB and verify password
saltedhash = AccountManager.saltPassword("Guest","Anonymous")
if (mgr.verifyPassword("Guest",saltedhash)):
   print("Password verified")
else:
   print("Verification failed")

# Change the password on account "Test", load before and after
print(mgr.getUser("Test"))
mgr.updatePassword("Test","newpassword")
print(mgr.getUser("Test"))

# Remove user "Test" from db
mgr.deleteUser("Test")
```

**NOTE:** User names are unique, case insensitively. Thus "User" and "user" are considered the same and not permitted.  This constraint is enforced at the database
level as part of the schema.  User name cannot be NULL.  Password cannot be NULL.

#### Methods

| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| AccountManager() | **_(Optional)_** Database file name.  If not provided, uses default, "**accounts.db**" | Class instance | Constructor.  Takes optional db file name.  If the db does not exist, it creates the schema, otherwise it opens it for read/write access. |
| doesUserExist() | string user name | True if user exists in database, False otherwise | Checks if a user already exists in database. |
| addUser() | string user name; string password | True on success, False otherwise | Adds a new user record with salted, hashed password to database. |
| listUsers() | **None** | Returns a list of tuples, where each tuple is the equivalent of 1 record from the accounts table. | The fields in a record are ID (integer), Username (String), Password (String) and CreationDate (String, date/time format).  If the table is empty, an empty list is returned. |
| getUser() | string user name | Returns a tuple containing the complete user record, or **None** if no record found. | Always check for **None** in case user wasn't in the db. This can be avoided with a call to doesUserExist() before calling getUser(). |
| getPassword() | string user name | Returns the password entry for the specified user, or **None** if user not found. |  Password value is the salted, SHA256 hash value of the original password. Plain-text passwords are not stored.  Passwords are salted with the User name (the salt value is not secret). |
| updatePassword() | string user name, string newpassword | True on success, False otherwise. | **NOTE** The class will salt and hash the password, so you need only provide the plain-text version of the password to this method. |
| deleteUser() | string user name | True if successful, False otherwise | Deletes user from database.  **NOTE** If user doesn't exist, it returns False as nothing was deleted. Again, the programmer can avoid ambiguity on the meaning of a False return value (ie, user didn't exist, or DB error occurred) by first calling doesUserExist(). |
| verifyPassword() | string user name, string value to test | Returns True if user's salted hash password value matches the value provided, False if not. | **NOTE** This requires that the value you test is the salted pasword hash and not the plain text password.  See saltPassword() below for how to do this, and see the usage examples above for a code example. |
| **Static** AccountManager.saltPassword() | string user name, string plain-text password | Returns a string containing the salted, SHA256 password hash | **NOTE** This is a static method that can be used anytime without a class instance.  The user name is required, as it is the salt value that is used (the salt value is not secret).|

#### Misc

Running the following:
``` bash
python accountmanager.py
```

...will execute the AccountManager unit test cases.

***

### <a id="info_datastructures">Data Structures</a>

The Data Structure module contains multiple classes representing basic computer science data structures. You can easily add a stack to your programs, for example, using this module. Please see the usage examples below along with the method reference for more details.  Examples of using these data structures can be found in the module's unit tests.

Currently supported data structures include **[Stack](#info_stack) (LIFO), [Queue](#info_queue) (FIFO), and [BinaryTree](#info_binarytree)**.  More structures, such as AVL Trees, Red/Black Trees, and Priority Queues (Heaps) are intended.

#### Usage examples:
``` python
from datastructures import Stack, Queue, BinaryTree, TRAVERSALS
```
Or, to include all classes and enums:
``` python
from datastructure import *
```
Or, if using the gamzia package:
``` python
from gamzia.datastructures import *
```
Further usage examples are provided per class below.

---
### <a id="info_stack">Stack</a>

Stacks work like piles; you "push" an element onto the stack and it goes on the top of the pile.  You can "pop" an element off of the stack and it will return the element at the top, while at the same time removing it from the stack. This creates a last-in, first-out structure (**LIFO**).  You can "peek" at the top of the stack, or the "bottom" of the stack, which in both cases returns the element at that location without removing it (pop is always destructive).  Stacks are ordered by the order of element entry, and unsorted.

**Note** The Stack class supports the str() and len() commands. The Stack class supports iteration, returning the top data item each iteration, until the stack is empty. This type of iteration is destructive. If you want to preserve the stack, please make a copy via **stack.copy()** first.

``` python
# Iteration example
stack = Stack()
stack.push ("Alligator")
stack.push ("Bear")
stack.push ("Cat")

# Copy it first
stack_cp = stack.copy()

# Iterate top to bottom (Cat->Alligator)
for data in stack_cp:
   print(data)
   
# The copy is empty now:
print (len(stack_cp))

# But the original is preserved:
print (len(stack))
```

#### Methods
| Method | Alias(es) |Parameters | Returns | Summary |
|:-----|:--------|:--------|:-------|:-------|


#### Methods
| Method | Alias(es) |Parameters | Returns | Summary |
|:-----|:--------|:--------|:-------|:-------|
| Stack() | None | None | Class instance | Creates an empty stack structure. |
| clear() | reset(), delete() | None | nothing | Removes all elements from the stack, resetting it. |
| push() | put(), set(), push_back() | Object | nothing | nothing | Places an object element on the top of the stack. |
| pop() | take(), get(), pop_back() | None | The top element of the stack, or None if stack is empty | Removes and returns the top stack element if there is one. |
| peek() | look(), see(), top(), last() | None | The top element of the stack, or None if stack is empty | Returns the top stack element, without removing it, if there is one. |
| bottom() | first() | None | The last element of the stack, or None if stack is empty | Non-destructive. It's like peek for the bottom, or first, element. |
| size() | length() | None | The integer count of elements in the stack | Determines the size of the stack in elements. |
| toString() | None | **optional** topdown=True | A string representation of the stack, when possible. | Converts all elements to string and lists them.  Won't work when elements are complex objects. The optional parameter topdown represents the order of rendering; it is a boolean with the default being **True** (print from the top to the bottom). |

#### Examples

Example of creating a stack, pushing 4 elements onto it, and then popping them off.
``` python
from gamzia.datastructures import Stack

# Create empty stack
stack=Stack()

# Add four items
stack.push("Earth")
stack.push("Mars")
stack.push("Jupiter")
stack.push("Saturn")

# Display current stack
print ("Stack:",stack.toString())

# Get the size
print("Size:",stack.size())

# Peek at the top and bottom items
print("Top:",stack.peek())
print("Bottom",stack.bottom())

# Remove a couple of elements
s = stack.pop()
s = stack.pop()

print("Top:",stack.peek())
print("Bottom:",stack.bottom())
print("Size:",stack.size())
print("Stack:",stack.toString())

# Clear it
stack.clear()
print("Size after clear:",stack.size())

```

#### Misc

Running the following:
``` bash
python datastructures.py
```

...will execute the datastructure unit test cases, which test all the data structures in the module.

### <a id="info_queue">Queue</a>

Queues are lines; picture a queue as a linear buffer. When you "enqueue" and element, it enters the line at the next available position.  You can "dequeue" an element, which removes the first element (head) in the queue and returns it.  This creates a first-in, first-out structure (**FIFO**).  You can "peek" at the head of the queue, or the tail element of the queue, which in both cases returns the element at that location without removing it ("dequeue" is always destructive).  Queues are ordered by the order of element entry, and are unsorted.

Whereas Stacks have a "top to bottom" (up/down) organization, a queue has a "head to tail" or "front to back" (left/right) orientation.

**Note** The Queue class supports the str() and len() commands. The  Queue class supports iteration, dequeueing the head data item each iteration, until the  queue is empty. This type of iteration is destructive. If you want to preserve the queue, please make a copy via **queue.copy()** first.

``` python
# Iteration example
queue = Queue()
queue.enqueue ("Alligator")
queue.enqueue ("Bear")
queue.enqueue ("Cat")

# Copy it first
queue_cp = queue.copy()

# Iterate head to tail (Alligator->Cat)
for data in queue_cp:
   print(data)
   
# The copy is empty now:
print (len(queue_cp))

# But the original is preserved:
print (len(queue))
```

#### Methods
| Method | Alias(es) |Parameters | Returns | Summary |
|:-----|:--------|:--------|:-------|:-------|
| Queue() | None | None | Class instance | Creates an empty queue structure. |
| clear() | reset(), delete() | None | nothing | Removes all elements from the queue, resetting it. |
| enqueue() | push(), add(), append() | Object | nothing | nothing | Places an object element at the end (last) of the queue. |
| dequeue() | pop(), take(), get() | None | The first element of the queue, or None if queue is empty | Removes and returns the front (first) queue element if there is one. |
| first() | peek(), front() | None | The first element of the queue, or None if queue is empty | Returns the front queue element, without removing it, if there is one. |
| last() | back() | None | The last element of the queue, or None if queue is empty | Non-destructive. It peeks at the end of the line. |
| size() | length() | None | The integer count of elements in the queue | Determines the size of the queue in elements. |
| toString() | None | None | A string representation of the queue, when possible. | Converts all elements to string and lists them.  Won't work when elements are complex objects.  Orientation is front to back. |

#### Examples

Example of creating a queue, enqueueing 4 elements into it, and then dequeueing them.
``` python
from gamzia.datastructures import Queue

# Create empty queue
queue=Queue()

# Add four items
queue.enqueue("Earth")
queue.enqueue("Mars")
queue.enqueue("Jupiter")
queue.enqueue("Saturn")

# Display current queue
print ("Queue:",queue.toString())

# Get the size
print("Size:",queue.size())

# Peek at the first and last items
print("Top:",queue.first())
print("Bottom",queue.last())

# Remove a couple of elements
s = queue.dequeue()
s = queue.dequeue()

print("Top:",queue.first())
print("Bottom:",queue.last())
print("Size:",queue.size())
print("Stack:",queue.toString())

# Clear it
queue.clear()
print("Size after clear:",queue.size())

```

#### Misc

Running the following:
``` bash
python datastructures.py
```

...will execute the datastructure unit test cases, which test all the data structures in the module.

### <a id="info_binarytree">BinaryTree</a>

BinaryTrees are a special form of tree structure, where each node can have a maximum of two children.  It uses an ordered insertion, and as such is an ordered, sorted tree. Because of this, insertion in the worse case scenario can take **O(n)** processing time, but retrieval is guaranteed to taken no more than **O(log n)** processing time, thus is extremely fast.  In fact, a binary search is the fastest search algorithm in computer science.

The reason BinaryTrees can take so long to insert is that they can become "unbalanced".  A special type of binary tree, called an AVL tree, automatically rebalances the tree when necessary.  

BinaryTrees contain data in TreeNode structures. TreeNodes consist of a key and a value.  The key is usually an integer ordinal, or a string label, while the value can be any data, including other complex objects (for example, you could have a tree of queues, which is known as a B-Tree).  To use the BinaryTree, one first creates a TreeNode, populates it, and then inserts it into the tree.  Usage examples are provided below.

BinaryTrees can be traversed in four manners: inorder (ascending sorted), reverse inorder (descending sorted), preorder (left biased) and postorder (right biased). An enumeration called **TRAVERSALS** is provided containing reference names for the traversal method used with the toString() method.

**NOTE:** An advanced method of using BinaryTrees in Python is supported, in which multiple keys can reference the same data without duplicating the data.  This is a many:one relationship, and to do this, one must use the Datum class to store their data, and add the Datum object to the TreeNode for each key that is meant to refer to it.  This is facilitated with the **BinaryTree.insertManyKeys(keylist, datum)** method.

#### Enumeration: Traversals

``` python
class TRAVERSALS(Enum):
   INORDER   = 1
   REVERSE   = 2
   PREORDER  = 3
   POSTORDER = 4
```

**Note** The BinaryTree class supports the str() and len() commands. The BinaryTree class does not directly support iteration, as this action is undefined for the structure.  However, iteration can still be achieved by returning a list of keys in the desired traversal using **traverse()** and then iterating the keys and using **search()**:

``` python
# Iteration example
# Stuff tree with dummy keys
tree = BinaryTree()
for i in range(20):
   tree.insertKey(i)

# Iterate keys:
for key in tree.traverse(TRAVERSALS.INORDER):
   node=tree.search(key)
   
   # There is no data in our node, but this is how you would access it if there were
   print(f"Node key: {node.key}  |  Node data: {node.data})
   
# Prove it was non-destructive:
print ("Size of tree is:", len(tree))
```

#### Methods

##### TreeNode Class
The Key-Data combination is a dictionary pattern, same as a key-value pair.
| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| TreeNode() | integer or string key, **optional** object data | Class instance | Inherits from Node; contains BinaryTree specific node values. |
| copy() | None | A deep copy of TreeNode object | Performs a deep copy, creating a new instance with identical contents. |

##### BinaryTree Class
| Method | Alias(es) |Parameters | Returns | Summary |
|:-----|:--------|:--------|:-------|:-------|
| BinaryTree() | None | None | Class instance | Creates an empty stack structure. |
| insert() | put(), push() | TreeNode | nothing | Inserts a new treenode into the binary tree, based on **treenode.key** |
| insertKey() | None | string or integer Key | nothing | Like insert(), but only inserts a key, without associated data. |
| exists() | doesexist() | string or integer Key | True if key is in binary tree, False otherwise | Searches nodes to see if one with the specified key exists |
| search() | find(), retrieve(), get() | string or integer Key | Returns the tree node with the associated key, or None if not found | Non-destructive. |
| traverse() | None | **optional** traversal=TRAVERSALS.INORDER | A list of binary tree node keys in the order requested. | The optional parameter traversal represents the order of rendering; the default is **TRAVERSALS.INORDER** (prints sorted, ascending). |
| min() | None | None | The lowest key value in the tree. | The min value is tracked during an insert, so this call is heavily optimized. |
| max() | None | None | The highest key value in the tree. | The max value is tracked during an insert, so this call is heavily optimized. |
| size() | length() | None | The integer number of nodes in the binary tree. | This method is fully optimized for speed; counting is done on insert operations. |
| toString() | None | **optional** traversal=TRAVERSALS.INORDER | A string representation of the binary trees keys. | Converts all node keys to string and lists them.  The optional parameter traversal represents the order of rendering; the default is **TRAVERSALS.INORDER** (prints sorted, ascending). |

##### Not Implemented:
  * delete()  
  Delete is a precarious operation in trees.  It can unbalance them, and can take significant  time to complete.  Most of the literature recommends avoiding deletes or using a lazy delete style.  Ideally, the delete would both remove the node, chain the parent node with children nodes, and then rebalance the tree.  Also, some initial testing showed issues with Python not freeing up deleted nodes if a reference was left to them, so it must be implemented cautiously. **FUTURE IMPLEMENTATION**
  * getHeight()  
  Only has a partial implementation. Returns a tuple of (left height, right height) from the root node.  Do not rely on this method!  The current implementation is incomplete; it calculates the height of the extreme left branch and the extreme right branch, but nested children may extend the height to deeper levels and they are currently ignored.  **FUTURE IMPLEMENTATION**
  * clear()  
  Since this would require sequentially deleting all nodes (bottom - up), and delete is not implemented, neither is clear().  However, this is simply done by just recreating a new class instance:
  ``` python
  bst=BinaryTree()
  bst.insert(20)
  bst.insert(10)
  bst.insert(30)
  
  # Clear bst:
  bst=BinaryTree()
  ```
  This approach will ensure Python memory management handles frees the old tree and associated nodes.  **FUTURE IMPLEMENTATION**

#### Examples

Example of creating a binary tree, inserting 4 nodes (keys with data) into it, finding and updating them.
``` python
from gamzia.datastructures import BinaryTree, TreeNode, TRAVERSALS

# Create empty binary search tree
bst=BinaryTree()

# Add four items, string keys with string data
tnode=TreeNode("Earth", "3rd Rock from the Sun")
bst.insert(tnode)

tnode=TreeNode("Mars", "Red dusty desert.")
bst.insert(tnode)

tnode=TreeNode("Jupiter", "Fat planet with killer storms.")
bst.insert(tnode)

tnode=TreeNode("Saturn", "If you like it, put a ring on it")
bst.insert(tnode)

# Display current bst tree, sorted ascending (TRAVERSALS.INORDER is the default)
print ("Binary Tree:",bst.toString())

# Display current BST tree, sorted descending
print ("Binary Tree:",bst.toString(traversal=TRAVERSALS.REVERSE))

# Get the size
print("Size:",bst.size())

# Get the data for Earth and Saturn
tnode=bst.find("Earth")
print(f"Key: {tnode.key}  |  Data: {tnode.data}")

tnode=bst.find("Saturn")
print(f"Key: {tnode.key}  |  Data: {tnode.data}")

# Update Earth data, display
tnode=TreeNode("Earth", "This is new data for Earth, demonstrating an update operation.")
bst.insert(tnode)
tnode=bst.find("Earth")
print(f"Key: {tnode.key}  |  Data: {tnode.data}")

# Show min and max values:
print("Min:",bst.min())
print("Max:",bst.max())

# Clear it
bst=BinaryTree()
print("Size after clear:",bst.size())
```

#### Misc

Running the following:
``` bash
python datastructures.py
```

...will execute the datastructure unit test cases, which test all the data structures in the module.

***

## <a id="info_filedescriptor">FileDescriptor</a>

The FileDescriptor class was a purpose built class for implementation of the [FBomb](https://www.github.com/Sultaneous/fbomb) file-transfer protocol.  However, when building clients and servers supporting FBomb, it became useful to break out FileDescriptor as a generic class for quick adoption.

FileDescriptor assembles important metadata about a particular file in the file system. It is quickly transformed into a simple JSON representation, and the serialized JSON is easily sent over the network between client and server.  The same logic was replicated in C# to produce a C# FBomb client which seamlessly communicates with a Python based FBomb server.

To create the JSON object, first the class fields are populated, after which reflection is used to extract the public value attributes and create a dictionary. Python's JSON library handles dictionaries quite well, and outputs the JSON string.  Deserialization is done via a static factory method, which converts the JSON representation back to a dictionary and then dynamically populates a new FileDescriptor instance with the values (again, using reflection style techniques).

#### Usage examples:
``` python
from filedescriptor import FileDescriptor as FD
```
Or, if using the gamzia package:
``` python
from gamzia.filedescriptor import FileDescriptor as FD
from gamzia.filedescriptor import FILEMODE, HASHTYPE
```
``` python
# Create an instance
fd=FD()

# populate with file meta data for "temp.txt"
if (not fd.populate("temp.txt")):
  print("Error! Does file exist?")
  exit()
  
# Change file type to ASCI (defaults to binary).
fd.filemode=FILEMODE.ASCII

# Serialize it
s=fd.serialize()
print (s)

# Create a new instance from JSON string
fd2=FD.deserialize(s)

# Show that they are different objects
print(f"fd = fd2?  {fd==fd2}")

# Show that the JSON strings are the same
print(f"Json(fd) = Json(fd2)?  {fd.serialize()==fd2.serialize()}")

# Display second object instance
print(fd2.toString())
```

#### Enums

FileDescriptor implements two enumerations. Note that they use multiple inheritance, as Enums can't be JSON serialized, but strings can.

```python
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
```

#### Methods
| Method | Parameters | Returns | Summary |
|:-----|:--------|:-------|:-------|
| FileDescriptor() | None | Class instance | Constructor |
| populate() | string filename | True on success, False otherwise (usually due to file does not exist errors). | Assembles the meta data and SHA256 hash for the specified file. |
| serialize() | None | A JSON string | Creates a JSON representation of the object instance, using only its public value attributes. |
| **static** deserialize() | None | A new FileDescriptor class instance, poulated | This is a static, factory method for creating objects from JSON strings. |
! toDictionary() | None | A dictionary representation of object instance | Adds only entries for public value attributes. |
| toString() | None | A string representation of object instance | Displays public value attributes only. |

#### Misc

Running the following:
``` bash
python filedescriptor.py
```

...will execute the FileDescriptor unit test cases.

***
