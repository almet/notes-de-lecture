import os
import shutil


def copy(source, destination):
    """Recursively copy source into destination.
    Taken from pelican.
    If source is a file, destination has to be a file as well.
    The function is able to copy either files or directories.
    :param source: the source file or directory
    :param destination: the destination file or directory
    """
    source_ = os.path.abspath(os.path.expanduser(source))
    destination_ = os.path.abspath(os.path.expanduser(destination))
    
    if os.path.isfile(source_):
        dst_dir = os.path.dirname(destination_)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy2(source_, destination_)

    elif os.path.isdir(source_):
        if not os.path.exists(destination_):
            os.makedirs(destination_)
        if not os.path.isdir(destination_):
            return

        for src_dir, subdirs, others in os.walk(source_):
            dst_dir = os.path.join(destination_,
                                   os.path.relpath(src_dir, source_))

            if not os.path.isdir(dst_dir):
                # Parent directories are known to exist, so 'mkdir' suffices.
                os.mkdir(dst_dir)

            for o in others:
                src_path = os.path.join(src_dir, o)
                dst_path = os.path.join(dst_dir, o)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dst_path)