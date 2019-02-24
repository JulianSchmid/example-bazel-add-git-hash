load(":bake_git_hash.bzl", "git_hash_cpp")

py_binary(
    name = "gen_cpp",
    srcs = ["gen_cpp.py"]
)

git_hash_cpp(
    name = "foo",
    header = "b.h",
    cpp = "b.cpp"
)

cc_library(
    name = "somelib",
    hdrs = [":b.h"],
    srcs = [":b.cpp"],
)

cc_binary(
    name = "print",
    srcs = [
        "main.cpp"
    ],
    deps = [":somelib"]
)