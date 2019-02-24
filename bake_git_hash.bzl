"""Execute a binary.
The example below executes the binary target "//actions_run:merge" with
some arguments. The binary will be automatically built by Bazel.
The rule must declare its dependencies. To do that, we pass the target to
the attribute "_merge_tool". Since it starts with an underscore, it is private
and users cannot redefine it.
"""

def _impl(ctx):
    # The list of arguments we pass to the script.
    # volatile status file: ctx.version_file
    # stable status file: ctx.info_file
    print(ctx.attr.commit_variable_name)
    print(ctx.attr.dirty_variable_name)
    args = ["--header", ctx.outputs.header.path] + ["--source", ctx.outputs.cpp.path] + ["--volatile_file", ctx.version_file.path, "--stable_file", ctx.info_file.path, "--commit_hash_name", "GIT_COMMIT_HASH", "--workspace_dirty_name", ""]

    # Action to call the script.
    ctx.actions.run(
        inputs = [ctx.version_file, ctx.info_file],
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
        "commit_variable_name": attr.string(mandatory=True),
        "dirty_variable_name": attr.string(mandatory=True),
        "header": attr.output(mandatory = True),
        "cpp": attr.output(mandatory = True)
    },
    #output_to_genfiles = True,
)