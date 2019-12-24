# email-connector

Makes a less friendly email server more friendly.

# Goals

- Use [Dovecot][] to:
  - Continuously retrieve email from a server
  - Make that mail available to multiple users, keeping track of read and deleted for each user
- Log all server actions, including:
  - Retrieved mail
  - Read mail
  - Logins to Dovecot
  - Logins through SSH
  - Modifications to OS and Dovecot configuration files
- Email log summaries
- Setup, use, and test backup of email files
- Serve a web page with setup instructions for email clients


[dovecot]: <https://www.dovecot.org/>
