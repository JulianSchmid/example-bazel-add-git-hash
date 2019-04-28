# example-bazel-add-git-hash
Example for baking the current git commit hash into a bazel C++ project

## Running the example

The following command runs a C++ binary that prints the git commit hash present during its build.

```sh
bazel run //:print
```

## Files
|   |   |
|---|---|
| `.bazelrc` | Defines the command that is executed to determine the current workspace status (runs every time `bazel` is run). In the case of this example `python workspace_status.py` is defined as the command |
| `workspace_status.py` | Executes two git commands to determine the current commit hash & workspace status. These values are returned via the standard output. See https://docs.bazel.build/versions/master/user-manual.html#flag--workspace_status_command for an in detailed description of the output format. |
| bake_git_hash.bzl | Defines the codegenerator rule that adds the current the git hash & status to a C++ program. |
| gen_cpp.py | Code generator that takes the workspace status files as an input and outputs a C++ header and source files containing the git hash & status. |
| main.cpp | C++ program that prints the git hash present during its build. |
| BUILD | Defines the codegenerator instance as well as the program that prints the git hash that was present during the build. |
