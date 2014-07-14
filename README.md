# change_line_profile.py
*by timdoug*

This a simple tool to programmatically toggle Annex A and M profiles on a Sonic.net Fusion DSL connection. It replicates the functionality available in the web UI, but makes it very easy to, e.g., enable upload priority at the beginning of a nightly backup script and reenable download priority when finished.


### Software requirements

 * Python 2.x
 * requests (`pip install requests`)


### Usage

First, create a `.sonicnet` config file in your home directory with the following contents (with the proper values for your account and line, of course):
```
[fusion]
user=timdoug
password=foobar
number=4155551212
```

Then call the script with either download or upload as desired, e.g.:
```
$ ./change_line_profile.py
usage: ./change_line_profile.py upload|download
$ ./change_line_profile.py download
Authenticating... done.
Changing profile to download... done.
$
```

If your line is already in the preferred profile, it'll noop:
```
$ ./change_line_profile.py download
Authenticating... done.
Current profile is already download.
$
```
