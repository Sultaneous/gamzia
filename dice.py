import random
from datastructures import Stack, Queue

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

# The DiceResolver class is an infix expression resolver,
# which handles order of operations (Using the Canadian BEDMAS rule
# and not the American PEMDAS rule - although the outcomes are
# necessarily the same under either rule, there is an implemntation
# difference).  NOTE: Current implementation doesn't care - uses both.
# rolls dice on a 'd' operator (ie, to roll a 6 sided die once, use 1d6)
# and optionally can create a histogram with mean, mode, and 
# frequency chart.

# KSU 210814 Added '!' (factorial) operator; precedence is debatable,
# since it isn't in the BEDMAS rule, but mathematicians peg it between
# brackets and exponents.

# KSU 210814 Added "C" for choose (combinatorics).
# Set the priority to same as multiplication (via formula expansion).

# KSU 210816 Added getHistogram() which provides a heuristic analysis
# of a particular dice roll.
class DiceResolver:
   def __init__(self):
      
      # BEDMAS ==> d()!^/%*+-
      # PEMDAS ==> d()!^*/%+-
      # Precedence weighting reflects rule; higher means priority
      # Close bracket ')' not included; it is a special case (collapses stack to '(')
      self.precedence = {
         "(": 0,
         "+": 3,
         "-": 3,
         "/": 5,
         "*": 5,
         "%": 5,
        "C": 5,
         "c": 5,
         "^": 7,
         "!": 8,
         "d": 9
      }
      
      # 's' is a stack used for rearranging infix arguments
      self.s = Stack()
      
      # 'q' is a queue used to store the postfix arguments
      self.q = Queue()
      self.error = False

   # Converts a valid infix expression (mathematical expression)
   # to postfix using Reverse Polish Notation (RPN). Infix exp-
   # ression must be valid; this function can not check validi-
   # ty.  Note that by design, this only supports integer expr-
   # ession (no floating point support). FP support can be add-
   # ed if while building numbers, the '.' character is accepted.

   # Example: Expression="1 + 2 * 3"  --> 7, NOT 9
   # RPN="1 2 3 * +"  --> 7
   # Note that the order of operations is preserved in the RPN.
   def infixToRPN(self, expression):
      
      # Since a number may be multiple characters, we start with an empty string,
      # and while each character is numeric, we append the number until a non-
      # numeric value is encountered.
      num = ""

      # Tokenize expression character by character
      for c in expression:
         token=str(c)

         # Case: we had accumulated a number but this character is not a
         # numeric value; so save accumulated number, and reset accumulator.
         if (num!="" and not token.isnumeric()):
            self.q.enqueue(num)
            num=""

         # We aren't a number; so handle the token
         # '(' start brackets are simply markers of what point to return to when
         # a ')' close bracket is encountered.
         if (token=="("):
            self.s.push(token)

         # Special case; we look for this first -> it means we have to pop all
         # previous values off stack into the RPN queue until we find the '('
         elif (token==")"):
            # pop up until the bracket
            while (self.s.peek()!="("):
               self.q.enqueue(self.s.pop())

            # pop the bracket / throw it away (it was just a marker, we're done with it)
            self.s.pop()

         # Casee: operator handling
         # we are done handling brackets, check for a valid operator
         elif (token in self.precedence):
            while self.s.size() !=0 and (self.precedence[token] <= self.precedence[self.s.peek()]):
               self.q.enqueue(self.s.pop())
            self.s.push(token)

         # Case: character is numeric.
        # Append to accumulator and continue parsing
         elif (token.isnumeric()):
            num += token

      # Did token end on a number? If so store accumulated number in RPN queue
      if (num != ""):
         self.q.enqueue(num)

      # Now pop items from stack to the queue to cleanup
      while (self.s.size() != 0):
         self.q.enqueue(self.s.pop())
         
      # At this point, we have a valid RPN in the 'q' queue
      # (if the infix expression was valid)
      # Let's return a string version:
      q_cp = self.q.copy()

      rpn=""
      for c in q_cp:
         rpn+=c+" "
      return (rpn)


   # Routine to calculate a factorial
   def factorial(self, value):
      if (value<0):
         return (0)
      elif (value==0 or value==1):
         return (1)
      elif (value==2):
         return (2)

      product=value;

      for x in range(2, value):
         product = product * x
      return(product)


   # Routine to calculate "choose" (combinatorics)
   # Formula:
   # nCr (n Choose r) = n! / r!(n-r)!
   def choose(self, n, r):
      numerator=self.factorial(n)
      denominator=self.factorial(r)*self.factorial(n-r)

      # Sanity
      if (denominator==0):
         return (0)

      # Compute
      # NOTE: Should always be an integer result, but cast
      # it anyways to be safe
      return (int(numerator/denominator))
         

   # Given left value, right value, and an operator, calculate.
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
         return (left % right)

      elif (op == "!"):
         return (self.factorial(left))

      elif (op == "c" or op == "C"):
         return (self.choose(left, right))

      # dice roll; handled with 'random'
      # NOTE: expressions without 'd' are deterministic;
      # expressions with 'd' are non-deterministic (variable
      # outcomes).
      elif (op == "d"):
         sum = 0;

         # Left value is number of rolls; right value is die
         # IE 3d6 = 3 rolls of a 6 sided die, summed.
         for i in range(left):
            sum+=random.randint(1, right);
         return (sum);

      # whoops shouldn't have happened try to be graceful
      return (0);


   # Nifty little stack and queue algorithm for evaluating
   # the RPN.  Expects a valid RPN expression.
   def evaluateRPN(self):
      workstack=Stack()

      # As we pull tokens from the queue, we validate them and if neither a number
      # nor an operator, we abort with an error.
      for t in self.q.copy():
         if (t in self.precedence):
            # As we work backwards, right value is first; validate
            right=workstack.pop()
            if (not str(right).isnumeric() and not right in self.precedence):
                self.error=True
                break

            # Now get left value, validate
            # Special case: ! only takes one argument. Make them identical
            if (t=="!"):
               left=right
            else:
               left=workstack.pop()
               if (not str(left).isnumeric() and not left in self.precedence):
                   self.error=True
                   break

            # Both valid, so calculate
            workstack.push(self.calculate(left, right, t))
         else:
            workstack.push(int(t))

      # answer is now on the stack
      if (not self.error):
         return (workstack.pop())
      else:
         return (0)


   # One function to handle it all. How Pythonic.
   def resolve(self, expression, repeat=False):
      if not repeat:
         self.error=False
         self.q.clear()
         self.s.clear()
         self.infixToRPN(expression)
         return (self.evaluateRPN())
      else:
         # Repeat=True
         # This allows repeat dice rolls / calculations, without rebuilding
         # the RPN queue each time.
         return (self.evaluateRPN())

   # Heuristic to calculate expression distribution, ment to be
   # used with dice rolls (ie, 2d6).  This is done by repeating rolls
   # to a cap of n trials, then assessing the results.
   # Returns a histogram report with trial results, mean and mode.
   def getHistogram(self, expression, trials):
      # Validate min/max boundaries
      if (trials<0):
         trials = 1
      elif (trials > 1000000):
         trials=1000000

      # Initialize
      sb = ""
      rolls = dict()
      sum=0
      pct=1.0
      max=dict()
      result=dict()

      # Build
      for i in range(trials):
         if i==0:
            roll=self.resolve(expression);
         else:
            # We already built the RPN, don't waste cycles
            # reuilding it on every iteration, set repeat=True.
            roll=self.resolve(expression, repeat=True)

         # Track the recurrences of roll values
         if (roll in rolls.keys()):
            rolls[roll] += 1
         else:
            rolls[roll]= 1

      # Nifty way to build a key sorted report
      keys = list(rolls.keys())
      keys.sort()

      # Report
      sb=f"DISTRIBUTION HISTORGRAM ({trials:,} trials):\n"
      max[0]=max[1]=0
      for key in keys:
         result[key] = rolls[key]
         sum += key * rolls[key]
         pct = float(rolls[key])/float(trials,)*100.0
         if (pct > max[0]):
            max[0] = pct
            max[1] = key
         
         sb+=f"[{key:3}] ==> {rolls[key]:,} ({pct:.2f}%)\n"

         # Stash pct for later
         rolls[key]=pct

      mean=float(sum)/float(trials) + 0.5
      sb+=f"Mean: {mean:.2f}\n"
      mode=max[1]
      sb+=f"Mode: {mode}\n\n"

      # Scaling calculation uses a lambda function
      scale = lambda x,y: int(float(x/100)*float(y)+0.5)
      
      # Build histogram pictogragh
      pic = "PICTORIAL HISTOGRAM:\n"
      for key in keys:
         pic += f"[{key:3}] "
         for i in range(scale(rolls[key],160)):
            pic += "*"
         pic+="\n"
                        
      # Send back the report
      return (sb+pic)
  

# Integrated, interactive testing of module.
# Run module to access this function.
def test():
   dice = DiceResolver()
   p=""
   while True:
      x=input(f"Enter expression to resolve, 'q' to quit [{p}]: ")
      if x=="q" or x=='Q':
         break
      if (x!=""):
         p=x
      print("RPN:    ",dice.infixToRPN(p))
      print("ANSWER: ",dice.resolve(p))
      print(dice.getHistogram(p, 50000))
   return

# Interactive testing
if __name__ == "__main__":
   test()

