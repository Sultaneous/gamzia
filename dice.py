import random
from gamzia.datastructures import Stack, Queue

# Karim Sultan 2021 08 12
# Adapted from C# version, DiceResolver.cs by Karim Sultan, 2019.
# Integer based Reverse Polish Notation resolver.
# Converts infix notation to RPN notation.
# Evaluates outcome.
# Enforces order of operations, accepts 'd' operator (dice roll), and handles brackets.
# Does not work with floating point. Although trivial to adjust for floating point,
# the use of integers only was a design decision for dice management.

# Typical use:
# MATH: "(12+2^3)/10*8%5" would resolve to 1.
# Dice: "3d6" would resolve to the range 3-18.
# Mixed: "2d4 + 3d6 - 1" would resolve to the range 4-25.
# Faulty: "(9*7" = 0 or "*oas" = 0 (error always returns 0).

class DiceResolver:
   def __init__(self):
      # BEDMAS ==> d()^/%*+-
      self.precedence = {
         "(": 0,
         "+": 3,
         "-": 3,
         "/": 5,
         "*": 5,
         "%": 5,
         "^": 7,
         "d": 9
      }
      self.s = Stack()
      self.q = Queue()
      self.error = False

   def infixToRPN(self, expression):
      num = ""

      for c in expression:
         token=str(c)

         if (num!="" and not token.isnumeric()):
            self.q.enqueue(num)
            num=""

         if (token=="("):
            self.s.push(token)

         elif (token==")"):
            # pop up until the bracket
            while (self.s.peek()!="("):
               self.q.enqueue(self.s.pop())

            # pop the bracket
            self.s.pop()

         # operator handling
         elif (token in self.precedence):
            while self.s.size() !=0 and (self.precedence[token] <= self.precedence[self.s.peek()]):
               self.q.enqueue(self.s.pop())
            self.s.push(token)

         elif (token.isnumeric()):
            num += token

      # Did we end on a number?
      if (num != ""):
         self.q.enqueue(num)

      # Now pop items from stack to the queue to cleanup
      while (self.s.size() != 0):
         self.q.enqueue(self.s.pop())


   def calculate(self, left, right, op):   
      if (op == "+"):
         return (left + right)

      elif (op == "-"):
         return (left - right)

      elif (op == "*"):
         return (left * right)

      elif (op == "/"):
         return (int(left / right))

      elif (op == "^"):
         return (left**right)

      elif (op == "%"):
         return (left % right);

      # dice roll
      elif (op == "d"):
         sum = 0;

         for i in range(left):
            sum+=random.randint(1, right);
         return (sum);

      # whoops shouldn't have happened try to be graceful
      return (0);

   def evaluateRPN(self):
      workstack=Stack()

      # As we pull tokens from the queue, we validate them and if neither a number
      # nor an operator, we abort with an error.
      for t in self.q:
         if (t in self.precedence):
            right=workstack.pop()
            if (not str(right).isnumeric() and not right in self.precedence):
                print(f"Error {right} is invalid token.")
                self.error=True
                break

            left=workstack.pop()
            if (not str(left).isnumeric() and not left in self.precedence):
                self.error=True
                break
               
            workstack.push(self.calculate(left, right, t))
         else:
            workstack.push(int(t))

      # answer is now on the stack
      if (not self.error):
         return (workstack.pop())
      else:
         return (0)


   def resolve(self, expression):
      self.error=False
      self.q.clear()
      self.s.clear()
      self.infixToRPN(expression)
      return (self.evaluateRPN())
   

def test():
   dice = DiceResolver()
   p=""
   while True:
      x=input(f"Enter expression to resolve, 'q' to quit [{p}]: ")
      if x=="q" or x=='Q':
         break
      if (x!=""):
         p=x         
      print(dice.resolve(p))
   return

# Interactive testing
#if __name__ == "__main__":
#   test()



