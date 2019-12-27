# Notes

## roles

- sudo log_output
  - Send sudo-io to remote logging
- logging: setup rsyslog

caddy
  accept-eula
  email = something
  firewall:
    80
    443

This error is transient:

```text
TASK [firewall : Which modules are required by nftables] **********************************************************************************************
ok: [10.77.38.18]

TASK [firewall : Add those modules to a load-list] ****************************************************************************************************
changed: [10.77.38.18] => (item=skipped, since /etc/modules-load.d/nftables.conf exists)

TASK [firewall : debug] *******************************************************************************************************************************
ok: [10.77.38.18] => {
    "firewall_modules": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_loop_var": "item",
                "backup": "",
                "changed": true,
                "diff": [
                    {
                        "after": "",
                        "after_header": "/etc/modules-load.d/nftables.conf (content)",
                        "before": "",
                        "before_header": "/etc/modules-load.d/nftables.conf (content)"
                    },
                    {
                        "after_header": "/etc/modules-load.d/nftables.conf (file attributes)",
                        "before_header": "/etc/modules-load.d/nftables.conf (file attributes)"
                    }
                ],
                "failed": false,
                "invocation": {
                    "module_args": {
                        "attributes": null,
                        "backrefs": false,
                        "backup": false,
                        "content": null,
                        "create": true,
                        "delimiter": null,
                        "directory_mode": null,
                        "firstmatch": false,
                        "follow": false,
                        "force": null,
                        "group": null,
                        "insertafter": null,
                        "insertbefore": null,
                        "line": "skipped, since /etc/modules-load.d/nftables.conf exists",
                        "mode": null,
                        "owner": null,
                        "path": "/etc/modules-load.d/nftables.conf",
                        "regexp": null,
                        "remote_src": null,
                        "selevel": null,
                        "serole": null,
                        "setype": null,
                        "seuser": null,
                        "src": null,
                        "state": "present",
                        "unsafe_writes": null,
                        "validate": null
                    }
                },
                "item": "skipped, since /etc/modules-load.d/nftables.conf exists",
                "msg": "line added"
            }
        ]
    }
}

TASK [firewall : Load modules] ************************************************************************************************************************
failed: [10.77.38.18] (item=skipped, since /etc/modules-load.d/nftables.conf exists) => {
    "ansible_loop_var": "item",
    "changed": true,
    "cmd": [
        "modprobe",
        "skipped,",
        "since",
        "/etc/modules-load.d/nftables.conf",
        "exists"
    ],
    "delta": "0:00:00.002726",
    "end": "2019-12-24 03:56:36.543507",
    "item": "skipped, since /etc/modules-load.d/nftables.conf exists",
    "rc": 1,
    "start": "2019-12-24 03:56:36.540781"
}

STDERR:

modprobe: FATAL: Module skipped, not found in directory /lib/modules/4.19.0-6-amd64


MSG:

non-zero return code
```

## Caddy

https://github.com/caddy-ansible/caddy-ansible
https://github.com/caddyserver/caddy/tree/master/dist/init/linux-systemd

Example Caddyfile: https://github.com/pyca/infra/blob/master/caddy/Caddyfile

## nftables

Should really read up on nftables: https://wiki.nftables.org

And networking in general

https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes#Examples
https://lyngvaer.no/log/simple-nftables-config
https://wiki.nftables.org/wiki-nftables/index.php/Classic_perimetral_firewall_example

This is suggested as it explains conntrack states:

https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#STATEMACHINE
