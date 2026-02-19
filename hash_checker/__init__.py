import hashlib
import sys

import cloup


def md5_hash(filepath: str) -> str:
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


@cloup.group(invoke_without_command=True)
@cloup.argument("filepath", required=False)
@cloup.pass_context
def main(ctx: cloup.Context, filepath: str | None) -> None:
    """Get the MD5 hash of a file."""
    if ctx.invoked_subcommand is not None:
        return
    if filepath is None:
        print(ctx.get_help())
        return
    try:
        print(md5_hash(filepath))
    except FileNotFoundError:
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {filepath}", file=sys.stderr)
        sys.exit(1)


@main.command()
@cloup.argument("files", nargs=-1, required=True)
def compare(files: tuple[str, ...]) -> None:
    """Compare MD5 hashes of two or more files."""
    hashes: dict[str, str] = {}
    for filepath in files:
        try:
            hashes[filepath] = md5_hash(filepath)
        except FileNotFoundError:
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: permission denied: {filepath}", file=sys.stderr)
            sys.exit(1)

    unique_hashes = set(hashes.values())
    if len(unique_hashes) == 1:
        print("All files match.")
    else:
        print("Files do not match:", file=sys.stderr)
        for filepath, digest in hashes.items():
            print(f"  {digest}  {filepath}", file=sys.stderr)
        sys.exit(1)
