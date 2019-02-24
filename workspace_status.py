import subprocess, sys, os

def main():
    git_hash = get_git_hash(".")
    git_is_dirty = is_git_dirty(".")

    git_is_dirty_str = "0"
    if git_is_dirty:
        git_is_dirty_str = "1"

    print("GIT_COMMIT_HASH {}".format(git_hash))
    print("GIT_DIRTY {}".format(git_is_dirty_str))

    #git_status_path = os.path.normpath(os.path.join(__file__, "..", ".git_status"))
    #with open(os.path.join(git_status_path, "commit_hash"), "w") as f:
    #    f.write(git_hash)

    #with open(os.path.join(git_status_path, "workspace_dirty"), "w") as f:
    #    f.write(git_is_dirty_str)

def get_git_hash(path):
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return out.encode("ascii").strip()

def is_git_dirty(path):
    p = subprocess.Popen(["git", "status", "-s"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return not not out.encode("ascii").strip()

if __name__ == "__main__":
    main()