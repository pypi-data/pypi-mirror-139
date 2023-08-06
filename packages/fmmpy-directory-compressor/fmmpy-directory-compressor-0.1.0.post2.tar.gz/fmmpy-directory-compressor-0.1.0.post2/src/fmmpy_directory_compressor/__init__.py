from sys import platform
if platform == "linux" or platform == "linux2":
    from .unix.fmmpy_directory_compressor import compress_directory, decompress_directory
elif platform == "win32":
    from .win32.fmmpy_directory_compressor import compress_directory, decompress_directory
else:
    raise OSError("The operating system you are using is currently not supported!")