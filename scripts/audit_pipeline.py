import os
import site

def scan():
    print("[!] SYSTEM AUDIT: Searching for Malicious Persistence Hooks...")
    suspicious_found = False
    
    # Scan all Python site-package locations
    for path in site.getsitepackages():
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".pth"):
                    file_path = os.path.join(path, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        # Signatures of our attack
                        if "base64" in content or "requests" in content:
                            print(f"[CRITICAL THREAT] Found unauthorized startup hook: {file_path}")
                            print(f"    Payload Detected: {content[:50]}...")
                            suspicious_found = True
    
    if not suspicious_found:
        print("[+] Environment appears clean.")

if __name__ == "__main__":
    scan()
