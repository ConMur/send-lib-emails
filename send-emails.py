#Import stmplib for the email sending function
import smtplib

#Import argparse to parse command line args
import argparse

#Import sys so that we can exit when given bad command line args
import sys

#Import re for regex tokenizing of the file input
import re

#Import datetime and time to check dates
from datetime import date
import time

#Function definitons
def send_email(quest_id: str, date: str, book_name_list) -> None:
    """Sends an email to quest_id@csclub.uwaterloo.ca if the date the book
    was signed out exceeds the days it is supposed to be signed out for"""

    email_address = quest_id + "@csclub.uwaterloo.ca"
    book_name = "".join(book_name_list)

    if overdue(days, date):
        print("sending email for book {}".format(book_name))
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

#Set up the parser
parser = argparse.ArgumentParser()
parser.add_argument("days",type=int, default = 21, help="This is the maximum number of days ago that a book can be signed out without this script sending an email")
args = parser.parse_args()
days = args.days

#Ensure the days are not less than 0
if days < 0:
    print("Error: days must be greater than 0")
    sys.exit

#Open the file that contains the list of signed out library books
signed_out_books_file = open("checkedout.txt", "r")

for line in signed_out_books_file:
    tokens = line.split(" ") 
    send_email(tokens[0], tokens[1], tokens[2:])
    

#TODO: parse contents of file and send emails if they have been checked out for
# longer than "days" days
# After sending an email, make note of that in the file so that emails arent
#   sent out every time this script is run (maybe specify an interval to email?)
