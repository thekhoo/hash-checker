# hash-checker

A CLI tool for computing and comparing MD5 checksums.

## Installation

```bash
uv tool install .
```

## Usage

### Get the MD5 hash of a file

```bash
checksum <filepath>
```

```
$ checksum photo.jpg
d8e8fca2dc0f896fd7cb4cb0031ba249
```

### Compare files

```bash
checksum compare <file1> <file2> [file3 ...]
```

Returns a success message if all files are identical, or lists each file's hash and exits with a non-zero status if they differ.

```
$ checksum compare file_a.zip file_b.zip
All files match.

$ checksum compare original.zip modified.zip
Files do not match:
  d8e8fca2dc0f896fd7cb4cb0031ba249  original.zip
  aabbcc112233445566778899aabbcc11  modified.zip
```
