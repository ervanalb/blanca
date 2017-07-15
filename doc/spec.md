blanca technical spec
=====================

blanca will be written in Python 3.
It will use `flask` as the web framwork
and `sqlalchemy` for database interface.

There will be two main parts:
the webapp, and the email handler.

The Webapp
----------

The webapp will allow you to administer lists and your account.

The Email Handler
-----------------

The email handler will be executed every time a mail arrives.
It will route the mail appropriately.

Database structure
------------------

### Users table

The users table will contain usernames and passwords.

### Lists table

The lists table will store local lists. It will have columns such as:
* List name
* List description
* List admin
* List memacl

### String table

The string table will store strings (i.e. bare email addresses) added to lists.
This is to maintain compatibility with the membership table.

### Membership table

The membership table will store what users and lists are on what lists.
