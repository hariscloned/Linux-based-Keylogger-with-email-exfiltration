# Linux-based-Keylogger-with-email-exfiltration
This is a linux based python keylogger with AES log encryption and Email Exfiltration 


📄 Project Overview
This project implements a Python-based keylogger for Linux that securely captures user keystrokes, encrypts them using AES (via Fernet), and sends the encrypted logs to a specified email address at regular intervals. The logs are stored in a hidden directory and automatically encrypted every two minutes to ensure confidentiality. A custom decryption utility is also provided for log retrieval and decryption.

🛠️ Key Features
-Encrypted Keylogging
Captures all keystrokes with timestamps and stores them in an encrypted format using AES (Fernet).

-Periodic Auto-Encryption & Archival
Automatically encrypts the log file every 2 minutes to protect data integrity and confidentiality.

-Email Reporting System
Securely sends encrypted logs to a specified email using SMTP over SSL.

-Custom Decryption Utility
Provides a dedicated script to decrypt the logs using the AES key.

-Stealth & Persistence
Runs silently in the background and stores logs in a hidden system directory. When executed via the ELF file, the keylogger operates in the background and can only be terminated by manually killing the process.

📂 Project Structure
File Name	Description
keylogger.py	Core script that captures keystrokes, encrypts logs, and handles email reporting.
Decrypt.py	Decryption utility to recover and view encrypted log files.
Keylogger Executable	ELF executable that stealthily runs the keylogger on Linux and requires manual process termination.
Path.txt	Stores the path to the hidden directory where logs and keys are saved.

🔒 Background
While keyloggers are often linked to malicious activity, they are essential tools in cybersecurity research, digital forensics, and penetration testing. This project focuses on ethical use in controlled lab environments to understand input capture mechanisms, encryption, and secure data handling. It uses:

pynput for keystroke capture
cryptography.fernet for AES encryption
smtplib for secure log transfer via email

🚀 Getting Started
Prerequisites:
Linux OS
Python 3.x

-Required Python libraries:
"pip install pynput cryptography"

-Running the Keylogger (Python Script)

"python3 keylogger.py"

The keylogger will:
Start capturing keystrokes
Encrypt logs every 2 minutes
Send logs via email

-Running the Keylogger (ELF Executable):
"./ncys2_keylogger"

-When executed via the ELF file:
The keylogger will run stealthily in the background.
-It can only be shut down by manually killing the process.

-Decrypting Logs:

"python3 Decrypt.py"
Provide the encrypted log name as an argument in the command.

⚙️ Tools & Technologies

Python 3
Linux
pynput (Keyboard input capture)
cryptography (Fernet/AES)
smtplib (Email via SMTP over SSL)

⚠️ Disclaimer
This project is intended strictly for educational and ethical purposes. Unauthorized deployment of keyloggers is illegal and unethical. Please ensure all testing is done in controlled environments with proper authorization.
