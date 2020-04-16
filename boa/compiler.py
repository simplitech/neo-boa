import os
from boa.code.module import Module


class Compiler(object):
    """
    The main compiler interface class.

    The following loads a python file, compiles it to the `.avm` format
    and saves it alongside the python file.

    .. code-block:: python

        from boa.compiler import Compiler
        Compiler.load_and_save('path/to/your/file.py')

        # return the compiler object for inspection
        compiler = Compiler.load('path/to/your/file.py')

        # retrieve the default module for inpection
        default_module = compiler.default

        # retreive the default/entry method for the smart contract
        entry_method = default_module.main
    """

    __instance = None

    entry_module = None

    nep8 = True

    @staticmethod
    def instance():
        """
        Retrieve the current instance of the Compiler object, if it exists,
        or create one.

        :return: the singleton instance of the Compiler object
        """

        if not Compiler.__instance:
            Compiler.__instance = Compiler()
        return Compiler.__instance

    @property
    def default(self):
        """
        Retrieve the default or 'entry' module.

        :return: the default `boa.code.Module` object or None upon exception
        """
        return self.entry_module

    def write_file(self, data, path):
        """
        Save the output data to the file system at the specified path.

        :param data: a byte string of data to write to disk
        :param path: the path to write the file to
        """

        with open(path, 'wb+') as out_file:
            out_file.write(data)

    def write(self):
        """
        Write the default module to a byte string.

        :return: the compiled Python program as a byte string
        :rtype: bytes
        """

        out_bytes = bytes(self.entry_module.write())
        return out_bytes

    @staticmethod
    def load_and_save(path, output_path=None, use_nep8=True, neo_version='2.9.0'):
        """
        Call `load_and_save` to load a Python file to be compiled to the .avm format and save the result.
        By default, the resultant .avm file is saved along side the source file.

        :param path: The path of the Python file to compile
        :param output_path: Optional path to save the compiled `.avm` file
        :return: the instance of the compiler

        The following returns the compiler object for inspection

        .. code-block:: python

            from boa.compiler import Compiler

            Compiler.load_and_save('path/to/your/file.py')
        """

        compiler = Compiler.load(os.path.abspath(path), use_nep8=use_nep8, neo_version=neo_version)
        from boa.code.version import Version
        data = Version.compiler.save(compiler, path, output_path=output_path)

        return data

    @staticmethod
    def load(path, use_nep8=True, neo_version='2.9.0'):
        """
        Call `load` to load a Python file to be compiled but not to write to .avm

        :param path: the path of the Python file to compile
        :return: The instance of the compiler

        The following returns the compiler object for inspection.

        .. code-block:: python

            from boa.compiler import Compiler

            compiler = Compiler.load('path/to/your/file.py')
        """

        Compiler.__instance = None
        compiler = Compiler.instance()

        from boa.code.version import Version
        Version.init(neo_version)

        compiler.nep8 = use_nep8
        compiler.entry_module = Module(path)

        return compiler
