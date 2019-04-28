"""
Executes a python script that gets the volatile & stable workspace status
files as an input.

The result is a C++ header & source file containing the git hash & git dirty flag.
"""

def _impl(ctx):
    # The list of arguments we pass to the script.
    # volatile status file: ctx.version_file
    # stable status file: ctx.info_file
    args = ["--header", ctx.outputs.header.path] + ["--source", ctx.outputs.cpp.path] + ["--volatile_file", ctx.version_file.path, "--stable_file", ctx.info_file.path, "--commit_hash_name", ctx.attr.commit_variable_name, "--workspace_dirty_name", ctx.attr.dirty_variable_name]

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
)