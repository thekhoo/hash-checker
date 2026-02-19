import hashlib

import pytest
from click.testing import CliRunner

from hashcheck.main import main, md5_hash


@pytest.fixture
def runner():
    return CliRunner()


# --- md5_hash ---

def test_md5_hash_returns_correct_digest(tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"hello world")
    expected = hashlib.md5(b"hello world").hexdigest()
    assert md5_hash(str(f)) == expected


def test_md5_hash_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_bytes(b"")
    expected = hashlib.md5(b"").hexdigest()
    assert md5_hash(str(f)) == expected


def test_md5_hash_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        md5_hash(str(tmp_path / "nonexistent.txt"))


# --- hashcheck <filepath> ---

def test_main_prints_hash(runner, tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"hello world")
    expected = hashlib.md5(b"hello world").hexdigest()

    result = runner.invoke(main, [str(f)])

    assert result.exit_code == 0
    assert f"{expected}  {str(f)}" in result.output


def test_main_no_args_shows_error(runner):
    result = runner.invoke(main, [])
    assert result.exit_code != 0


def test_main_file_not_found(runner, tmp_path):
    result = runner.invoke(main, [str(tmp_path / "missing.txt")])
    assert result.exit_code == 1
    assert "file not found" in result.output


# --- hashcheck <file1> <file2> ... ---

def test_compare_matching_files(runner, tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_bytes(b"same content")
    f2.write_bytes(b"same content")

    result = runner.invoke(main, [str(f1), str(f2)])

    assert result.exit_code == 0
    assert "All files match." in result.output
    digest = hashlib.md5(b"same content").hexdigest()
    assert f"{digest}  {str(f1)}" in result.output
    assert f"{digest}  {str(f2)}" in result.output


def test_compare_different_files(runner, tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_bytes(b"content a")
    f2.write_bytes(b"content b")

    result = runner.invoke(main, [str(f1), str(f2)])

    assert result.exit_code == 1
    assert "do not match" in result.output
    assert hashlib.md5(b"content a").hexdigest() in result.output
    assert hashlib.md5(b"content b").hexdigest() in result.output


def test_compare_multiple_files_all_match(runner, tmp_path):
    files = []
    for name in ["a.txt", "b.txt", "c.txt"]:
        f = tmp_path / name
        f.write_bytes(b"identical")
        files.append(str(f))

    result = runner.invoke(main, files)

    assert result.exit_code == 0
    assert "All files match." in result.output
    digest = hashlib.md5(b"identical").hexdigest()
    for filepath in files:
        assert f"{digest}  {filepath}" in result.output


def test_compare_file_not_found(runner, tmp_path):
    f = tmp_path / "exists.txt"
    f.write_bytes(b"data")

    result = runner.invoke(main, [str(f), str(tmp_path / "missing.txt")])

    assert result.exit_code == 1
    assert "file not found" in result.output
