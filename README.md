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

## Releasing

Releases are published to PyPI automatically by the CI workflow when a version tag is pushed.

**1. Bump the version in `pyproject.toml`**

```toml
[project]
version = "0.2.0"
```

**2. Commit the version bump**

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
```

**3. Tag and push**

```bash
git tag v0.2.0
git push origin main --tags
```

The `publish` job in CI will build the package and upload it to PyPI once all tests pass.

> **First-time setup:** PyPI Trusted Publishing must be configured before the first release.
> Go to your PyPI project → *Manage* → *Publishing* and add a trusted publisher:
> - Publisher: GitHub
> - Repository: `<owner>/hash-checker`
> - Workflow: `ci.yml`
> - Environment: `pypi`
