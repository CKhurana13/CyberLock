# CyberLock: Educational Ransomware Simulation

CyberLock is a Windows desktop program written in Python. It recreates the visual experience of a ransomware lock screen in a controlled way, then walks the audience through prevention tips.

**Safe, non-destructive demo.** CyberLock does not encrypt, delete, modify or upload any file, and makes no system changes. It only shows a full-screen, ransomware-style lock screen so audiences can see what an attack looks like and learn how to prevent one.

---

**Why I Built It**

Most people have heard of ransomware but have never seen how it looks or how fast it can feel overwhelming. A live, safe demo makes the lesson stick.

I built CyberLock for the awareness programs I take part in as a cyber crime investigation intern, to help citizens and students recognise the signs of an attack and know what to do.

---

**Features**

- Full-screen ransomware-style lock overlay with Matrix / glitch visual effects
- Keyboard and mouse input blocking while the demo is active
- Recovery-key popup (opened with Shift + Z or a button) that unlocks the screen when the correct key is entered
- Hidden presenter exit (Ctrl + Shift + X) so the demo can always be ended safely
- Awareness screen shown after unlocking, with ransomware prevention tips
- Auto-exit timeout so the screen can never stay locked
- No file encryption, no file access, no network activity, no persistence

---

**Prevention Tips Covered**

- Keep offline backups
- Do not open unknown attachments
- Install software updates
- Turn on multi-factor authentication
- Report incidents to IT or the cyber cell

---

**Download and Run (Windows)**

No Python is needed.

1. Go to the Releases page and download CyberLock.zip.
2. Extract the zip and open the CyberLock folder.
3. Run CyberLock.exe.

**Note:** Windows SmartScreen or antivirus may show a warning. The program is unsigned and behaves like a lock screen (full-screen window, input blocking), which security tools often flag. This is expected for this kind of demo. The complete source code is in this repository, so you can read exactly what it does.

---

**Presenter Notes**

- Know the exit shortcut (Ctrl + Shift + X) and the recovery key before running it.
- Run it only on a computer you own or have permission to use.
- Tell your audience beforehand that it is a demo.

---

**Tech Stack**

- Python
- Tkinter
- PyInstaller

---

**Responsible Use**

This project is for education and awareness only.

- Do not use it to scare, trick or harm anyone.
- Do not run it on devices you do not have permission to use.
- It must not be modified to add real encryption, file deletion or any other harmful behaviour.

The author takes no responsibility for misuse.

---

**Author**

Cheshta Khurana
B.Tech (Industrial IoT) | Cybersecurity enthusiast

LinkedIn: https://www.linkedin.com/in/cheshta-khurana-315170332
GitHub: https://github.com/CKhurana13
