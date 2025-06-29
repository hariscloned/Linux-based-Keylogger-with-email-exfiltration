from cryptography.fernet import Fernet
import os

# === Folder and Key Paths ===
FOLDER_NAME = os.path.expanduser("~/Documents/.ncys2_project")
KEY_FILE = os.path.join(FOLDER_NAME, "key.key")

def decrypt_log():
    # Prompt for encrypted file name
    file_name = input("Enter the name of the encrypted log file (e.g., NCYS2_log_20250416_102028.encrypted): ").strip()
    enc_log_path = os.path.join(FOLDER_NAME, file_name)

    if not os.path.exists(enc_log_path):
        print(f"[!] File not found: {enc_log_path}")
        return

    output_file = os.path.join(FOLDER_NAME, f"{os.path.splitext(file_name)[0]}_decrypted.txt")

    try:
        # Load the key
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        # Read the encrypted data
        with open(enc_log_path, "rb") as enc_file:
            encrypted_data = enc_file.read()

        # Decrypt the content
        decrypted_data = fernet.decrypt(encrypted_data)

        # Write decrypted data to output file
        with open(output_file, "wb") as dec_file:
            dec_file.write(decrypted_data)

        print(f"[✓] Log decrypted successfully.\nSaved at: {output_file}")

    except Exception as e:
        print(f"[!] Decryption failed: {e}")

if __name__ == "__main__":
    decrypt_log()
