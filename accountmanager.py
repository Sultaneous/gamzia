#!/usr/bin/python

# Account Manager, Karim Sultan September 2020.
# CRUD for accounts and passwords in an sqlite DB.
# Passwords are salted and stored hashed in SHA256.
# Uses username as the salt value (SALT is not secret).

# KSU 201011 Formalized unit tests.
# KSU 201012 Fixed case insensitive user name conflict issue by altering
#            schema to "...user TEXT UNIQUE COLLATE NOCASE ..."

# When creating an instance of the AccountManager class,
# provide the dbname parameter (or it will use the default name):
# "accounts.db"
# NOTE: This will create db and schema if required.
# mgr = AccountManager("mydb.db")
#
# To add a user:
# addUser(user,password)
#
# To verify a password hash:
# NOTE: Only salted password hashes are compared, not actual
# passwords. Actual passwords are not stored, for security.
# verifyPassword(user, passwordHash)
#
# To generate a salted password hash, use the static method:
# NOTE: User name must be provided, as this is the salt value
# for the algorithm.  The salt value is not a secret.
# hash=AccountManager.saltedHash(user, password)
#
# NOTE: main() has test routines which provide example usage.

import hashlib
import datetime
import sqlite3 as sql
import os

FLAG_DEBUG=False
DEF_DBNAME="accounts.db"          # Default database filename
DEF_TESTDB="unit_tests.db"        # Default unit test database filename

class AccountManager():
   def __init__(self, dbname=DEF_DBNAME):
      self.dbname=dbname
      self.__createAccountsTable()

   # Returns true if table exists in DB
   def __doesTableExist(self):
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            q="SELECT count(name) FROM sqlite_master " \
               "WHERE type='table' AND name='accounts'"
            k.execute(q)
            if (k.fetchone()[0]==0):
               return(False)
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::doesTableExist(): {e}")
         return(False)
      return(True)

   # Returns true if user account exists in table
   def doesUserExist(self, user):
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            q="SELECT count(user) FROM accounts " \
               "WHERE user=? "
            k.execute(q, (user, ))
            if (k.fetchone()[0]==0):
               return(False)
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::doesUserExist({user}): {e}")
         return(False)
      return(True)

   # Creates the accounts table.  Only used for new dbs.
   # Sets username column to unique, case insensitive.
   def __createAccountsTable(self):
      if not self.__doesTableExist():
         # Table does not exist so create it
         try:
            with sql.connect(self.dbname) as c:
               q="CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                  "user TEXT UNIQUE COLLATE NOCASE, password, created)"
               c.execute(q)
               c.commit()
         except Exception as e:
            if (FLAG_DEBUG):
               print(f"Error::createAccountsTable(): {e}")
            return(False)
         return(True)

   # C-RUD
   def addUser(self, user, password):
      password=AccountManager.saltPassword(user, password)
      try:
         c=sql.connect(self.dbname)
         qp="INSERT INTO accounts (user, password, created) VALUES (?, ?, ?)"
         c.execute(qp, (user, password, datetime.datetime.now()))
         c.commit()
         c.close()
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::addUser({user}, {password}): {e}")
         return(False)
      return(True)

   # C-R-UD -> Returns all records in account database as a list of tuple.
   # Returns an empty list if no records found.
   def listUsers(self):
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            qp="SELECT * FROM accounts"
            k.execute(qp)
            records=k.fetchall()
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::listUsers(): {e}")
         return(None)
      return(records)

   # C-R-UD -> returns entire user record as tuple
   # Returns None if record is not found.
   def getUser(self, user):
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            qp="SELECT * FROM accounts WHERE user=?"
            k.execute(qp, (user,))
            record=k.fetchone()
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::getUser({user}): {e}")
         return(None)
      return(record)

   # C-R-UD -> Password field only
   # Returns None if password is not found.
   def getPassword(self, user):
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            qp="SELECT password FROM accounts WHERE user=?"
            k.execute(qp, (user,))
            password=k.fetchone()
            if (FLAG_DEBUG):
              print(f"PasswordHash: [{password[0]}]")
            return(password[0])
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::getPassword({user}): {e}")
         return(None)

   # CR-U-D Updates user record password
   def updatePassword(self, user, password):
      password=AccountManager.saltPassword(user, password)
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            qp="UPDATE accounts SET password=? WHERE user=?"
            k.execute(qp, (password, user))
            c.commit()
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::updatePassword({user}, {password}): {e}")
         return(False)
      return(True)

   # CRU-D Deletes record by user name
   def deleteUser(self, user):
      if not self.doesUserExist(user):
         return(False)
      try:
         with sql.connect(self.dbname) as c:
            k=c.cursor()
            q="DELETE FROM accounts WHERE user=?"
            k.execute(q, (user,))
            c.commit()
            # Reclaim file space
            c.execute("VACUUM")
      except Exception as e:
         if (FLAG_DEBUG):
            print(f"Error::deleteUser({user}): {e}")
         return(False)
      return(True)

   # Compares a salted password hash to the one in DB. Returns True/False.
   # DO NOT PROVIDE A PASSWORD AS THE PARAMETER.
   # A PRE-SALTED, PRE-HASHED STRING IS EXPECTED (ie, the client program
   # should never provide an actual password; everything is done with
   # irreversible salted hashes for security purposes.
   def verifyPassword(self, user, passwordHash):
      if (FLAG_DEBUG):
         print(f"[{user}][{passwordHash}]")
         answer=self.getPassword(user)
         print(str(answer)==str(passwordHash))
         print(f"Answer:[{answer}]")
      if (passwordHash==self.getPassword(user)):
         return(True)
      return(False)

   # Applies the salt formula and produces password hash (SHA256)
   @staticmethod
   def saltPassword(user, password):
      s=user+password+user
      b=s.encode("utf-8")
      h=hashlib.sha256(b).hexdigest().lower()
      return(h)

#End of class
#**************************************************************************

# Unit test helper methods
def fail(err="Test failed."):
   print (f"FAILED: {err}\n")

def passed(msg="Test passed."):
   print (f"PASSED: {msg}\n")

# Unit test
def UnitTestCreateSchema():
   print("TEST: Creating AccountManager object; creates DB and accounts table")
   try:
      mgr=AccountManager(DEF_TESTDB)
      passed("Schema created.")
      return True
   except Exception as err:
      fail(err)
      return (false)

def UnitTestUserExists1():
   print("TEST: Does User Exist already?  Should be False.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=False
      actual=mgr.doesUserExist("Karim")
      print("   User Karim Exists?", actual)
      assert expected==actual
      passed("User does not exist.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestAddUser():
   print("TEST: Adding a user (+password).")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=True
      actual=mgr.addUser("Karim", "test")
      assert expected==actual
      passed("User Karim added.")
      return True
   except Exception as err:
      fail(err)
      return False

def UnitTestAddDuplicateUser():
   print("TEST: Adding a duplicate user.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=False
      mgr.addUser("Dupe", "dupe")
      # Test adding same user name with different case
      actual=mgr.addUser("dupe", "dupe")
      assert expected==actual
      passed("Duplicate detected, addUser aborted.")
      return True
   except Exception as err:
      fail(err)
      return False

def UnitTestUserExists2():
   print("TEST: Does User Karim Exist now?  Should be True.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=True
      actual=mgr.doesUserExist("Karim")
      print("   User Karim Exists?", actual)
      assert expected==actual
      passed("User exists.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestGetUser():
   print("TEST: Load user record. Loads id, user, password hash, creation date.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      print("   getUser(Karim): ")
      results=mgr.getUser("Karim")
      assert results!=None
      for s in results:
         print(f"      Value: {s}")
      passed("Record loaded.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestGetPassword():
   print("TEST: Get Password for user. Should be password hash.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      actual=mgr.getPassword("Karim")
      assert actual!=None
      print("   getPassword (Karim):",actual)
      passed("Loaded password hash.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestVerifyBadPassword():
   print("TEST: Verify BAD Password.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=False
      actual=mgr.verifyPassword("Karim","test")
      print("   verifyPassword(Karim,test):",actual)
      assert expected==actual
      passed("Bad password rejected.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestVerifyGoodPassword():
   print("TEST: Verify GOOD Password (salted hash of password).")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=True
      actual=mgr.verifyPassword("Karim",
             AccountManager.saltPassword("Karim","test"))
      print("   verifypassword(Karim,salted hash of test):",actual)
      assert expected==actual
      passed("Good password accepted.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestUpdatePassword():
   print("TEST: Update password.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=True
      actual=mgr.updatePassword("Karim", "newpwd")
      print("   updatePassword(Karim, newpasswd):",actual)
      assert expected==actual
      passed("Password updated.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestListUsers():
   print("TEST: List users.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      mgr.addUser("Admin","Admin")
      mgr.addUser("Bob","Slob")
      mgr.addUser("Deimos","Phobos")
      results=mgr.listUsers()
      assert results!=None
      print(results)
      passed("Listed at least one user.")
      return True
   except Exception as err:
      fail (err)
      return False

def UnitTestDeleteUser():
   print("TEST: Delete user.")
   try:
      mgr=AccountManager(DEF_TESTDB)
      expected=True
      actual=mgr.deleteUser("Karim")
      print("   deleteUser(Karim):",actual)
      assert expected==actual
      passed("User deleted.")
      return True
   except Exception as err:
      fail (err)
      return False

   
def doTests():
   # Register unit tests. Order is important.
   passed=0
   unittests=[]
   unittests.append(UnitTestCreateSchema)
   unittests.append(UnitTestUserExists1)
   unittests.append(UnitTestAddUser)
   unittests.append(UnitTestAddDuplicateUser)
   unittests.append(UnitTestUserExists2)
   unittests.append(UnitTestGetUser)
   unittests.append(UnitTestGetPassword)
   unittests.append(UnitTestVerifyBadPassword)
   unittests.append(UnitTestVerifyGoodPassword)
   unittests.append(UnitTestUpdatePassword)
   unittests.append(UnitTestListUsers)
   unittests.append(UnitTestDeleteUser)

   # Execute unit tests
   for test in unittests:
      if (test()):
         passed+=1

   # Report
   print()
   print (f"Results: passed {passed} / {len(unittests)} unit tests.")
   print ("Testing complete.")

   # Clean up
   if os.path.exists(DEF_TESTDB):
      os.remove (DEF_TESTDB)

   print()
   print("DONE.")
   print()

#**************************************************************************

if (__name__=="__main__"):
   doTests()
   

