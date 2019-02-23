import subprocess, sys

def main():
    print("GIT_HASH {}".format(get_git_hash(".")))

def get_git_hash(path):
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return out.encode("ascii")

if __name__ == "__main__":
    main()