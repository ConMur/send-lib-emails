#Import stmplib for the email sending function
import smtplib

#Import argparse to parse command line args
import argparse

#Import sys so that we can exit when given bad command line args
import sys

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

#TODO: parse contents of file and send emails if they have been checked out for
# longer than "days" days
# After sending an email, make note of that in the file so that emails arent
#   sent out every time this script is run (maybe specify an interval to email?)
