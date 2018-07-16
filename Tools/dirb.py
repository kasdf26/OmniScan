#!/usr/bin/env python3.6
import http.client
import subprocess
from os import listdir



class Dirb:
    @staticmethod
    def wget(url):
        parts = url.split('/',3)
        print(parts)
        if 'https' in url:
            ssl = True
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            h = http.client.HTTPSConnection(parts[2], context=context)
        else:
            h = http.client.HTTPConnection(parts[2])

        headers ={b"User-Agent": b"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                    b"Accept": b"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    b"Accept-Language": b"en-US, en;q = 0.5",
                    b"Accept-Encoding": b"deflate"}

        h.request("GET", '/'+parts[3], headers)
        r = h.getresponse()
        print(r.getheaders())
        header = r.getheaders()

        for y in range(0, header.__len__()):
            if header[y][0] == 'Location':
                return parts[0]+'//'+parts[2]+'/'+header[y][1]

        # if 'set-cookie' in header:
        #     for x in header:
        #         if x[0] == 'Set-Cookie':
        #             headers += {b'Cookie': x[1]}
        #             break
        #     h.request("GET", '/' + parts[3], headers)
        #     r = h.getresponse()
    @staticmethod
    def all_web(settings, n):
        if len(settings.targets) <= n:
            print('[ERROR] index out of bounds')
            return
        y = 0
        for x in settings.targets[n].services:
            if x.web:
                print("[INFO] {Dirb.all_web}[%s,%s] Starting scan of port: %s " % (type(settings).__name__, n, x.port))
                Dirb.scan(settings, y, indx=n)
            y += 1

    @staticmethod
    def summary(n, settings, dirs, pages):
        notes = '~'*20
        notes += '\n DIRECTORIES FOUND'
        notes += '\n' + '~'*20
        for x in dirs:
            notes += '\n'+x

        notes = '\n'+'~' * 20
        notes += '\n Pages FOUND'
        notes += '\n'+'~' * 20
        for x in pages:
            notes += '\n'+x

        settings.tool_notes(n, '', notes, 'dirb-summary.txt')

    @staticmethod
    def scan(settings, m, indx=None, ip=None):
        m = int(m)
        if ip is None and indx is None:                            # Function to check targets ip
            print('[ERROR] Need to specify ip or index')
            return
        elif ip is not None:
            x = int(ip)
            n = int(settings.find_target(x))                        # find target or create new
        else:
            n = int(indx)
        tar_ip = settings.targets[n].ip                         # Set target ip
        out_dir = settings.tool_dir(n, 'dirb')
        proto = settings.targets[n].services[m].web_proto()
        port = settings.targets[n].services[m].port
        url = proto+tar_ip+ ':' + port + '/'        # Build url of target

        folders = ["/opt/wordlists/dirb", "/opt/wordlists/dirb/vulns"]  # Folders with word lists

        print("INFO: Starting dirb scan for " + url)
        for folder in folders:
            for filename in listdir(folder):

                outfile = " -o " + out_dir + "port-"+port + "_dirb_" + filename
                dirbscan = "dirb %s %s/%s %s -S -r" % (url, folder, filename, outfile)
                print("[INFO] {Dirb.scan} scan of %s with: %s"% (url, filename))
                subprocess.check_output(dirbscan, shell=True)


    @staticmethod
    def importdirb(settings,n,m):
        folders = ["/usr/share/dirb/wordlists", "/usr/share/dirb/wordlists/vulns"]  # Folders with word lists
        out_dir = settings.tool_dir(n, 'dirb')
        port = settings.targets[n].services[m].port
        found = []  # list to store pages
        found_dir = []  # list to store directories
        print("[INFO] {Dirb.importdirb}: Starting import")
        for folder in folders:
            for filename in listdir(folder):
                infile =  out_dir + "port-" + port + "_dirb_" + filename
                f = open(infile, 'r')
                for line in f:
                    if "+" in line:
                        if line not in found:
                            tmp = line.replace("\n", "")
                            found.append(tmp)
                    elif "==>" in line:
                        if line not in found_dir:
                            tmp = line.replace("\n", "")
                            found_dir.append(tmp)
        if found[0] != "" and found_dir[0] != "":
            print("[INFO] {Dirb.importdirb}{%s} import complete with results " % settings.targets[n].ip)
        else:
            print("[INFO] {Dirb.importdirb}{%s} Possibly no results found " % settings.targets[n].ip)
        found = list(set(found))
        found_dir = list(set(found_dir))
        settings.targets[n].services[m].pages = found
        settings.targets[n].services[m].dirs = found_dir
        Dirb.summary(n, settings, found_dir, found)


if __name__ == "__main__":
    from Tools.discovery import Discovery
    from notes import *

    f = open('/opt/Scripts/targets.txt', 'r')
    scope = Settings(r'/opt/test/testing/')
    for ip in f:
        tmp = ip.replace("\n", "")
        scope.targets.append(Target(tmp))

    Discovery.integrateNmap(scope, scope.Workspace+scope.targets[0].ip+'/'+'nmap/'+scope.targets[0].ip+'-top-ports.xml')
    port_index = scope.targets[0].find_port(8000)
    #Discovery.host_summary(scope, 0)
    #Dirb.all_web(scope, 0)
    Dirb.importdirb(scope,0,port_index)
    url = 'http://10.11.1.252:8000/index.php'
    x = Dirb.wget(url)
    print(x)
