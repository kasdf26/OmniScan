#! /usr/bin/env python3.6

import socket
import sys


def smtpscan(settings, n, m):
    print("INFO: Trying SMTP Enum on %s" % settings.targets[n].ip)
    tar_ip = settings.targets[n].ip
    port = settings.targets[n].services[m].port
    names = open('/usr/share/wfuzz/wordlist/fuzzdb/wordlists-user-passwd/names/namelist.txt', 'r')
    notes = '~' * 20
    notes += '\n SMTP scan results'
    notes += '\n' + '~' * 20
    for name in names:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect=s.connect((tar_ip, int(port)))
        banner=s.recv(1024)
        s.send('HELO test@test.org \r\n')
        result= s.recv(1024)
        s.send('VRFY ' + name.strip() + '\r\n')
        result=s.recv(1024)
        if ("not implemented" in result) or ("disallowed" in result):
            notes += ("INFO: VRFY Command not implemented on " + sys.argv[1])
            break
        if ("250" in result or "252" in result) and ("Cannot VRFY" not in result):
            notes += "[*] SMTP VRFY Account found on " + tar_ip + ": " + name.strip()
        s.close()
    settings.tool_notes(n, '', notes, 'smtp-summary.txt')
    print("INFO: completed SMTP Enum on %s" % settings.targets[n].ip)