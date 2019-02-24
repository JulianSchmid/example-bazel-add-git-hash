import argparse, sys, os

def read_values(path):
    result = {}
    with open(path, "r") as f:
        for entry in f.read().split("\n"):
            if entry:
                key_value = entry.split(' ', 1)
                key = key_value[0].strip()
                if key in result:
                    sys.stderr.write("Error: Duplicate key '{}'\n".format(key))
                    sys.exit(1)
                else:
                    result[key] = key_value[1].strip()
    return result

def main():

    parser = argparse.ArgumentParser(description='Bake a git hash into a header & source.')
    parser.add_argument('--header',
                        required=True,
                        help='output header file')
    parser.add_argument('--source',
                        required=True,
                        help='output source file')
    # parser.add_argument('git_hash', 
    #                     help='the git hash')
    parser.add_argument('--version_file',
                         required=True,
                         help='file containing the current commit hash')
    parser.add_argument('commit_hash_name',
                         help='name of the hash')
    
    args = parser.parse_args()

    stable_values = read_values(args.version_file)
    h = stable_values[args.commit_hash_name.strip()]

    #with open(args.commit_hash_file, "r") as f:
    #    h = f.read()

    is_dirty = False
    #with open(args.workspace_dirty_file, "r") as f:
    #    is_dirty = f.read().strip() != "0"

    print("Generating {}".format(args.header))
    with open(args.header, "w") as f:
        f.write("""
#pragma once

struct VersionInfo {{
    static char git_hash[{0}];
    static bool git_is_workspace_dirty;
}};
""".format(len(h)));

    print("Generating {}".format(args.source))
    with open(args.source, "w") as f:
        hash_array = ""
        first = True
        for c in h: 
            if not first:
                hash_array += ', '
            else:
                first = False
            hash_array += "'"
            hash_array += c
            hash_array += "'"

        f.write("""
#include "{2}"

char VersionInfo::git_hash[{0}] = {{ {1} }};
bool VersionInfo::git_is_workspace_dirty = {3};
""".format(
                len(h),
                hash_array,
                args.header,
                "true" if is_dirty else "false"
            )
        )

if __name__ == "__main__":
    main()