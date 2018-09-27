import sys
import smtplib

# save template
TEMPLATE = sys.argv[1]

# check for rest of args
VARDEF = []
VARFILE = None
FROM = None
PW = None
TO = None

if len(sys.argv) > 2:
	for i in range(2, len(sys.argv)):
		VARDEF.append(sys.argv[i])
		if "--varfile" in sys.argv[i]:
			VARFILE = sys.argv[i].rstrip().replace("--varfile=", "")
		if "[TO]" in sys.argv[i]:
			TO = sys.argv[i].rstrip().replace("[TO]=", "")
		if "[PW]" in sys.argv[i]:
			PW = sys.argv[i].rstrip().replace("[PW]=", "")
		if "[FROM]" in sys.argv[i]:
			FROM = sys.argv[i].rstrip().replace("[FROM]=", "")


# if VARFILE definition found: open and save var_defs
if VARFILE is not None:
	file = open(VARFILE, "r")
	for line in file:
		if "[TO]" in line:
			TO = line.rstrip().replace("[TO]=", "")
		if "[PW]" in line:
			PW = line.rstrip().replace("[PW]=", "")
		if "[FROM]" in line:
			FROM = line.rstrip().replace("[FROM]=", "")
		if not any(line.split("=")[0] in elem for elem in VARDEF):
			VARDEF.append(line.rstrip())

# check if required variables are given
if FROM is None or PW is None or TO is None:
	if FROM is None:
		print("Err: FROM not defined")
	if PW is None:
		print("Err: PW not defined")
	if TO is None:
		print("Err: TO not defined")
	sys.exit()

# preinit of templatetext vars
var = []
subject = ""
body = ""

# go through template
file = open(TEMPLATE, "r")
MODE = None
for line in file:
	if "VAR:" in line:
		MODE = "VAR"
	elif "SUBJECT:" in line:
		MODE = "SUBJECT"
	elif "BODY:" in line:
		MODE = "BODY"
	else:
		if MODE is "VAR":
			var.append(line.rstrip())
		if MODE is "SUBJECT":
			subject += line
		if MODE is "BODY":
			body += line

subject = subject.rstrip()


# now we have TO, var[], VARDEF[], subject, body
# replace vars ind subject and body with definitions in VARDEF[]
for var_sngl in var:
	contains = None
	for var_def_sngl in VARDEF:
		if var_sngl in var_def_sngl:
			contains = var_def_sngl
	if contains is None:
		print(var_sngl + " not defined")
		sys.exit()
	else:
		dfntn = contains.split("=", 1)[1]
		subject = subject.replace(var_sngl, dfntn)
		body = body.replace(var_sngl, dfntn)

# make it beautiful
print("==================================================\n")
print("To: " + TO)
print("------------")
print("Subject: " + subject)
print("------------")
print("\n" + body)
print("\n==================================================\n")


# send mail
bool_send = input("Send? (y/n): ")
if bool_send is not "y":
	sys.exit()

# setting up server
server = smtplib.SMTP_SSL('smtp.gmail.com')
server.set_debuglevel(1)
server.ehlo

# setting up credentials
server.login(FROM.replace("@gmail.com", ""), PW)
server.sendmail(FROM, TO, "Subject: {}\n\n{}".format(subject, body))
server.quit()

print("\nE-Mail sent..")
