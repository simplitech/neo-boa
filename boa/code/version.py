from boa.code.compiler import Neo2Compiler, Neo3Compiler
from boa.code.converter import Neo2Converter, Neo3Converter


class Version:
    converter = None
    compiler = None
    __version = None

    @staticmethod
    def init(version):
        if version is None:
            raise Exception('Incompatible neo version: ' % version)

        if version.startswith('2.'):
            _init_neo2()
        elif version.startswith('3.'):
            _init_neo3()

        Version.__version = version


def _init_neo2():
    Version.converter = Neo2Converter()
    Version.compiler = Neo2Compiler()


def _init_neo3():
    Version.converter = Neo3Converter()
    Version.compiler = Neo3Compiler()
