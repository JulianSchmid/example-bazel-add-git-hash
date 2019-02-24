import argparse, sys, os

class VariableStore:
    def __init__(self, values, is_reliable, name_prefix):
        self.values = values
        self.name_prefix = name_prefix
        self.is_reliable = is_reliable

    def get(self, name):
        return self.values.get(self.name_prefix + name)

class MultipleVariableStore:
    def __init__(self):
        self.values = []

    def add_file(self, path, is_reliable, name_prefix = ""):
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
        self.values.append(VariableStore(result, is_reliable, name_prefix))

    def get(self, name):
        for l in self.values:
            result = l.get(name)
            if result is not None:
                return (result, l.is_reliable)
        return (None, False)

def main():

    parser = argparse.ArgumentParser(description='Bake a git hash into a header & source.')
    parser.add_argument('--header',
                        required=True,
                        help='output header file')
    parser.add_argument('--source',
                        required=True,
                        help='output source file')
    parser.add_argument('--volatile_file',
                         required=True,
                         help='file containing the volatile variables')
    parser.add_argument('--stable_file',
                         required=True,
                         help='file containing the stable variables')
    parser.add_argument('--commit_hash_name',
                         help='variablename of the hash')
    parser.add_argument('--workspace_dirty_name',
                         help='variablename of the boolean communicating if the workspace has no local changes')
    
    args = parser.parse_args()

    variables = MultipleVariableStore()
    variables.add_file(args.stable_file, True, "STABLE_")
    variables.add_file(args.volatile_file, False)

    (commit_hash, commit_hash_reliable) = variables.get(args.commit_hash_name.strip())
    (is_dirty_str, is_dirty_reliable) = variables.get(args.workspace_dirty_name.strip())
    is_dirty = "0" != is_dirty_str

    print("Generating {}".format(args.header))
    with open(args.header, "w") as f:
        f.write("""
#pragma once

struct VersionInfo {{
    static char git_hash[{hash_len}];
    static bool git_hash_reliable;
    static bool git_is_workspace_dirty;
    static bool git_is_workspace_dirty_reliable;
}};
""".format(hash_len=len(commit_hash)));

    print("Generating {}".format(args.source))
    with open(args.source, "w") as f:
        hash_array = ""
        first = True
        for c in commit_hash: 
            if not first:
                hash_array += ', '
            else:
                first = False
            hash_array += "'"
            hash_array += c
            hash_array += "'"

        f.write("""
#include "{header_path}"

char VersionInfo::git_hash[{hash_len}] = {{ {hash_array} }};
bool VersionInfo::git_hash_reliable = {hash_reliable};
bool VersionInfo::git_is_workspace_dirty = {is_dirty};
bool VersionInfo::git_is_workspace_dirty_reliable = {is_dirty_reliable};
""".format(
                hash_len = len(commit_hash),
                hash_array = hash_array,
                hash_reliable = "true" if commit_hash_reliable else "false",
                header_path = args.header,
                is_dirty = "true" if is_dirty else "false",
                is_dirty_reliable = "true" if is_dirty_reliable else "false",
            )
        )

if __name__ == "__main__":
    main()