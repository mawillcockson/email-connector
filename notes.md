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

## How to bootstrap the server

This is a general outline of how I think it'd be possible to bootstrap a server. This relies on the provider having a feature similar to [cloud-init](https://cloudinit.readthedocs.io/en/latest/), namely, a way to describe a set of actions to take on an instance at the OS level after it's booted, without having to connect to the instance.

For instance:

- [DigitalOcean lets you specify `user_data`](https://developers.digitalocean.com/documentation/v2/#create-a-new-droplet)
- [Vultr lets you specify a `bash` script](https://www.vultr.com/api/#startupscript):
  - <blockquote>On Linux, the startup script is saved to `/tmp/firstboot.exec`, it is executed with `/bin/bash` (as `root`), and the output is saved to `/tmp/firstboot.log`</blockquote>
- [Linode has `bash` scripts they call StackScripts](https://www.linode.com/docs/platform/stackscripts/)

All of these meet this requirement.

Alright, so here's how it'd go:

1. You spin up an instance with a boot script
1. While it's spinning up, you query the provider's API for the instance's network addresses, and set DNS records accordingly
1. The startup script:
  a. Sets `pubkey` as the only valid login method for SSH
  a. Downloads [`caddy`](https://caddyserver.com) or an [ACME client](https://letsencrypt.org/docs/client-options/)
    - Downloads a `Caddyfile` if `caddy` is used
  a. Obtains an HTTPS certificate for the domain you set DNS records for
  a. Sets up `caddy` or a server to serve the instance's SSH host public key only using HTTPS
1. You connect to the domain you set DNS records for, requiring valid HTTPS certificates, and save the SSH public key
1. You set an SSHFP record for the domain you set DNS records for, using the SSH public key you downloaded

If your provider doesn't let you specify an SSH public key to add to an `authorized_keys` file, and you need to provide the instance with your SSH public key so you can connect, you could have the boot script include a line that downloads your public key into an `authorized_keys` file, using HTTPS.

Aside from that, you're done.

This relies on your provider giving you the correct network information for the instance, and on Let's Encrypt validating that the route to your server, using the same information you would use to connect to it by fully-qualified domain name.

This means I'm not worried about someone trying to use my scripts to set up a rogue instance for me to connect to, as the first connection made to the instance is using the FQDN over HTTPS: If someone can impersonate my instance to the point where they can get a valid certificate from Let's Encrypt, despite the FQDN pointing to the instance that was just spun up, then I have bigger problems to worry about, than connecting to a rogue instance.

The only danger here are stale DNS records: if this process is done, and then the instance is destroyed, but the DNS records aren't removed, then they point to an IP address that could (and probably would) be given to another instance spun up by the provider, on behalf of a random person.

Also, I'm not worried about someone providing bad information to the instance. Since it's using built-in certificates to make all its connections (for the setup) over HTTPS, to locations on the internet that are under your sole control, if someone can man-in-the-middle that, they either have access to the instance pre- or post-boot, or they control the certificate store of the instance, in which case, I again have larger concerns.

Lastly, I'm not worried about someone using the info that has to be made public:

- The instance only serves up information that will go into a public `SSHFP` DNS record
- You only publish DNS information about the instance that's necessary to run a website from it
- SSH public keys are safe to make public

The only thing that isn't absolutely necessary for connecting to the instance, or visiting a website hosted by it, is for your SSH public key to remain public.

Let's Encrypt [has policies on how often you can request a certificate](https://letsencrypt.org/docs/rate-limits/), which would limit how frequently this procedure could be used to spin up an instance.

If I run into that limit, I'll figure something else out.
