#!/usr/bin/python

# DataStructures by Karim Sultan, October 2020.

# Contains common data structures for Python.

# Chart
#                   LI     FI
#               LO  Queue  Stack
#               FO  Stack  Queue

# KSU 201014 Updated BinaryTree testing, added some aliases, implemented
#            duplicate key as update use case for insert, added toString()
#            method which had somehow been forgotten.  Still need to
#            determine if delete is to be supported (literature suggests not
#            to, or to implement a lazy delete / flagged delete.)  Added a
#            test case for find, and found typo bug (fixed).  Cleaned up enum.
# KSU 201119 Added iterators to Stack and Queue.  Iterators are destructive.  For
#            example, it will pop items off the stack until the stack is empty.
#            Added head, tail and copy to queue.  Updated unit tests.
#            NOTE: Score one for python making adding iteration a snap.  Java,
#            C#: take note!

from enum import Enum

# Constants
APP_NAME    = "DataStructures"
APP_VERSION = 1.0
APP_AUTHOR  = "Karim Sultan"
APP_DATE    = "October 2020"
APP_EMAIL   = "karimsultan@hotmail.com"
APP_BLURB   = "Library containing simple data structures for Python"
APP_SYNTAX  = "'import gamzia.datastructures' or example: 'from gamzia.datastructures import Stack'"

class TRAVERSALS(Enum):
   INORDER   = 1
   REVERSE   = 2
   PREORDER  = 3
   POSTORDER = 4

#*************************************************************************

# Classic LIFO structure
class Stack:
   def __init__(self):
      self.__stack=[]
      self.isdebug=False

      # Some convenience methods for users of other languages
      self.put=self.push
      self.take=self.pop
      self.look=self.peek
      self.set=self.push
      self.get=self.pop
      self.see=self.peek
      self.top=self.peek
      self.push_back=self.push
      self.pop_back=self.pop
      self.last=self.peek
      self.first=self.bottom
      self.reset=self.clear
      self.delete=self.clear
      self.length=self.size

   # Iter() + next() implements iterative protocol.
   # __iter__ must return an iterative object
   def __iter__(self):
      return self

   # Next must return the next item (data) in the sequence,
   # or raise the StopIteration exception.
   # Note that iterating on a queue is destructive to the stack.
   # Make a deep copy if you require the original.
   def __next__(self):
      data = self.pop()
      if (data==None):
         raise StopIteration
      else:
         return data

   # Empties stack.
   def clear(self):
      del(self.__stack)
      self.__stack=[]

   # Places item on top of stack.
   def push(self, obj):
      self.__stack.append(obj)
      if (self.isdebug):
         print(f"   Pushed {obj} onto stack. Size:  {self.size()}")

   # Removes top item from stack and returns it.
   def pop(self):
      if (self.size()>0):
         if (self.isdebug):
            print(f"   Removed top item '{self.peek()}' from stack." \
                  f"  Size: {self.size()}")
         return(self.__stack.pop())
      else:
         return(None)

   # Reveals top item on stack without discarding it.
   def peek(self):
      if self.size()>0:
         return(self.__stack[-1])
      else:
         return(None)

   # Returns the bottom item in a stack, non destructively
   def bottom(self):
      if (self.size()>0):
         return(self.__stack[0])
      else:
         return(None)

   # Returns size of stack
   def size(self):
      return  (len(self.__stack))

   # Makes a deep copy of itself
   def copy(self):
      s=Stack()
      for data in self.__stack:
         s.push(data)
      return(s)

   # Creates a string representation of stack, bottom up by default.
   # Set topdown=True for a visualization of stack from top downwards.
   def toString(self, topdown=False):
      s=""
      for value in self.__stack:
         if (topdown):
            s=f"{value}\n"+s
         else:
            s+=f"{value}\n"
      return(s)

#*************************************************************************

# Classic FIFO structure
class Queue:
   def __init__(self):
      self.__queue=[]
      self.isdebug=False

      # Some convenience methods for users of other languages
      self.add=self.enqueue
      self.append=self.enqueue
      self.queue=self.enqueue
      self.push=self.enqueue
      self.pop=self.dequeue
      self.take=self.dequeue
      self.get=self.dequeue
      self.first=self.head
      self.peek=self.head
      self.front=self.head
      self.last=self.tail
      self.back=self.tail
      self.reset=self.clear
      self.delete=self.clear
      self.length=self.size

   # Iter() + next() implements iterative protocol.
   # __iter__ must return an iterative object
   def __iter__(self):
      return self

   # Next must return the next item (data) in the sequence,
   # or raise the StopIteration exception.
   # Note that iterating on a queue is destructive to the queue.
   # Make a deep copy if you require the original.
   def __next__(self):
      data = self.dequeue()
      if (data==None):
         raise StopIteration
      else:
         return data

   # Empties queue.
   def clear(self):
      del(self.__queue)
      self.__queue=[]

   # Places item at tail of queue.
   def enqueue(self, obj):
      self.__queue.append(obj)
      if (self.isdebug):
         print(f"   Enqueued '{obj}' into queue. Size:  {self.size()}")

   # Removes head item from queue and returns it.
   def dequeue(self):
      if (self.size()>0):
         if (self.isdebug):
            print(f"   Dequeued first item '{self.__queue[0]}' from queue." \
                  f"  Size: {self.size()}")
         return(self.__queue.pop(0))
      else:
         return(None)

   # Reveals first item in queue without discarding it.
   def head(self):
      if self.size()>0:
         return(self.__queue[0])
      else:
         return(None)

   # Returns the tail item in a queue, non destructively
   def tail(self):
      if (self.size()>0):
         return(self.__queue[-1])
      else:
         return(None)
   # Returns size of queue
   def size(self):
      return  (len(self.__queue))

   # Makes a deep copy of itself
   def copy(self):
      q=Queue()
      for data in self.__queue:
         q.enqueue(data)
      return(q)

   # Creates a string representation of queue, front to back.
   def toString(self):
      s=""
      for value in self.__queue:
         s+=f"{value}\n"
      return(s)

#*************************************************************************

# A node must have a comparable key (int, str, etc...) and the data
# component is optional.  IE, if the key is the data, then data can be None.
class Node:
   def __init__(self, key, data=None):
      self.key=key
      self.data=data

   # Meant to perform a deep copy. Descendant classes should override
   # and replace with their attributes
   def copy(self):
      return(Node(self.key, self.data))

class TreeNode(Node):
   def __init__(self, key, data=None):
      self.key=key
      self.data=data
      self.leftChild=None
      self.rightChild=None

   # Creates a deep copy
   def copy(self):
      treenode=TreeNode(self.key, self.data)
      treenode.leftChild=self.leftChild
      treenode.rightChild=self.rightChild
      return(treenode)

# Binary tree construct.  Requries orderable key (int, str, etc...)
# as it is based on ordering data by comparison.
class BinaryTree:
   def __init__(self):
      self.__root=None
      self.__size=0
      self.__min=None
      self.__max=None
      self.isdebug=False

      # Convenience methods
      self.doesexist=self.exists
      self.find=self.search
      self.put=self.insert
      self.push=self.insert
      self.retrieve=self.search
      self.remove=self.delete
      self.get=self.search
      self.length=self.size
      #self.reset=self.clear

   #def clear(self):
      # TODO: Implememt delete algorithm as explained in Algorithm Book (Correl et al.)

   # Walks the tree in ascending sorted order
   def __traverseInOrder(self, node, bucket):
      if not node:
         return
      # Recurse left side of tree
      self.__traverseInOrder(node.leftChild, bucket)
      # Done left, take self as temp root
      bucket.append(node.key)
      # Append right side
      self.__traverseInOrder(node.rightChild, bucket)

   # Walks the tree in descending sorted order
   def __traverseReverse(self, node, bucket):
      if not node:
         return
      # Recurse left side of tree
      self.__traverseReverse(node.rightChild, bucket)
      # Done left, take self as temp root
      bucket.append(node.key)
      # Append right side
      self.__traverseReverse(node.leftChild, bucket)

   # Pre Order walks the tree as it is represented
   def __traversePreOrder(self, node, bucket):
      if (not node):
         return
      # Start with current node key
      bucket.append(node.key)
      # Recurse left
      self.__traversePreOrder(node.leftChild, bucket)
      # Recurse right
      self.__traversePreOrder(node.rightChild, bucket)

   # Never really knew what post order represented. May be good for
   # a deletion order of the tree, otherwise who knows. RTFM dude.
   def __traversePostOrder(self, node, bucket):
      if (not node):
         return
      # Recurse left
      self.__traversePostOrder(node.leftChild, bucket)
      # Recurse right
      self.__traversePostOrder(node.rightChild, bucket)
      # Now use current node
      bucket.append(node.key)

   # Traverses the tree by requested order.  Returns a list of
   # all values, in order defined by the TRAVERSALS enumeration.
   def traverse(self, traversalOrder=TRAVERSALS.INORDER):
      bucket=[]
      if (traversalOrder==TRAVERSALS.INORDER):
         self.__traverseInOrder(self.__root, bucket)
      elif (traversalOrder==TRAVERSALS.REVERSE):
         self.__traverseReverse(self.__root, bucket)
      elif (traversalOrder==TRAVERSALS.PREORDER):
         self.__traversePreOrder(self.__root, bucket)
      elif (traversalOrder==TRAVERSALS.POSTORDER):
         self.__traversePostOrder(self.__root, bucket)
      return(bucket)

   # Converts all node keys to string and lists them.
   # The optional parameter represents the order of rendering.
   def toString(self, traversal=TRAVERSALS.INORDER):
      l = self.traverse(traversal)
      result=""
      for s in l:
         result = f"{result}, {s}"
      if result.startswith(","):
         result=result[1::].lstrip()
      return(result)

   # Inserts a tnode by key into tree, updates size, min & max
   def insert(self, tnode):
      treenode = TreeNode(tnode.key, tnode.data)
      key=treenode.key

      if self.__root==None:
         self.__root=treenode
         self.__size+=1
         self.__min=key
         self.__max=key
      else:
         current = self.__root
         parent=None

         while True:
            parent=current

            # Start with duplicate test (update case)
            if (key == parent.key):
               parent.data = treenode.data
               return

            # Check to the left left (<)
            elif (key < parent.key):
               current = current.leftChild
               # Insert left
               if (not current):
                  parent.leftChild=treenode
                  self.__size+=1
                  # only need to check min
                  if (key < self.__min):
                     self.__min=key
                  return
            else:
               # Check to the right (>)
               current = current.rightChild
               if (not current):
                  parent.rightChild=treenode
                  self.__size+=1
                  # only need to chek max
                  if (key > self.__max):
                     self.__max=key
                  return
      return

   # Allows for quick insertion of a key when there is no associated data.
   def insertKey(self, key):
      treenode = TreeNode(key)
      return (self.insert(treenode))

   # Searchs a tree for value, returns True if found, False otherwise.
   def exists(self, key):
      current = self.__root

      if (not current):
         return False

      while (not current.key==key):
         if (current):
            if self.isdebug:
               print(f"At tree node with key: {current.key}")

            if (current.key > key):
               # Go left
               current=current.leftChild

            else:
               # Go right
               current=current.rightChild

            if (not current):
               return False

      return True

   # Searchs a tree for value, returns the node if found, None otherwise.
   def search(self, key):
      current = self.__root

      if (not current):
         return False

      while (not current.key==key):
         if (current):
            if self.isdebug:
               print(f"At tree node with key: {current.key}")

            if (current.key > key):
               # Go left
               current=current.leftChild

            else:
               # Go right
               current=current.rightChild

            if (not current):
               return None

      return(current.copy())

   # Calculates the height of left side, and right side, and returns
   # a tuple of (left height, right height). Note that the height
   # can be 0 (root only), -1(tree is null), or x (number of left/right
   # children
   # TODO: Broken (doesn't handle nested subtrees with depth)
   def getHeight(self):
      # Validate
      if (self.__root is None):
         return ((-1,-1))

      # Handle left
      leftHeight=0
      node=self.__root
      while not node.leftChild is None:
         leftHeight+=1
         node=node.leftChild

      # Handle right
      rightHeight=0
      node=self.__root
      while not node.rightChild is None:
         rightHeight+=1
         node=node.rightChild

      # Done
      return ((leftHeight, rightHeight))


   # Balances the tree.  Does this by doing an inorder (sorted)
   # traversal, then retrieving each node from the middle outwards,
   # and building a new tree.  Balancing is memory intensive.
   def balance(self):
      # TODO: NOT IMPLEMENTED
      return(None)

      # Get keys
      keys=self.traverse(TRAVERSAL.TRAVERSE_INORDER)
      # Get their node data
      nodes={}
      for key in keys:
         nodes[key]=self.search(key)
      # Split, and move outward
      mid=len(keys)//2
      steps=mid
      bst=BinaryTree()
      for i in range(1, steps):
         bst.insert(keys[mid-i], nodes[keys[mid-i]])

   # Deletes a node from the BST based on key.
   # Automatically rebalances tree.
   def delete(self, key):
      #self.__size-=1
      #reset min, max -> use inorder traversal, take 1st and last elements
      pass

   # Returns minimum value of the tree. This is maintained during
   # inserts/deletes, therefore a traversal is not required.
   def min(self):
      return(self.__min)

   # Returns maximum value of the tree. This is maintained during
   # inserts/deletes, therefore a traversal is not required.
   def max(self):
      return(self.__max)

   # Returns size (number of nodes) of the tree. This is maintained during
   # inserts/deletes, therefore a traversal is not required.
   def size(self):
      return(self.__size)

#*************************************************************************
def printBanner():
      print(f"{'*'*75}")

def testStack():
   printBanner()
   print("Class Stack: Method Tests")
   stack=Stack()
   stack.isdebug=True

   # Test push
   stack.put("alto saxophone")
   stack.set("bass guitar")
   stack.push("cello")
   stack.push("drums")

   # Test toString(), bottom up and then top down
   print(f"Bottom up view:\n{stack.toString()}")
   print(f"Top down view:\n{stack.toString(topdown=True)}")

   # Test peek, size, bottom
   print (f"Top of stack: {stack.peek()}")
   print (f"Bottom of stack: {stack.bottom()}")
   print (f"Stack size is {stack.size()}")

   # Test deep copy
   s=stack.copy()
   print(f"Is stack object the same as copy? {stack==s}")
   print(f"Is stack data the same as copy's? {stack.toString()==s.toString()}")

   # Test pop iteratively
   print (f"\nPopping all items off stack via iteration.")
   for data in stack:
      print(f"   Got: {data}")

   print (f"Stack size is {stack.size()}")

   # Test peek at empty
   print()
   print (f"Peek at empty, should be 'None': {stack.peek()}")
   print (f"Bottom of empty, should be 'None': {stack.bottom()}")

   # Test pop from empty
   print (f"Pop from empty, should be 'None': {stack.pop()}")

   # Test clear
   stack.isdebug=False  # Turn off to limit verboseness of next step
   print()
   for i in range(1000):
      stack.push(i)
   print(f"Stack size, should be 1,000: {stack.size():,}")
   print("Clearing stack...")
   stack.clear()
   print(f"Stack size, should be 0: {stack.size()}")
   print("Done testing Stack!")

def testQueue():
   printBanner()
   print("Class Queue: Method Tests")
   queue=Queue()
   queue.isdebug=True

   # Test enqueue
   queue.enqueue("alto saxophone")
   queue.enqueue("bass guitar")
   queue.enqueue("cello")
   queue.enqueue("drums")

   # Test toString()
   print(f"Front to Back view:\n{queue.toString()}")

   # Test first, last, size
   print (f"Head of queue: {queue.first()}")
   print (f"Tail of queue: {queue.last()}")
   print (f"Queue size is {queue.size()}")

   # Test deep copy
   q=queue.copy()
   print(f"Is queue object the same as copy? {queue==q}")
   print(f"Is queue data the same as copy's? {queue.toString()==q.toString()}")

   # Test iterative dequeue
   print (f"Dequeueing all items off stack via iteration...")
   for data in queue:
      print(f"   Got: {data}")

   print (f"Queue size is {queue.size()}")

   # Test peek at empty
   print()
   print (f"Head of empty, should be 'None': {queue.front()}")
   print (f"Tail of empty, should be 'None': {queue.back()}")

   # Test dequeue from empty
   print (f"Dequeue from empty, should be 'None': {queue.dequeue()}")

   # Test clear
   queue.isdebug=False  # Turn off to limit verboseness of next step
   print()
   for i in range(1000):
      queue.enqueue(i)
   print(f"Queue size, should be 1,000: {queue.size():,}")
   print("Clearing queue...")
   queue.clear()
   print(f"Queue size, should be 0: {queue.size()}")
   print("Done testing Queue!")


def testBinaryTree():
   printBanner()
   print("Class BinaryTree: Method Tests")
   tree=BinaryTree()
   tree.isdebug=True

   # Test insert
   keys=[10, 8, 16, 19, 7, 14, 18, 6, 1, 4, 20, 13, 11, 5, 3, 15, 2, 17, 9, 12]
   #keys=["alto sax", "bass guitar", "cello", "drums", "electric snare"]
   print("Inserting 20 integer keys without associated data...")
   for key in keys:
      tree.insertKey(key)
   # Test duplicate key insert
   tree.insertKey(2)

   # Test exists, min, max, size
   print("Testing if exists for 30 elements (should be 20 True, 10 False)...")
   tree.isdebug=False   # Reduce verboseness
   for i in range(1,31):
      print(f"[{i:02}] {str(tree.exists(i)):15}  ", end='')
      if (i>=3 and i%3==0):
         print()
   tree.isdebug=True

   print()
   print(f"The Size of the tree is: {tree.size()} nodes.")
   print(f"The smallest value in the tree is: {tree.min()}")
   print(f"The biggest value in the tree is: {tree.max()}")

   # Test height of tree
   h=tree.getHeight()
   print(f"Height => Left: {h[0]}   Right: {h[1]}")

   # Print order traversals (inorder, reverse, preorder, postorder)
   print()
   print(f"The tree traversed in order:\n{tree.traverse(TRAVERSALS.INORDER)}")
   print(f"The tree traversed in reverse order:\n{tree.traverse(TRAVERSALS.REVERSE)}")
   print(f"The tree traversed in pre-order:\n{tree.traverse(TRAVERSALS.PREORDER)}")
   print(f"The tree traversed in post-order:\n{tree.traverse(TRAVERSALS.POSTORDER)}")

   # Add data to a node (update) and test find
   tnode=TreeNode(17, "Why was there no '17 Candles'?")
   tree.insert(tnode)
   tnode=tree.find(17)
   print(f"Key: {tnode.key}  =  Data: {tnode.data}")

   # toString with default, and optional param
   print()
   print ("Testing toString():")
   print(f"'{tree.toString()}'")
   print ("Testing toString() reverse traversal:")
   print(f"'{tree.toString(traversal=TRAVERSALS.REVERSE)}'")

   print()
   print("Done testing BinaryTree!")

def main():
   testStack()
   testQueue()
   testBinaryTree()
   printBanner()
   print("DONE.")

if (__name__=="__main__"):
   main()

