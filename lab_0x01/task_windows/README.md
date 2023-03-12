# Lab 0x01 (Windows Task)

## The task

We have a malicious binary and we have to use Process Monitor and API Monitor to see how this executable interacts with the Operating System. (Hint: Check for internet connections and registry changes)

## Solution

Firstly, i started the Process Monitor and checked for internet activity using the automatic filter that this tool has. It didn't appear anything. So then i tried with API Monitor and found this URL that it connects to and if we look at it we can determine that our malware is actually a stager that downloads a second stage malware that will actually do the malicious activity.

![alt text](url.png?raw=true)

In order to look for registry changes i used process monitor to filter for the *Process Name*, and the following *Operations*: **RegSetValue**,  **RegCreateKey** and **RegSaveKey**.

![alt text](regs.png?raw=true)

If we look at the screen shot above, we can see that the first RegSetValue is applied on the *\Software\Microsoft\Windows\CurrentVersion\Run* registry key that is used for launching executables at logon time. This way the malware is restart resistant.

Then the malware modifies the **ProxyBypass**, **IntranetName**, **UNCAsIntranet** and **AutoDetect** entries from the *\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap* registry key.

The malware enables the **ProxyBypass** policy entry, so the sites which bypass the proxy server are mapped into the Intranet Zone.

The malware enables the **IntranetName** policy entry, so local sites which are not explicitly mapped into a zone are considered to be in the Intranet Zone.

The malware enables the **UNCAsIntranet** policy entry, so all network paths are mapped into the Intranet Zone.

The malware disables the **AutoDetect** policy entry, so the intranet mapping rules will NOT be applied automatically if the computer belongs to a domain.

This way when the malicious URL, that the malware is communicating to, is added to the Intranet Zone it will become NOT suspicious for the IDS, IPS and Antivirus Software.

