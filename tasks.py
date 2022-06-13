import invoke


@invoke.task
def sort(ctx, path=".", check=False):
    """Sort module imports."""
    print("  sorting imports ...")
    args = ["isort", path, "--profile", "black"]
    if check:
        args.append("--check-only")
    ctx.run(" ".join(args))


@invoke.task
def fmt(ctx, path=".", sort_=True, check=False):
    """Run code formatter."""
    print("  formatting ...")

    args = ["black", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))
    if sort_:
        sort(ctx, path, check)


@invoke.task
def lint(ctx, path="kv_store"):
    ctx.run(f"pylint {path}")


@invoke.task
def api(ctx, dev=True):
    cmds = ["uvicorn kv_store.api.main:app"]
    if dev:
        cmds.append("--reload")
    ctx.run(" ".join(cmds))


@invoke.task
def gen_reqs(ctx):
    print("  generating requirements.txt ...")
    cmds = [
        "poetry",
        "export",
        "-f",
        "requirements.txt",
        "--without-hashes",
        "--output",
        "requirements.txt",
    ]
    ctx.run(" ".join(cmds))
