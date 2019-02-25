load(":bake_git_hash.bzl", "git_hash_cpp")

py_binary(
    name = "gen_cpp",
    srcs = ["gen_cpp.py"]
)

git_hash_cpp(
    name = "foo",
    commit_variable_name = "GIT_COMMIT_HASH",
    dirty_variable_name = "GIT_DIRTY",
    header = "a/c/b.h",
    cpp = "a/c/b.cpp"
)

cc_library(
    name = "somelib",
    hdrs = [":a/c/b.h"],
    srcs = [":a/c/b.cpp"],
)

cc_binary(
    name = "print",
    srcs = [
        "main.cpp"
    ],
    deps = [":somelib"]
)