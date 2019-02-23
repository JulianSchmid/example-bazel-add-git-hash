import subprocess, sys, os

def main():
    git_hash = get_git_hash(".")
    print("STABLE_GIT_HASH {}".format(get_git_hash(".")))

    git_status_path = os.path.normpath(os.path.join(__file__, "..", ".git_status"))
    with open(os.path.join(git_status_path, "commit_hash"), "w") as f:
        f.write(git_hash)

def get_git_hash(path):
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return out.encode("ascii").strip()

if __name__ == "__main__":
    main()