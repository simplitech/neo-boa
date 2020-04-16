import abc
import os


class ICompiler(abc.ABC):
    @abc.abstractmethod
    def save(self, compiler, path, output_path=None):
        """
        Save the compiled neo vm bytecode and metadata files to the
        file system at the specified path.

        :param compiler: Object with the compile logic
        :param path: Path of the python file to be compiled
        :param output_path: Path of the file where the data will be stored
        """
        pass


class Neo2Compiler(ICompiler):
    def save(self, compiler, path, output_path=None):
        data = compiler.write()

        if output_path is None:
            fullpath = os.path.realpath(path)
            path, filename = os.path.split(fullpath)
            newfilename = filename.replace('.py', '.avm')
            output_path = '%s/%s' % (path, newfilename)

        compiler.write_file(data, output_path)
        compiler.entry_module.export_debug(output_path)
        compiler.entry_module.export_abi_json(output_path)

        return data


class Neo3Compiler(ICompiler):
    def save(self, compiler, path, output_path=None):
        # TODO: Include the extra info needed for the .nef file and the logic of the .manifest.json file
        # TODO: Include the .abi.json generation method when merged
        pass
