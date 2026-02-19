import hashlib
import sys

import cloup


def md5_hash(filepath: str) -> str:
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


@cloup.command()
@cloup.argument("files", nargs=-1, required=True)
def main(files: tuple[str, ...]) -> None:
    """Get the MD5 hash of one or more files. Compares hashes when multiple files are given."""
    hashes: dict[str, str] = {}
    for filepath in files:
        try:
            digest = md5_hash(filepath)
            hashes[filepath] = digest
            print(f"{digest}  {filepath}")
        except FileNotFoundError:
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: permission denied: {filepath}", file=sys.stderr)
            sys.exit(1)

    if len(files) > 1:
        unique_hashes = set(hashes.values())
        if len(unique_hashes) == 1:
            print("All files match.")
        else:
            print("Files do not match.", file=sys.stderr)
            sys.exit(1)
