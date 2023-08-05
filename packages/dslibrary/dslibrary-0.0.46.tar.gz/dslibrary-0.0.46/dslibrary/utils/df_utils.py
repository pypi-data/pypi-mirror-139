import typing
import inspect


class LoadStrategy(object):
    """
    A description of how to load a dataframe.
    """
    def __init__(self, format: str=None, read_args: dict=None, use_dask: bool=False, read_method: typing.Callable=None,
                 uri: str=None, open_args: dict=None, opener: typing.Callable=None,
                 predefined=None, sql: str=None):
        """
        :param format:      File format, as a file extension, i.e. "csv", etc.
        :param read_args:   Arguments to send to the detected read_method.
        :param use_dask:    True to use dask and not pandas.
        :param read_method: Detected method, like pandas.read_csv(), etc.
        :param uri:         URL to open with opener()
        :param open_args:   Arguments to send to the detected opener() method.
        :param opener:      Method that opens a stream to read this data.
        :param predefined:  Predefined DataFrame to use instead of anything else.
        :param sql:         SQL, if data is coming from a database.
        """
        self.format = format
        self.read_args = read_args
        self.use_dask = use_dask
        self.read_method = read_method
        self.uri = uri
        self.open_args = open_args
        self.opener = opener
        self.predefined = predefined
        self.sql = sql

    @staticmethod
    def method_name(method: typing.Callable):
        """
        Work out package name and method name.

        :returns:  A tuple with
                0) name of module to import, or None
                1) qualified name of method to use
        """
        if not method:
            return None, None
        method_name = method.__name__
        module = method.__module__ if hasattr(method, "__module__") else None
        if module in ("pandas", "pandas.io.parsers.readers"):
            return "pandas", "pandas." + method_name
        if module == "dslibrary" or module.startswith("dslibrary."):
            return "dslibrary", "dslibrary." + method_name
        if module == "io" and method_name == "open":
            return None, "open"
        if module.startswith("dask.dataframe"):
            return "dask.dataframe", "dask.dataframe." + method_name
        return module, module + "." + method_name

    def _reader_supports_filename(self):
        """
        Some read functions (i.e. pandas.read_csv()) accept a filename.
        """
        reader_module = self.read_method.__module__ if hasattr(self.read_method, "__module__") else None
        if reader_module == "pandas" or reader_module.startswith("pandas"):
            return True
        if reader_module.startswith("dask."):
            return True
        return False

    def _reader_requires_filename(self):
        """
        Some read functions (i.e. dask.dataframe.read_csv()) require a filename and do not work with streams.
        """
        reader_module = self.read_method.__module__ if hasattr(self.read_method, "__module__") else None
        if reader_module.startswith("dask."):
            return True
        return False

    def _opener_can_be_simplified_to_filename(self):
        """
        Some combinations of 'opener' and 'open_args' translate into "just open this file".
        """
        if not self.opener:
            return True
        method_name = self.opener.__name__
        module = self.opener.__module__ if hasattr(self.opener, "__module__") else None
        if (module == "dslibrary" or module.startswith("dslibrary.")) and method_name == "open_resource":
            unrecognized_options = set(self.open_args or []) - {"storage_options"}
            if not unrecognized_options:
                return True
        if module == "io" and method_name == "open":
            return True

    def _can_skip_opener(self):
        """
        Code like 'pandas.read_csv(open('file.csv')) can be simplified, because pandas.read_csv() accepts a filename.
        This simplification is important when using bodo's JIT compiler.
        """
        if self._reader_supports_filename() and self._opener_can_be_simplified_to_filename():
            return True

    @staticmethod
    def repr_kwargs(kwargs: dict, comma_before: bool=True):
        out = ", ".join(f"{k}={repr(v)}" for k, v in (kwargs or {}).items())
        if comma_before and out:
            out = ", " + out
        return out

    def to_pandas_code(self, result_var: str="data") -> str:
        """
        Convert the strategy into Python code that uses pandas to load the dataframe.
        """
        code = ""
        if self.predefined:
            code += "import pandas\n"
            # TODO sort out arguments to to_json()
            code += f"{result_var} = pandas.DataFrame({repr(self.predefined.to_json())})\n"
        elif self.sql:
            mod_o, method_o = self.method_name(self.opener)
            if mod_o:
                code += f"import {mod_o}\n"
            connect_code = f"{method_o}({self.repr_kwargs(self.open_args, comma_before=False)})"
            # TODO: here, 'read_method' is assumed to be a self-contained local utility method - some kind of verification should happen
            code += inspect.getsource(self.read_method) + "\n"
            code += f"{result_var} = {self.read_method.__name__}({connect_code})\n"
        else:
            read_args = self.read_args
            mod_o, method_o = self.method_name(self.opener)
            if self._can_skip_opener():
                # don't use opener
                mod_o, method_o = None, None
                # merge open args to read args (i.e. storage_options for s3)
                read_args = dict(read_args or {})
                read_args.update(self.open_args or {})
            mod_r, method_r = self.method_name(self.read_method)
            if mod_o:
                code += f"import {mod_o}\n"
            if mod_r:
                code += f"import {mod_r}\n"
            if method_o:
                if self._reader_requires_filename():
                    raise ValueError(f"The method {method_r}() requires a filename, and it was not possible to simplify the supplied arguments to a filename")
                code_open = f"{method_o}({repr(self.uri)}{self.repr_kwargs(self.open_args)})"
            else:
                code_open = repr(self.uri)
            code += f"{result_var} = {method_r}({code_open}{self.repr_kwargs(read_args)})\n"
        return code


class CloseAfterIteration(object):
    """
    Wrapper for a pandas DataFrame iterator (i.e. read_csv(chunksize=...)), which makes sure an associated file stream
    gets closed.
    """
    def __init__(self, stream, iterator):
        self.stream = stream
        self.iterator = iterator
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.close()
            raise

    def close(self):
        if not self.closed:
            self.stream.close()
            self.closed = True

    def tell(self):
        if not hasattr(self.stream, "tell"):
            return
        return self.stream.tell()

    def get_chunk(self, size=None):
        try:
            if hasattr(self.iterator, "get_chunk"):
                return self.iterator.get_chunk(size)
        except StopIteration:
            self.close()
            raise


def load_dataframe_from_sql(db_conn, sql: str, use_dask: int=0):
    """
    Given a database connection, load a dataframe.

    NOTE: this method must be self-contained (i.e. include all its own imports) so that it can be sent elsewhere
    for execution.
    """
    try:
        import pandas
        c = db_conn.cursor()
        c.execute(sql)
        col_names = [col[0] for col in c.description]
        df = pandas.DataFrame(data=c, columns=col_names)
        # TODO here we are, dutifully moving a too-big dataframe to dask, is it worth it?
        if use_dask:
            import dask.dataframe
            mem_size = df.memory_usage().sum()
            if mem_size > use_dask:
                partition_size = max(use_dask, 40000000)
                df = dask.dataframe.from_pandas(df, npartitions=min(mem_size // partition_size, 2))
        return df
    finally:
        db_conn.close()
