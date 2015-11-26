# OWAContactLookup
A small script to do lookups in OWA contacts. It caches cookies and renews automatically

Dependencies:
```
sudo apt-get install python-bs4 -y 
```

To use with mutt:
```
set query_command = "/path/to/muttLookup.py '%s'"
```
By pressing ctrl+q(if not changed), you will be able to do lookups in SDU's contacts.
