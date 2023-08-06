# tsiconv

tsiconv is a cli tool I created to take an input time and convert to UTC (optionally a destination timezone).

Many tools I ran accross log in UTC time. Additionally SOC's are now run by people in different timezones including PST, MST, EST, CST, or international timezones in Africa, India, Europe, Asia.0

# Installation
I highly recommend you use `pipx` to install this, as it creates the virtualenv for you and seamlessly handles the loading of the virtual environment when running this tool. If you choose not to use `pipx`, you should create a virtualenv and possibly a wrapper script to launch this in the virtualenv.

```sh
pipx install tsiconv
```

# Usage

The following is the help for the program
```
usage: __main__.py [-h] [-V] [-v] -t TIME [-s SOURCE] [-d DESTINATION] [-l]

 a program to convert timezones
    ex: python tsiconv.py

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose
  -t TIME, --time TIME  A datetime to convert. This should be in ISO-8601 format
  -s SOURCE, --source SOURCE
                        A source timezone to translate from. Only required if --time is a naive format
  -d DESTINATION, --destination DESTINATION
                        A destination timezone to translate from
  -l, --list            List out the timezones supported by this application
```

Without providing a destination timeformat, the default is to convert to UTC.

# Examples

```sh
# print help/usage
tsiconv -h

# print all available timezone formats
tsiconv -l

# Convert from Central European Time to Eastern Standard Time
tsiconv -t "2011-12-03T10:15:30+01:00" -d America/New_York

# Convert from Central Standard Time to Eastern Standard Time
tsiconv -t "2011-12-03T10:15:30" -s America/Chicago -d America/New_York

# Convert to UTC verbosely
tsiconv -v -t "2011-12-03T10:15:30+05:00"
```

# Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.
