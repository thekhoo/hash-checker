# hash-checker

A CLI tool for computing and comparing MD5 hashchecks.

## Installation

```bash
uv tool install .
```

## Usage

### Get the MD5 hash of a file

```bash
hashcheck <filepath>
```

```
$ hashcheck photo.jpg
d8e8fca2dc0f896fd7cb4cb0031ba249  photo.jpg
```

### Compare files

Pass two or more files — hashes are always printed, and the exit code indicates whether they match.

```bash
hashcheck <file1> <file2> [file3 ...]
```

```
$ hashcheck file_a.zip file_b.zip
d8e8fca2dc0f896fd7cb4cb0031ba249  file_a.zip
d8e8fca2dc0f896fd7cb4cb0031ba249  file_b.zip
All files match.

$ hashcheck original.zip modified.zip
d8e8fca2dc0f896fd7cb4cb0031ba249  original.zip
aabbcc112233445566778899aabbcc11  modified.zip
Files do not match.
```

## Contributing

### Setup

```bash
uv sync
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

These commands install two git hooks:
- **pre-commit** — runs [pyrefly](https://pyrefly.org/) type checking before each commit
- **commit-msg** — enforces [Conventional Commits](https://www.conventionalcommits.org/) format; commits that don't conform are rejected

If you're using VS Code, both hooks and `uv sync` are installed automatically when you open the workspace.

### Commit message format

```
<type>: <description>

# Examples
feat: add SHA-256 support
fix: handle symlinks correctly
docs: update usage examples
```

| Type | Release triggered |
|------|-------------------|
| `feat:` | minor (`0.1.x` → `0.2.0`) |
| `fix:`, `perf:`, `refactor:` | patch (`0.1.3` → `0.1.4`) |
| `feat!:` or `BREAKING CHANGE:` footer | major (`0.x.x` → `1.0.0`) |
| `chore:`, `docs:`, `test:` | none |

## Releasing

Releases are fully automated. On every merge to `main`:

1. The release workflow reads commits since the last tag and determines the next version.
2. `pyproject.toml` is updated and a `vX.Y.Z` tag is pushed.
3. The publish workflow triggers on the tag, builds the package, and uploads it to PyPI.

No manual version bumping or tagging is needed.

> **First-time setup:** PyPI Trusted Publishing must be configured before the first release.
> Go to your PyPI project → *Manage* → *Publishing* and add a trusted publisher:
> - Publisher: GitHub
> - Repository: `<owner>/hash-checker`
> - Workflow: `ci.yml`
> - Environment: `pypi`
