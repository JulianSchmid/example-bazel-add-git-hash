"""Execute a binary.
The example below executes the binary target "//actions_run:merge" with
some arguments. The binary will be automatically built by Bazel.
The rule must declare its dependencies. To do that, we pass the target to
the attribute "_merge_tool". Since it starts with an underscore, it is private
and users cannot redefine it.
"""

def _impl(ctx):
    # The list of arguments we pass to the script.
    args = ["--header", ctx.outputs.header.path] + ["--source", ctx.outputs.cpp.path] + [ctx.file.git_status_commit.path, ctx.file.git_workspace_dirty.path]

    # Action to call the script.
    ctx.actions.run(
        inputs = [ctx.file.git_status_commit, ctx.file.git_workspace_dirty],
        outputs = [ctx.outputs.header, ctx.outputs.cpp],
        arguments = args,
        progress_message = "Adding Git Hash to %s" % ctx.outputs.header.short_path,
        executable = ctx.executable._gen_cpp_tool,
    )

git_hash_cpp = rule(
    implementation = _impl,
    attrs = {
        "_gen_cpp_tool": attr.label(
            executable = True,
            cfg = "host",
            allow_files = True,
            default = Label("//:gen_cpp"),
        ),
        "git_status_commit": attr.label(
            allow_single_file = True,
        ),
        "git_workspace_dirty": attr.label(
            allow_single_file = True,
        ),
        "header": attr.output(mandatory = True),
        "cpp": attr.output(mandatory = True)
    },
    #outputs = {
    #    "a.h": "a.h",
    #    "a.cpp": "a.cpp",
    #},
    #output_to_genfiles = True,
)