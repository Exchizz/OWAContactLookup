#!/usr/bin/python

from OWA_Contacts import OWA_Contacts

owa_contacts = OWA_Contacts('sdu\user', 'password', 'cookies_OWA')
people = owa_contacts.SearchForName("sara marie")

for person in people:
        print person

