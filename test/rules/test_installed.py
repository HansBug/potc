import pytest

import test
from potc.testing import transobj_assert, mock_potc_plugins
from ..conftest import with_pythonpath


@pytest.fixture()
def potc_dict_installed():
    with with_pythonpath('plugins/dict'):
        with mock_potc_plugins('potc_dict.plugin'):
            yield


@pytest.fixture()
def potc_invalid_plugin_1_installed():
    with mock_potc_plugins(test):  # module without __rules__
        yield


@pytest.fixture()
def potc_invalid_plugin_2_installed():
    with mock_potc_plugins(233):  # invalid type
        yield


@pytest.mark.unittest
class TestRulesInstalled:
    @classmethod
    def __with_pkg(cls, pkgs):
        pass

    def test_without_potc_dict(self):
        with transobj_assert({'a': 1, 'b': 2}) as (obj, name):
            assert obj == {'a': 1, 'b': 2}
            assert name == 'builtin_dict'

    def test_potc_dict_installed(self, potc_dict_installed):
        with transobj_assert({'a': 1, 'b': 2}) as (obj, name):
            assert obj == {'a': 1, 'b': 2}
            assert name == 'pretty_dict'

    def test_potc_invalid_plugin_1(self, potc_invalid_plugin_1_installed):
        with pytest.raises(ImportError):
            with transobj_assert({'a': 1, 'b': 2}) as (obj, name):
                pytest.fail('Should not reach here.')

    def test_potc_invalid_plugin_2(self, potc_invalid_plugin_2_installed):
        with pytest.raises(TypeError):
            with transobj_assert({'a': 1, 'b': 2}) as (obj, name):
                pytest.fail('Should not reach here.')