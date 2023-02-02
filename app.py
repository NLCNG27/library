# LIBRARY APP: Write a program to oversee the library
# Needs to contain items such as:
# Name, type, year, pages, publisher, and price

# Functionalities include: 
# 1. View list of books
# 2. Add Books
# 3. Edit Books
# 4. Delete all
# 5. Delete Book
# 6. Find Books

#--------------------------------------------------------
# """NECESSARY FUNCTIONS"""
#--------------------------------------------------------

# importing necessary modules for mysql
import mysql.connector
MYDB = "libraryDb"

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database=MYDB
)

# creating cursor object 
cursor = db.cursor()

# creating table
def create_table():
  cursor.execute('DROP TABLE IF EXISTS BOOKS')

  sql = '''CREATE TABLE BOOKS(
      name CHAR(255),
      type CHAR(50),
      year CHAR(50),
      pages CHAR(50),
      publisher CHAR(50),
      price CHAR(50)
    )'''

  cursor.execute(sql)

  for i in cursor:
    print(i)

  return

# menu
def options():
  print("=" * 40)
  print("CHOOSE YOUR OPTION:")
  print("1. View all books")
  print("2. Add ")
  print("3. Edit")
  print("4. Delete All")
  print("5. Delete A Book")
  print("6. Find")
  print("NOTE: if quitting, enter a non-listed number.")
  print("=" * 40)

  return

# listing tables
def list_all():
  cursor.execute("SELECT * FROM BOOKS")
  myList = cursor.fetchall()

  if len(myList) == 0:
    print("Nothing to list!")
    return

  for i in myList:
    print(i)
    
  return

# add books to database
def add(name, type, year, pages, publisher, price):
  
  sql = "INSERT INTO BOOKS (name, type, year, pages, publisher, price) VALUES (%s, %s, %s, %s, %s, %s)"
  values = (name, type, year, pages, publisher, price)
  cursor.execute(sql, values)

  db.commit()

  print(cursor.rowcount, "item(s) inserted.")
  return

# edit books
def edit():

  print("Choose category to edit: ")
  print("1. name")
  print("2. type")
  print("3. year")
  print("4. pages")
  print("5. publisher")
  print("6. price")
  categoryChoice = int(input("Category (1-6): "))

  if categoryChoice == 1:
    criteria = 'name'
  elif categoryChoice == 2:
    criteria = 'type'
  elif categoryChoice == 3:
    criteria = 'year'
  elif categoryChoice == 4:
    criteria = 'pages'
  elif categoryChoice == 5:
    criteria = 'publisher'
  elif categoryChoice == 6:
    criteria = 'price'
    
  changeFrom = input("Change From: ").upper()
  changeTo = input("Change To: ").upper()

  sql = "UPDATE BOOKS SET " + criteria + " = %s WHERE " + criteria + " = %s"  
  values = (changeTo, changeFrom)

  cursor.execute(sql, values)
  db.commit()
  print(cursor.rowcount, "item(s) were updated!")

  return 

# delete all books from database
def delete_all():

  sql = "DELETE FROM BOOKS"
  cursor.execute(sql)

  db.commit()
  print(cursor.rowcount, "item(s) were deleted.")
  
  return

# delete a book (for this purpose, just use name as parameter)
def delete(): 
  book = input('Enter book name to remove: ').upper()
  values = book
  sql = "DELETE FROM BOOKS WHERE name = %s"
  cursor.execute(sql, (values,))

  db.commit()
  print(cursor.rowcount, "item(s) were deleted.")
  
  return

# find a book
def find(bookTitle):

  cursor = db.cursor()

  sql = "SELECT * FROM BOOKS WHERE name = %s"
  values = (bookTitle)

  cursor.execute(sql, (values,))
  myList = cursor.fetchall()

  if len(myList) == 0:
    print("Item not found!")
    return

  for i in myList:
    print(i)

  return


#--------------------------------------------------------
#                 MAIN FUNCTION
#--------------------------------------------------------

def main():

  # UNCOMMENT BELOW LINE IF NEEDING TO CREATE A TABLE AND DROP IF EXISTS ALREADY
  create_table()

  again = 'Y'
  while again == 'Y':
    options()
    choice = int(input("Your choice: "))

    if choice < 1 or choice > 6:
      print("Invalid choice, choose again.\n")
      continue
  
    elif choice == 1:
      list_all()

    elif choice == 2:
      print("Please provide the following...")
      name = input("Book Name: ").upper()
      type = input("Genre: ").upper()
      year = input("Publication Year: ")
      pages = input("Pages: ")
      publisher = input("Publisher: ").upper()
      price = input("Price: ")
      add(name, type, year, pages, publisher, price)
    elif choice == 3:
      edit()
    elif choice == 4:
      delete_all()
    elif choice == 5:
      delete()
    elif choice == 6:
      book = input("Enter book to search: ")
      find(book)

    again = input("Choose again? (Y/N): ").upper()
    if again == 'Y':
      continue
    elif again == 'N':
      break

  return  

# calling main function
if __name__ == "__main__":
  main()

  # closing cursor and database
  cursor.close()
  db.close()
  print("Cursor and database closed...")
