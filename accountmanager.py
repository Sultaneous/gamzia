#!/usr/bin/python

# Account Manager, Karim Sultan September 2020.
# CRUD for accounts and passwords in an sqlite DB.
# Passwords are salted and stored hashed in SHA256.
# USes username as the salt value (SALT is not secret).

# When creating an instance of the AccountManager class,
# provide the dbname parameter (or it will use the default name):
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
DEF_TABLE="accounts"
DEF_DBNAME="accounts.db"

class AccountManager():
   def __init__(self, dbname=DEF_DBNAME):
      self.dbname=dbname
      self.createAccountsTable()

   # Returns true if table exists in DB
   def doesTableExist(self):
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
         reurn(False)
      return(True)

   # Creates the accounts table.  Only used for new dbs.
   def createAccountsTable(self):
      if not self.doesTableExist():
         # Table does not exist so create it
         try:
            with sql.connect(self.dbname) as c:
               q="CREATE TABLE accounts (id INTEGER PRIMARY KEY, " \
                  "user, password, created)"
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

#**************************************************************************

def main():
   # Some test routines
   print("TEST: Creating AccountManager object; creates DB and accounts table")
   mgr=AccountManager("amgrtest.db")
   print("   If no exception, SUCCESS.")

   print()
   print("TEST: Does User Exist already?  Should be False.")
   print("   User Karim Exists?",mgr.doesUserExist("Karim"))

   print()
   print("TEST: Adding a user (+password).  Should be True, True.")
   print("   addUser(Karim, test) Karim worked? ",mgr.addUser("Karim", "test"))
   print("   doesUserExist(Karim)",mgr.doesUserExist("Karim"))

   print()
   print("TEST: Load user record. Should have id, user, password hash, date.")
   print("   getUser(Karim): ")
   results=mgr.getUser("Karim")
   for s in results:
      print(f"      Value: {s}")

   print()
   print("TEST: Get Password for user. Should be password hash.")
   print("   getPassword (Karim):",mgr.getPassword("Karim"))

   print()
   print("TEST: Verify Password. Should be False, True.")
   print("   verifyPassword(Karim,test):",mgr.verifyPassword("Karim","test"))
   print("   verifypassword(Karim,salted hash of test):",
         mgr.verifyPassword("Karim",AccountManager.saltPassword("Karim","test")))

   print()
   print("TEST: Update password. Should be True, hash.")
   print("   updatePassword(Karim, newpasswd): ",mgr.updatePassword("Karim", "newpwd"))
   print("   getPassword(Karim):",mgr.getPassword("Karim"))

   print()
   print("TEST: List users.  Should be a list with at least 1 record.")
   print("   listUsers():", mgr.listUsers())

   print()
   print("TEST: Delete user.  Should be True, False.")
   print("   deleteUser(Karim):",mgr.deleteUser("Karim"))
   print("   doesUserExist(Karim)",mgr.doesUserExist("Karim"))

   print()
   print("DONE.")
         

if __name__=="__main__":
   main()
   

