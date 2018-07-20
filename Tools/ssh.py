import subprocess


def ssh_scan(settings, n, m):               # Change
    print("[INFO] [host: %s] {ssh_scan} starting enumeration" % settings.targets[n].ip)
    tar_ip = settings.targets[n].ip
    port = settings.targets[n].services[m].port
    out_dir = settings.tool_dir(n, 'ssh')  # Change tool dir name
    outfile = out_dir + "port-%s-ssh-hydra.txt" % port
    errfile = out_dir+'error.log'
    notes = '~' * 20
    notes += '\n ssh_scan scan results'     # Change
    notes += '\n' + '~' * 20
    command = settings.proxypass + " hydra -t 4 -L /opt/wordlists/userlist -P " \
                                   "/opt/wordlists/offsecpass -f -o " \
                                   "%s -u %s -s %s ssh" % (outfile, tar_ip, port)
    try:
        #print("[INFO] [host: %s] {ssh_scan} starting enumeration" % settings.targets[n].ip)
        results = subprocess.check_output(command, shell=True, stderr=errfile)
        resultarr = results.split("\n")
        for result in resultarr:
            if "login:" in result:
                notes += "[*] Valid ssh credentials found: " + result
    except:
        print("[ERROR] [host: %s] {ssh_scan} Enumeration Failed" % settings.targets[n].ip)

    settings.tool_notes(n, '', notes, 'ssh-summary.txt')
    print("[INFO] [host: %s] {ssh_scan} Completed enumeration" % settings.targets[n].ip)

