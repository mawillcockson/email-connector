# general
What I would like to happen is for the sudo role to fail gracefully if it can't login as root, and retry with the provision_username.

# roles

- sudo log_output
  - Send sudo-io to remote logging
- logging: setup rsyslog
- dovecot

caddy
  accept-eula
  email = something
  firewall:
    80
    443
