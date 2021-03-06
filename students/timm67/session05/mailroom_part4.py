#!/usr/bin/env python3

"""
Tim Meese
Au2018-Py210B
Mailroom Part 4 assignment
"""

import collections
from collections import defaultdict

# Revised donor database uses tuples for names instead of a single string

donors = {
     ('Jim', 'Tillson'): [5.00, 20.00],
     ('Barb', 'Langley'): [10.00, 20.00, 100.00],
     ('Jen', 'Garfield'): [10.00, 20.00, 5.00],
     ('Rex', 'Miller'): [20.00, 20.00, 5.00],
     ('Tony', 'Blake'): [20.00, 20.00, 10.00]
     }

exitMail = False


def prompt_donor():
    global donors
    donor_found = False
    donor_fname = input("Enter donor first name ('list' for all donors) : ")
    if donor_fname == 'list':
        for name in donors.keys():
            print("{}, {} ".format(name[0], name[1]))
        donor_fname = input("Enter donor first name : ")
    donor_lname = input("Enter donor last name : ")
    while True:
        donor_amt = input("Enter donation value: ")
        try:
            donor_amt = float(donor_amt)
            break
        except ValueError:
            print("Please enter a numeric donation value")

    # Not optimal for optimization via list comprehension
    for donor in donors.keys():
        if donor[0] == donor_fname and donor[1] == donor_lname:
            print("{0}, {1} FOUND".format(donor_fname, donor_lname))
            donors[donor].append(donor_amt)
            donor_found = True
            break

    if not donor_found:
        print("{0}, {1} NOT found, creating".format(donor_fname, donor_lname))
        donor = (donor_fname, donor_lname)
        donors[donor] = [donor_amt]

    return donor


def send_thankyou_single_donor_task():
    donor = prompt_donor()
    return generate_thankyou_single_donor_task(donor)


def send_thankyou_single_donor_test(donor):
    return generate_thankyou_single_donor_task(donor)


def add_single_donor_test(donor_fname, donor_lname, donor_amt):
    global donors
    donor_found = False

    for donor in donors.keys():
        if donor[0] == donor_fname and donor[1] == donor_lname:
            print("{0}, {1} FOUND".format(donor_fname, donor_lname))
            for amount in donor_amt:
                donors[donor].append(amount)
            donor_found = True
            break

    if not donor_found:
        print("{0}, {1} NOT found, creating".format(donor_fname, donor_lname))
        donor = (donor_fname, donor_lname)
        donors[donor] = donor_amt


def generate_thankyou_single_donor_task(donor):
    global donors
    total_donations = float(0.0)
    outlines = []
    fmtline0 = "\n\nDear {0},\n\n"
    fmtline1 = "Many thanks for your recent donation of {0:6.2f}.\n\n"
    fmtline2 = "Your total donations are {0:6.2f}, averaging {1:6.2f}\n\n"
    fmtline3 = "Thanks for your generous donation.\n\nBest Regards,\nThe Staff"
    donations = donors[donor]
    for donation in donations:
        total_donations += donation
    avg_donation = total_donations / len(donations)
    outlines.append(fmtline0.format(donor[0]))
    outlines.append(fmtline1.format(donations[(len(donations) - 1)]))
    outlines.append(fmtline2.format(total_donations, avg_donation))
    outlines.append(fmtline3.format())
    [print(outline) for outline in outlines]
    return outlines


def send_thankyou_multiple_donors_task():
    global donors
    filenames = []
    ffmtline0 = "\n\nDear {0},\n\n"
    ffmtline1 = "Many thanks for your recent donation of {0:6.2f}.\n\n"
    ffmtline2 = "Your total donations are {0:6.2f}, averaging {1:6.2f}\n\n"
    ffmtline3 = "Thanks for your generous donation.\nBest Regards,\nThe Staff"
    for donor in donors.keys():
        filename = "./{0}_{1}.txt".format(donor[0], donor[1])
        filenames.append(filename)
        print("Writing {0}...".format(filename))
        donations = donors[donor]
        total_donations = sum(donations)
        avg_donation = total_donations / len(donations)
        try:
            with open(filename, 'w') as handle:
                handle.write(ffmtline0.format(donor[0]))
                handle.write(ffmtline1.format(donations[(len(donations) - 1)]))
                handle.write(ffmtline2.format(total_donations, avg_donation))
                handle.write(ffmtline3.format())
        except PermissionError:
            print("Permission Error")
        except IOError:
            print("I/O Error")
    return filenames


def formatter(fname, lname, in_list):
    list_len = len(in_list)
    fmt_string = "{0:15} {1:15} ".format(fname, lname)
    fmt_string += list_len * '{:6.2f}, '
    return str(fmt_string.format(*in_list))


def create_report_task():
    global donors
    outlines = []
    report_fmt_str_hdr = "{0:15} {1:15} {2:10}"
    print(report_fmt_str_hdr.format('First Name', 'Last Name', ' Donations'))
    for key in donors.keys():
        outlines.append(formatter(key[0], key[1], donors[key]))
    [print(outline) for outline in outlines]
    return outlines


def print_menu():
    print("Mailroom Tasks")
    print("[1] Send a Thank you to a single donor")
    print("[2] Create a report")
    print("[3] Send letters to all donors")
    print("[9] Exit Mailroom")
    pass


def exit_mail():
    global exitMail
    exitMail = True


task_dict = {
    9: exit_mail,
    3: send_thankyou_multiple_donors_task,
    2: create_report_task,
    1: send_thankyou_single_donor_task
}


def main():
    while not exitMail:
        print_menu()
        response = input("Enter Mailroom Option: ")

        # Validate response
        try:
            response = int(response)
        except ValueError:
            print("Enter a number between 1-9")
            continue

        # Dispatch task based on response
        try:
            task_dict[response]()
        except KeyError:
            print("Please enter a correct task number")
            continue

if __name__ == "__main__":
    main()
