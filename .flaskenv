export FLASK_APP=microblog.py
#export FLASK_DEBUG=1



# To start fake local python email server that will just print to the console
# python -m smtpd -n -c DebuggingServer localhost:8025
export MAIL_SERVER=localhost
export MAIL_PORT=8025



# This is how to setup emailing via gmail with the error logging. May have to
# fiddle with account settings to allow less secure apps to access email
# export MAIL_SERVER=smtp.googlemail.com
# export MAIL_PORT=587
# export MAIL_USE_TLS=1
# export MAIL_USERNAME=<your-gmail-username>
# export MAIL_PASSWORD=<your-gmail-password>
