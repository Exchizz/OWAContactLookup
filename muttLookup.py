#!/usr/bin/python
import sys

from OWA_Contacts import OWA_Contacts


# Get first parameter
needle = ' '.join(sys.argv[1:])

print needle
owa_contacts = OWA_Contacts('sdu\user1337', 'password', 'cookies_OWA')
people = owa_contacts.SearchForName(needle)

for person in people:
        print person['email'], "\t", person['name']

