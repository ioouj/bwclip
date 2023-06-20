# bwclip

A bitwarden-cli python wrapper for quick usage

### Requirements
- python 3.x
- bitwarden-cli
- curses
- gpg
- xclip

Generate a gpg key for the bwmaster with a passphrase.
Update the locations in ./bwclip.fish
```sh
  set -l PASSPHRASE_FILE ~/passphrase
  set -l ENCRYPTED_BWMASTER_FILE ~/bwmaster.gpg
```


### Usage
```sh
  ./bwclip.fish
```

To do: Auto gpg generation and encrypt/decrypt master pass
