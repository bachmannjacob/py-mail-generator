# py-mail-generator
Python-Script to generate mails and send them via SMTP.

## Usage
There are three possibilites to run the script and define the mail:

### The template
The template should always look like this:
```
SUBJECT:
Text that should be displayed in the subject-section
BODY:
Text that should be displayed in the body-section
```
Optionally one can add a variable section:
```
VAR:
Text
body
```
The script looks through the subject- and body-section for these tags to replace them. Which leads us to the first method:

### 1. Method - Use arguments
There are three required arguments and optional arguments to define the VAR-tags:
```
$ python script.py template [FROM]=account-mail [PW]=accound-password [TO]=target-mail Text=Everything body=ankle
```
[FROM] and [PW] are the login credentials for the script to log into your e-mail client to send the mail to [TO].
In this example i defined "Optionally" to be "Everything" and "one" to be "we".

### 2. Method - Use variables-template
The required arguments and the VAR-tags can be defined in a separat file:
```
[FROM]=account-mail
[PW]=accound-password
[TO]=target-mail
Text=Everything
body=ankle
```
Execute:
```
$ python script.py template [VARFILE]=variables-template
```
Done.

### 3. Method - Use both
Everything like in method 1 and 2 with variables-template:
```
Text=Everything
body=ankle
```
And execution like:
```
$ python script.py template [VARFILE]=variables-template [FROM]=account-mail [PW]=accound-password [TO]=target-mail
```
Done.
