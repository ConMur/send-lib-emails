#Import smtp for the email sending function
import smtplib

#Import argparse to parse command line args
import argparse

#Import sys so that we can exit when given bad command line args
import sys

#Import datetime and time to check dates
from datetime import date
import time

#Import getpass for password input
import getpass

#Import subprocess for validation of if a user is in a group
import subprocess

#Set up the parser
parser = argparse.ArgumentParser()
parser.add_argument("days",type=int, default = 21, help="This is the maximum number of days ago that a book can be signed out without this script sending an email")
parser.add_argument("--librarianName", default = "Librarian", help="This is the name that will be displayed in the "+
                     "signature line of the email")
args = parser.parse_args()
days = args.days

#Ensure the days are not less than 0
if days < 0:
    print("ERROR: days must be greater than 0")
    sys.exit

#Get the login info from the user
print("You will be prompted to enter your csclub login for this script to access the mail server."+
      " Please note this will only work if you are a member of the exec group")
csclubID = input("Enter your csclubID: ")

#Validate that the user is in the exec group
try:
    output = subprocess.check_output(["groups",  csclubID])
except subprocess.CalledProcessError as  e:
    print("ERROR: Invalid input")
    sys.exit

if not "exec" in str(output):
    print("ERROR: The user " + csclubID + " is not in the exec group.")
    sys.exit

csclubPwd = getpass.getpass()

#Set up email
server = smtplib.SMTP_SSL("mail.csclub.uwaterloo.ca", 465)
server.login(csclubID, csclubPwd)

#Function definitons
def send_email(quest_id: str, date: str, book_name_list) -> None:
    """Sends an email to quest_id@csclub.uwaterloo.ca if the date the book
    was signed out exceeds the days it is supposed to be signed out for"""

    email_address = quest_id + "@csclub.uwaterloo.ca"
    book_name = "".join(book_name_list)

    if overdue(days, date):
        email_message_body = "Hi " + quest_id + ",\n\n" +  "Our records indicate that you have had the book " + book_name + " signed out for " + str(days) + " days.\n\n" +  "Please return the book to the CS Club office (MC 3036) at your earliest convenience.\n\n" + "Thanks,\n\n" + args.librarianName + "\n" + "Computer Science Club | University of Waterloo\n" + "librarian@csclub.uwaterloo.ca"
        
        email_message_subject = "Overdue book: {}".format(book_name)
        email_message = "Subject: {}\n\n{}".format(email_message_subject, email_message_body)

        print("sending email for book {}".format(book_name))

        server.sendmail("librarian@csclub.uwaterloo.ca", email_address, email_message)
    else:
        print("not sending email for book {}".format(book_name))

def overdue(max_days_can_be_signed_out:int, signed_out_date: str) -> bool:    
    """Determines if a book is due if signed_out_date is more days back in history
    than max_days_can_be_signed_out.
    signed_out_date must be in the format YYYY-MM-DD"""

    #Determine the days the book has been signed out
    date_tokens = signed_out_date.split("-")
    date_signed_out = date(int(date_tokens[0]), int(date_tokens[1]), int(date_tokens[2]))
    days_signed_out = date.fromtimestamp(time.time()) - date_signed_out

    #Check the date to see if the book has been signed out too long
    return days_signed_out.days > max_days_can_be_signed_out


#Open the file that contains the list of signed out library books
signed_out_books_file = open("checkedout.txt", "r")

for line in signed_out_books_file:
    tokens = line.split(" ") 
    
    #Change book name into a space seperated name
    book_name_with_spaces = ""

    for i in range(len(tokens) - 2):
        book_name_with_spaces += str(tokens[i + 2]) + " "
    
    #Remove the \n at the end of book_name_with_spaces
    book_name_with_spaces = book_name_with_spaces[:-2]

    send_email(tokens[0], tokens[1], book_name_with_spaces)

#Exit from the email server    
server.quit()


#TODO: parse contents of file and send emails if they have been checked out for
# longer than "days" days
# After sending an email, make note of that in the file so that emails arent
#   sent out every time this script is run (maybe specify an interval to email?)
