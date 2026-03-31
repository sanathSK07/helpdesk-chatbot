# ============================================================
# IT Helpdesk Knowledge Base
# Author: Sanath | York University
# ============================================================
# I created 10 realistic IT helpdesk articles covering the most
# common support topics: VPN, passwords, email, WiFi, printers,
# software, Teams, laptops, security, and onboarding. In a real
# company, these would come from actual documentation — I wrote
# realistic versions to demonstrate the RAG pipeline.
# ============================================================

KNOWLEDGE_BASE = [
    {
        "id": "vpn-setup",
        "title": "VPN Setup and Troubleshooting Guide",
        "category": "Network",
        "content": """To set up the company VPN on your device, follow these steps:
1. Download the GlobalProtect VPN client from the IT portal at https://itportal.company.com/vpn
2. Install the application and restart your computer
3. Open GlobalProtect and enter the portal address: vpn.company.com
4. Sign in using your company email and Active Directory password
5. Click Connect and wait for the green checkmark

Common VPN issues and solutions:
- If the VPN won't connect, first check your internet connection by opening a website
- If you get an "Authentication Failed" error, reset your password at https://passwordreset.company.com
- If the VPN is slow, try disconnecting and reconnecting, or switch to a different WiFi network
- If you see "Portal Unreachable", the VPN server may be under maintenance. Check the IT status page
- For Mac users: make sure you have allowed the GlobalProtect system extension in System Preferences > Security & Privacy
- The VPN automatically disconnects after 8 hours of inactivity. Simply reconnect when needed."""
    },
    {
        "id": "password-reset",
        "title": "Password Reset and Account Recovery",
        "category": "Account Management",
        "content": """To reset your company password:
1. Go to https://passwordreset.company.com
2. Enter your company email address
3. Verify your identity through the authenticator app or SMS code
4. Create a new password following these requirements:
   - Minimum 12 characters
   - At least one uppercase letter, one lowercase letter, one number, and one special character
   - Cannot be the same as your last 10 passwords
   - Cannot contain your name or username

Password expires every 90 days. You will receive email reminders starting 14 days before expiration.

If you are locked out of your account after too many failed attempts:
- Wait 30 minutes for the automatic unlock
- Or contact the IT Help Desk at ext. 5555 or helpdesk@company.com for immediate unlock
- Have your employee ID ready when calling

For Multi-Factor Authentication (MFA) issues:
- If you lost your phone, contact IT to reset your MFA
- You can use backup codes stored in your company secure vault
- The IT Help Desk can provide a temporary bypass code valid for 24 hours"""
    },
    {
        "id": "email-setup",
        "title": "Email Configuration and Troubleshooting",
        "category": "Communication",
        "content": """Company email uses Microsoft 365 (Outlook).

Setting up email on your devices:
- Desktop: Outlook is pre-installed on company laptops. Sign in with your company email.
- Mobile (iOS): Go to Settings > Mail > Accounts > Add Account > Microsoft 365
- Mobile (Android): Download Microsoft Outlook from Play Store and sign in
- Web: Access email at https://outlook.office365.com

Email storage limit is 50GB per mailbox. If emails are not sending, check if your mailbox is full, ensure you're connected to the internet, check if the attachment is under the 25MB limit, and look in your Outbox for stuck emails. For shared mailboxes or distribution lists, submit a request through the IT Service Portal."""
    },
    {
        "id": "wifi-setup",
        "title": "Office WiFi Network Setup",
        "category": "Network",
        "content": """Company office WiFi networks:
- CorpNet-Secure: Main work network. Requires company credentials.
- CorpNet-Guest: Guest network for visitors. Limited bandwidth, no internal access.

Connecting to CorpNet-Secure:
1. Select CorpNet-Secure from your WiFi list
2. Enter your company email as username
3. Enter your Active Directory password
4. Accept the security certificate when prompted

If you cannot connect: forget the network and reconnect, make sure your password hasn't expired, restart your WiFi adapter, or on Windows run 'netsh wlan delete profile name=CorpNet-Secure' in Command Prompt and reconnect."""
    },
    {
        "id": "software-install",
        "title": "Software Installation and Requests",
        "category": "Software",
        "content": """Company-approved software can be installed through the Software Center (Windows) or Self Service (Mac). Pre-approved software includes: Microsoft Office 365, Zoom, Slack, Chrome, Firefox, Adobe Reader, VS Code, Postman, and Docker Desktop (requires developer group membership).

To request software not in the Software Center, submit a form at https://itportal.company.com/software-request with the software name, version, business justification, and estimated users. IT Security reviews within 3-5 business days. Installing software outside of Software Center is not permitted on company devices."""
    },
    {
        "id": "printer-setup",
        "title": "Printer Setup and Troubleshooting",
        "category": "Hardware",
        "content": """To add a printer on Windows: Settings > Printers & Scanners > Add a printer. Select your floor's printer (format: PRN-Floor#-Location). On Mac: System Preferences > Printers & Scanners > Add (+).

Common issues: Paper jam — open front panel and remove jammed paper. Print job stuck — cancel all jobs and restart Print Spooler service. Poor quality — run cleaning cycle from printer touch screen. Cannot find printer — make sure you're on CorpNet-Secure, not the guest network. Color printing is available only on Floor 1 and Floor 5."""
    },
    {
        "id": "teams-meeting",
        "title": "Microsoft Teams Meetings and Collaboration",
        "category": "Communication",
        "content": """Microsoft Teams is the company's primary collaboration platform. To start a meeting: open Teams Calendar, click New Meeting, add participants. For external participants, they can join via the meeting link without a Teams account.

If your camera or microphone isn't working: check Teams Settings > Devices, make sure no other app is using the camera, try unplugging and re-plugging USB devices, or restart Teams. Recording: click three dots > Start Recording. Recordings save to OneDrive automatically."""
    },
    {
        "id": "laptop-issues",
        "title": "Laptop Performance and Hardware Issues",
        "category": "Hardware",
        "content": """If your laptop is running slowly: 1. Restart (don't just close the lid), 2. Close unnecessary browser tabs, 3. Check for OS updates, 4. Clear temporary files, 5. Run a virus scan through CrowdStrike.

For hardware issues: cracked screen — submit a ticket immediately. Battery issues — request replacement if under 2 years old. Keyboard problems — use external keyboard temporarily. Laptops are replaced on a 3-year cycle. Submit replacement requests at https://itportal.company.com/hardware with your asset tag number (sticker on bottom starting with 'ASSET-')."""
    },
    {
        "id": "security-awareness",
        "title": "Cybersecurity Best Practices",
        "category": "Security",
        "content": """Phishing protection: never click unexpected links, check sender addresses carefully, report suspicious emails using the 'Report Phishing' button. IT will never ask for your password via email.

Data protection: don't share company data on personal email or cloud storage, use only approved tools (OneDrive, SharePoint, Teams), lock your screen when away (Win+L or Ctrl+Cmd+Q). Don't plug unknown USB drives into your laptop.

If you suspect a security breach: contact security@company.com immediately. If you clicked a phishing link, disconnect from WiFi and call IT at ext. 5555."""
    },
    {
        "id": "onboarding-it",
        "title": "New Employee IT Onboarding Guide",
        "category": "Onboarding",
        "content": """Day 1 checklist: 1. Pick up laptop from IT (Room 101, Floor 1), 2. Sign in with temporary credentials from welcome email, 3. Change your password at https://passwordreset.company.com, 4. Set up MFA using Microsoft Authenticator, 5. Connect to CorpNet-Secure WiFi, 6. Verify Outlook email, 7. Install Teams and join your team channels, 8. Bookmark https://itportal.company.com.

First week: complete Cybersecurity Awareness Training, set up VPN for remote work, request additional software, add your floor's printer. Your IT Buddy contact is in your welcome email. Urgent issues: IT Help Desk at ext. 5555 or helpdesk@company.com."""
    }
]

if __name__ == "__main__":
    print(f"✅ Knowledge base loaded: {len(KNOWLEDGE_BASE)} documents")
    for doc in KNOWLEDGE_BASE:
        print(f"   [{doc['category']}] {doc['title']} ({len(doc['content'])} chars)")
