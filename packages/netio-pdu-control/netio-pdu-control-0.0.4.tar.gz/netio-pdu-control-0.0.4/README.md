# netio-pdu-control
Library for control and monitoring of Netio PowerPDU devices over LAN.

This library has been implemented by IFAE (www.ifae.es) control software department.

## CLI tool
You may run the terminal client with `python -m netio_pdu_control`. By default it assumes that `netio_pdu_credentials.cfg` is in the same folder or XDG's config home or directories. A different path can be specified with the argument `--credentials / -c`.

Please run the `-h / --help` argument for a description of every argument.

### Credentials file example
```
[office01]
EntryPoint = http://172.16.7.225
ReadUser = read
ReadPassword = read
WriteUser = write
WritePassword = write

[workshop]
EntryPoint = http://172.16.7.226
ReadUser = read
ReadPassword = read
WriteUser = segona
WritePassword = segona

[lab]
EntryPoint = http://192.168.4.20
ReadUser = admin
ReadPassword = 1234
WriteUser = admin
WritePassword = 1234

```