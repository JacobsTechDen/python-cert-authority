import subprocess
import sys

script_name = sys.argv[0]

if len(sys.argv) != 2:
    print("Usage: {} <path_to_certificate_file>".format(script_name))
    sys.exit(1)

path_to_cert = sys.argv[1]

def add_certificate_to_trusted_root(cert_file_path):
    try:
        subprocess.run(['certutil', '-addstore', 'Root', cert_file_path], check=True)
        print("Certificate added to trusted root store successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding certificate: {e}")
    except FileNotFoundError:
        print("certutil not found. Make sure you are running this script with administrative privileges.")

if __name__ == "__main__":
    add_certificate_to_trusted_root(path_to_cert)
