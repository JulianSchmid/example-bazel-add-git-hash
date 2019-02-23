import argparse, sys, os

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
    parser.add_argument('commit_status_file', 
                         help='file containing the current commit hash')
    
    args = parser.parse_args()

    h = None
    with open(args.commit_status_file, "r") as f:
        h = f.read()
    
    print("Generating {}".format(args.header))
    with open(args.header, "w") as f:
        f.write("""
#pragma once

struct VersionInfo {{
    static char git_hash[{0}];
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
""".format(
                len(h),
                hash_array,
                args.header
            )
        )

if __name__ == "__main__":
    main()