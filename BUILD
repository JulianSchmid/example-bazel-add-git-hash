load(":bake_git_hash.bzl", "git_hash_cpp")

py_binary(
    name = "gen_cpp",
    srcs = ["gen_cpp.py"]
)

git_hash_cpp(
    name = "foo",
    git_status_commit = ".git_status/commit_hash",
    git_workspace_dirty = ".git_status/workspace_dirty",
    header = "b.h",
    cpp = "b.cpp"
)

cc_library(
    name = "somelip",
    hdrs = [":b.h"],
    srcs = [":b.cpp"],
)

cc_binary(
    name = "print",
    srcs = [
        "main.cpp"
    ],
    deps = [":somelip"]
)