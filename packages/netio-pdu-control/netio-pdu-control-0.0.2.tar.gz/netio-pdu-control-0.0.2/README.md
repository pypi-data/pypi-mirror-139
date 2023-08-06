# netio-pdu-control
Library for control and monitoring of Netio PowerPDU devices over LAN.

This library has been implemented by IFAE (www.ifae.es) control software department.

## CLI tool
You may run the terminal client with `python -m netio_pdu_control`. By default it assumes that `credentials.cfg` is in the same folder, but a different path can be specified with the argument `--credentials / -c`.

### Credentials file example
```
[office01]
EntryPoint = http://192.168.1.33
ReadUser = read
ReadPassword = read
WriteUser = write
WritePassword = write

[workshop]
EntryPoint = http://192.168.1.17
ReadUser = admin
ReadPassword = admin
WriteUser = admin
WritePassword = admin

[lab]
EntryPoint = http://192.168.4.20
ReadUser = admin
ReadPassword = 1234
WriteUser = admin
WritePassword = 1234
```