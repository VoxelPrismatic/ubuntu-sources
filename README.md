# ubuntu sources
just lists sources so i can use both the LTS and current versions at the same time

### files
- `releases.json` - provides release names and LTS status
- `sources.py` - prints the sources

formatted like below:
```deb
### 23.10 - Mantic Minotaur
deb http://us.archive.ubuntu.com/ubuntu/ mantic main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ mantic main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ mantic main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ mantic main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ mantic main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu/ mantic main restricted universe multiverse

deb http://us.archive.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu/ mantic-updates main restricted universe multiverse

deb http://us.archive.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu/ mantic-backports main restricted universe multiverse

deb http://us.archive.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu/ mantic-proposed main restricted universe multiverse

deb http://us.archive.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu/ mantic-security main restricted universe multiverse
```
