#!/bin/fish

# Variables
set -l PASSPHRASE_FILE ~/.gnupg/bw/passphrase.me
set -l ENCRYPTED_BWMASTER_FILE ~/.gnupg/bw/bwmaster.gpg

# Get master password
set -l BWMASTER (cat $PASSPHRASE_FILE | gpg --quiet --pinentry-mode loopback --passphrase-fd 0 --decrypt $ENCRYPTED_BWMASTER_FILE)

# Access BW with master password and set the items
set -l ITEMS (echo $BWMASTER | bw list items 2>/dev/null)

# Uses curses wrapper
python bwclip.py (echo $ITEMS)
