import argparse, sys, os

class VariableStore:
    def __init__(self, values, name_prefix):
        self.values = values
        self.name_prefix = name_prefix

    def get(self, name):
        return self.values.get(self.name_prefix + name)

class MultipleVariableStore:
    def __init__(self):
        self.values = []

    def add_file(self, path, name_prefix = ""):
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
        self.values.append(VariableStore(result, name_prefix))

    def get(self, name):
        for l in self.values:
            result = l.get(name)
            if result is not None:
                return result
        return None

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
    parser.add_argument('commit_hash_name',
                         help='variablename of the hash')
    
    args = parser.parse_args()

    variables = MultipleVariableStore()
    variables.add_file(args.stable_file, "STABLE_")
    variables.add_file(args.volatile_file)

    h = variables.get(args.commit_hash_name.strip())

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