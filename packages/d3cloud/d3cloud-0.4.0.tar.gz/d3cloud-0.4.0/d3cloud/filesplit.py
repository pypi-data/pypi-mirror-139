
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging, os, ntpath, csv, time


class Filesplit(object):

    def __init__(self):
        self.log = logging.getLogger(
            __name__).getChild(self.__class__.__name__)
        self.man_filename = u'fs_manifest.csv'
        self._buffer_size = 1000000

    def __process_split(self, fi, fo, split_size, carry_over, newline=False, output_encoding=None, include_header=False, header=None):
        """
        Process that splits the incoming stream
        :param fi: input file like object that implements read() and readline()
        method
        :param fo: file like object that implements write() method
        :param split_size: file split size in bytes
        :param newline: when True, splits at newline on top of bytes
        :param output_encoding: split file encoding
        :param include_header: when True, first line is treated as header and
        each split receives the header. This flag is dependant on newline flag
        to be set to True as well
        :param carry_over: any carry over bytes to the next file
        :param header: header from the file if any
        :return:
        """
        buffer_size = (split_size if (
            split_size < self._buffer_size) else self._buffer_size)
        buffer = 0
        if (not newline):
            while True:
                if carry_over:
                    fo.write(carry_over)
                    buffer += (len(carry_over) if (not output_encoding)
                               else len(carry_over.encode(output_encoding)))
                    carry_over = None
                    continue
                chunk = fi.read(buffer_size)
                if (not chunk):
                    break
                chunk_size = (len(chunk) if (not output_encoding)
                              else len(chunk.encode(output_encoding)))
                if ((buffer + chunk_size) <= split_size):
                    fo.write(chunk)
                    buffer += chunk_size
                else:
                    carry_over = chunk
                    break
            if (not carry_over):
                carry_over = None
            return (carry_over, buffer, None)
        else:
            if carry_over:
                if header:
                    fo.write(header)
                fo.write(carry_over)
                if header:
                    buffer += ((len(carry_over) + len(header)) if (not output_encoding) else (
                        len(carry_over.encode(output_encoding)) + len(header.encode(output_encoding))))
                else:
                    buffer += (len(carry_over) if (not output_encoding)
                               else len(carry_over.encode(output_encoding)))
                carry_over = None
            for line in fi:
                if (include_header and (not header)):
                    header = line
                line_size = (len(line) if (not output_encoding)
                             else len(line.encode(output_encoding)))
                if ((buffer + line_size) <= split_size):
                    fo.write(line)
                    buffer += line_size
                else:
                    carry_over = line
                    break
            if (not carry_over):
                carry_over = None
            return (carry_over, buffer, header)

    def split(self, file, split_size, output_dir=u'.', callback=None, **kwargs):
        """
        Splits the file into chunks based on the newline char in the file.
        By default uses binary mode.
        :param file: path to the source file
        :param split_size: file split size in bytes
        :param output_dir: output dir to write the split files
        :param callable callback: (Optional) callback function
        [func (str, long, long)] that accepts
        three arguments - full file path to the destination, size of the file
        in bytes and line count.
        """
        start_time = time.time()
        self.log.info(u'Starting file split process')
        newline = kwargs.get(u'newline', False)
        include_header = kwargs.get(u'include_header', False)
        if include_header:
            newline = True
        encoding = kwargs.get(u'encoding', None)
        split_file_encoding = kwargs.get(u'split_file_encoding', None)
        f = ntpath.split(file)[1]
        (filename, ext) = os.path.splitext(f)
        (fi, man) = (None, None)
        if (split_file_encoding and (not encoding)):
            raise ValueError(
                u'`encoding` needs to be specified when providing `split_file_encoding`')
        try:
            if (encoding and (not split_file_encoding)):
                fi = open(file, mode=u'r')
            elif (encoding and split_file_encoding):
                fi = open(file, mode=u'r')
            else:
                fi = open(file, mode=u'rb')
            man_file = os.path.join(output_dir, self.man_filename)
            man = open(man_file, mode=u'w+')
            man_writer = csv.DictWriter(
                f=man, fieldnames=[u'filename', u'filesize', u'encoding', u'header'])
            man_writer.writeheader()
            (split_counter, carry_over, header) = (1, u'', None)
            while (carry_over is not None):
                split_file = os.path.join(
                    output_dir, u'{0}_{1}{2}'.format(filename, split_counter, ext))
                fo = None
                try:
                    if (encoding and (not split_file_encoding)):
                        fo = open(split_file, mode=u'w+',
                                  encoding=encoding)
                    elif (encoding and split_file_encoding):
                        fo = open(split_file, mode=u'w+',
                                  encoding=split_file_encoding)
                    else:
                        fo = open(split_file, mode=u'wb+')
                    (carry_over, output_size, header) = self.__process_split(fi=fi, fo=fo, split_size=split_size, newline=newline,
                                                                             output_encoding=split_file_encoding, carry_over=carry_over, include_header=include_header, header=header)
                    if callback:
                        callback(split_file, output_size)
                    di = {
                        u'filename': ntpath.split(split_file)[1],
                        u'filesize': output_size,
                        u'encoding': encoding,
                        u'header': (True if header else None),
                    }
                    man_writer.writerow(di)
                    split_counter += 1
                finally:
                    if fo:
                        fo.close()
        finally:
            if fi:
                fi.close()
            if man:
                man.close()
        run_time = round(((time.time() - start_time) / 60))
        self.log.info(u''.join([u'Process complete']))
        self.log.info(u''.join([u'Run time(m): ', u'{}'.format(run_time)]))

    def merge(self, input_dir, output_file=None, manifest_file=None, callback=None, cleanup=False):
        """Merges the split files based off manifest file
        Args:
            input_dir (str): directory containing the split files and manifest
            file
            output_file (str): final merged output file path. If not provided,
            the final merged filename is derived from the split filename and
            placed in the same input dir
            callback (Callable): callback function
            [func (str, long)] that accepts 2 arguments - path to destination
            , size of the file in bytes
            cleanup (bool): if True, all the split files, manifest file will be
            deleted after merge leaving behind the merged file.
            manifest_file (str): path to the manifest file. If not provided,
            the process will look for the file within the input_dir
        Raises:
            FileNotFoundError: if missing manifest and split files
            NotADirectoryError: if input path is not a directory
        """
        start_time = time.time()
        self.log.info(u'Starting file merge process')
        if (not os.path.isdir(input_dir)):
            raise NotADirectoryError(
                u'Input directory is not a valid directory')
        manifest_file = (os.path.join(input_dir, self.man_filename)
                         if (not manifest_file) else manifest_file)
        if (not os.path.exists(manifest_file)):
            raise FileNotFoundError(u'Unable to locate manifest file')
        fo = None
        clear_output_file = True
        header_set = False
        try:
            with open(manifest_file, mode=u'r') as man_fh:
                man_reader = csv.DictReader(f=man_fh)
                for line in man_reader:
                    encoding = line.get(u'encoding', None)
                    header_avail = line.get(u'header', None)
                    if (not output_file):
                        (f, ext) = ntpath.splitext(line.get(u'filename'))
                        output_filename = u''.join([f.rsplit(u'_', 1)[0], ext])
                        output_file = os.path.join(input_dir, output_filename)
                    if clear_output_file:
                        if os.path.exists(output_file):
                            os.remove(output_file)
                        clear_output_file = False
                    if (not fo):
                        if encoding:
                            fo = open(output_file, mode=u'a',
                                      encoding=encoding)
                        else:
                            fo = open(output_file, mode=u'ab')
                    try:
                        input_file = os.path.join(
                            input_dir, line.get(u'filename'))
                        if encoding:
                            fi = open(input_file, mode=u'r',
                                      encoding=encoding)
                        else:
                            fi = open(input_file, mode=u'rb')
                        if header_set:
                            next(fi)
                        for line in fi:
                            if (header_avail and (not header_set)):
                                header_set = True
                            fo.write(line)
                    finally:
                        if fi:
                            fi.close()
        finally:
            if fo:
                fo.close()
        if cleanup:
            with open(manifest_file, mode=u'r') as man_fh:
                man_reader = csv.DictReader(f=man_fh)
                for line in man_reader:
                    f = os.path.join(input_dir, line.get(u'filename'))
                    if os.path.exists(f):
                        os.remove(f)
            if os.path.exists(manifest_file):
                os.remove(manifest_file)
        if callback:
            callback(output_file, os.stat(output_file).st_size)
        run_time = round(((time.time() - start_time) / 60))
        self.log.info(u''.join([u'Process complete']))
        self.log.info(u''.join([u'Run time(m): ', u'{}'.format(run_time)]))