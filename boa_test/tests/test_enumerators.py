from boa_test.tests.boa_test import BoaTest
from boa.compiler import Compiler
from neo.Settings import settings

settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'
settings.log_smart_contract_events = True

from neo.Prompt.Commands.BuildNRun import TestBuild


class TestContract(BoaTest):

    def test_storage_find(self):

        output = Compiler.instance().load('%s/boa_test/example/demo/EnumeratorTest.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, [1], self.GetWallet1(), '02', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, [2], self.GetWallet1(), '02', '01')
        self.assertEqual(len(results), 1)
        res = [i.GetBigInteger() for i in results[0].GetArray()]
        self.assertEqual(res, [1, 2, 3, 5, 9, 14])

        tx, results, total_ops, engine = TestBuild(out, [3], self.GetWallet1(), '02', '01')
        self.assertEqual(len(results), 1)
        res = [i.GetBigInteger() for i in results[0].GetArray()]
        self.assertEqual(res, [1, 2, 3, 5, 9, 14])

        tx, results, total_ops, engine = TestBuild(out, [4], self.GetWallet1(), '02', '01')
        self.assertEqual(len(results), 1)
        res = [i.GetString() for i in results[0].GetArray()]
        self.assertEqual(res, ['1', '2', '3', '5', '9', '14', 'a', 'b', 'd', 'f'])

        tx, results, total_ops, engine = TestBuild(out, [5], self.GetWallet1(), '02', '01')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 6)
