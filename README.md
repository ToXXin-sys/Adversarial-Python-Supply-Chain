# Adversarial-Python-Supply-Chain: CI/CD Persistence Lab

## 🛡️ Executive Summary
This project is a high-fidelity simulation of a **Supply Chain Attack** targeting a CI/CD pipeline. As a **CompTIA PenTest+** certified researcher, I developed this lab to demonstrate a **TOCTOU (Time-of-Check to Time-of-Use)** bypass. By injecting a malicious `.pth` startup hook during the build phase, I achieved persistent code execution that fires every time the Python interpreter is invoked, successfully exfiltrating environment variables from an isolated container.

---

## 🏗️ Architecture
The lab consists of three main components:
1.  **The Poisoned Dependency (`internal_lib/`):** A library containing a malicious `setup.py`.
2.  **The CI/CD Pipeline (`.github/workflows/main.yml`):** A GitHub Actions workflow simulated via `act`.
3.  **The Forensic Audit (`scripts/audit_env.py`):** A defensive tool used to detect unauthorized persistence hooks.

---

## 🛠️ Rapid Lab Setup (Local Recreation)
If you are cloning this to a fresh Kali environment, run these commands to initialize the environment:

```bash
# 1. Initialize the directory structure
mkdir -p py-supply-chain-lab/{internal_lib,victim_app,scripts,.github/workflows}
cd py-supply-chain-lab

# 2. Install dependencies (Kali Linux)
sudo apt update && sudo apt install docker.io -y
curl -s [https://raw.githubusercontent.com/nektos/act/master/install.sh](https://raw.githubusercontent.com/nektos/act/master/install.sh) | sudo BINDIR=/usr/local/bin bash
sudo mv /usr/local/bin/act /usr/local/bin/gh-act

# 3. Create the Victim Application
echo "print('--- [VICTIM APP] ---')" > victim_app/app.py
echo "print('Initializing secure database connection...')" >> victim_app/app.py

# 4. Create the Audit Script
cat <<EOF > scripts/audit_env.py
import os, site
def scan():
    print("[!] SYSTEM AUDIT: Searching for Malicious Persistence Hooks...")
    for path in site.getsitepackages():
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".pth"):
                    print(f"[CRITICAL] Found hook: {os.path.join(path, f)}")
if __name__ == "__main__": scan()
EOF
