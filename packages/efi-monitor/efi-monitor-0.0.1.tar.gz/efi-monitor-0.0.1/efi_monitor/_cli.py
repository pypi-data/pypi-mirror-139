"""Define the command line iterface."""
import os
import glob


def _file_path():
    """Determine the file path."""
    return os.environ.get("EFI_MONITOR_FILE_PATH", "/sys/firmware/efi/efivars/dump*")


def _files():
    """Find the dump_files."""
    return glob.glob(_file_path())


def check():
    """Check for efi dump files."""
    for a_file in _files():
        print(a_file)


def clear():
    """Clear out efi dump files."""
    for a_file in _files():
        os.unlink(a_file)
