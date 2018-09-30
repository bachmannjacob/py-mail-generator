import sys
import smtplib
import win32com.client as win32

# save template
TEMPLATE = sys.argv[1]

# check for rest of args
VARDEF = []
VARFILE = None
FROM = None
PW = None
TO = None
Y_FLAG = False
M_FLAG = None

if len(sys.argv) > 2:
	for i in range(2, len(sys.argv)):
		VARDEF.append(sys.argv[i])
		if "--varfile" in sys.argv[i]:
			VARFILE = sys.argv[i].rstrip().split("=")[1]
		if "-y" in sys.argv[i]:
			Y_FLAG = True
		if "--mode" in sys.argv[i]:
			M_FLAG = sys.argv[i].rstrip().split("=")[1]
			print(M_FLAG)
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
		if "[TO]" in line and TO is None:
			TO = line.rstrip().replace("[TO]=", "")
		if "[PW]" in line and TO is None:
			PW = line.rstrip().replace("[PW]=", "")
		if "[FROM]" in line and FROM is None:
			FROM = line.rstrip().replace("[FROM]=", "")
		if not any(line.split("=")[0] in elem for elem in VARDEF):
			VARDEF.append(line.rstrip())

# check if required variables are given
if M_FLAG != "outlook" and (FROM is None or PW is None or TO is None):
	if FROM is None:
		print("Err: FROM not defined")
	if PW is None:
		print("Err: PW not defined")
	if TO is None:
		print("Err: TO not defined")
	sys.exit()

# preinit of templatetext vars
VAR = []
SUBJECT = ""
BODY = ""

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
			VAR.append(line.rstrip())
		if MODE is "SUBJECT":
			SUBJECT += line
		if MODE is "BODY":
			BODY += line

SUBJECT = SUBJECT.rstrip()

# now we have TO, VAR[], VARDEF[], SUBJECT, BODY
# replace vars ind SUBJECT and BODY with definitions in VARDEF[]
for var_sngl in VAR:
	contains = None
	for var_def_sngl in VARDEF:
		if var_sngl in var_def_sngl:
			contains = var_def_sngl
	if contains is None:
		print(var_sngl + " not defined")
		sys.exit()
	else:
		dfntn = contains.split("=", 1)[1]
		SUBJECT = SUBJECT.replace(var_sngl, dfntn)
		BODY = BODY.replace(var_sngl, dfntn)

# make it beautiful
print("==================================================\n")
print("To: " + TO)
print("------------")
print("SUBJECT: " + SUBJECT)
print("------------")
print("\n" + BODY)
print("\n==================================================\n")

# send mail
if not Y_FLAG:
	bool_send = input("Send? (y/n): ")
	if bool_send is not "y":
		sys.exit()

# defining smtp function
def smtp_send(ssl, server):
	# setting up server
	if ssl:
		print("Using SSL ...")
		server = smtplib.SMTP_SSL(server)
	else:
		server = smtplib.SMTP(server)
	
	server.set_debuglevel(1)
	server.ehlo
	print(FROM.split("@")[0])
	# setting up credentials
	if ssl:
		server.login(FROM.split("@")[0], PW)
	else:
		server.login(FROM, PW)
	server.sendmail(FROM, TO, "Subject: {}\n\n{}".format(SUBJECT, BODY))
	server.quit()


if M_FLAG == "outlook":
	print("Using Outlook ...")
	outlook = win32.Dispatch("outlook.application")
	mail = outlook.CreateItem(0)
	mail.To = TO
	mail.Subject = SUBJECT
	mail.Body = BODY
	mail.Send()
if M_FLAG == "gmail":
	print("Using gmail ...")
	smtp_send(True, 'smtp.gmail.com')
if M_FLAG == "gmx":
	print("Using gmx ...")
	smtp_send(False, "smtp.gmx.com")

print("\nE-Mail sent..")
