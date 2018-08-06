#! /usr/bin/env python3.6

import subprocess


def ftp_scan(settings, n, m):
    print("[INFO] [host: %s] {ftp_scan} starting enumeration" % settings.targets[n].ip)
    tar_ip = settings.targets[n].ip
    port = settings.targets[n].services[m].port
    out_dir = settings.tool_dir(n, 'ftp')
    outfile = out_dir + "nmap-ftp"

    notes = '~' * 20
    notes += '\n ftp_scan scan results'
    notes += '\n' + '~' * 20

    # try:
    print("[INFO] [host: %s] {ftp_scan} starting nmap ftp enumeration" % settings.targets[n].ip)
    ftpnmap = settings.proxypass + "nmap -sV -Pn -vv -p %s --script=ftp-anon,ftp-bounce," \
              "ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221" \
              " -oN %s %s" % (
                  port, outfile, tar_ip)
    notes += '\n Command: ' + ftpnmap
    results = subprocess.check_output(ftpnmap, shell=True)
    notes += results.decode('ascii')
    # except:
    #     print("[ERROR] [host: %s] {ftp_scan} nmap Enumeration Failed" % settings.targets[n].ip)

    try:
        outfile = out_dir + "hydra-ftp"
        print("[INFO] [host: %s] {ftp_scan} starting ftp hydra" % settings.targets[n].ip)
        HYDRA = settings.proxypass + "hydra -t 4 -L /opt/wordlists/userlist -P " \
                "/opt/wordlists/offsecpass " \
                "-f -o %s -u %s -s %s ftp" % (
        outfile, tar_ip, port)
        results = subprocess.check_output(HYDRA, shell=True).decode('ascii')
        resultarr = results.split("\n")
        for result in resultarr:
            if "login:" in result:
                notes += "[*] Valid ftp credentials found: " + result
    except:
        print("[ERROR] [host: %s] {ftp_scan} HYDRA Enumeration Failed" % settings.targets[n].ip)

    settings.tool_notes(n, '', notes, 'ftp-summary.txt')
    print("[INFO] [host: %s] {ftp_scan} Completed enumeration" % settings.targets[n].ip)
