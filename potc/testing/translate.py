import copy
import io
from contextlib import contextmanager
from typing import Mapping, Any

from ..translate import translate_object


def run_script(source: str) -> Mapping[str, Any]:
    vs = {}
    exec('', vs)
    original_vs = copy.deepcopy(vs)
    exec(source, vs)

    return {
        key: value for key, value in vs.items() if
        key not in original_vs.keys() or original_vs[key] is not vs[key]
    }


_TEST_OBJ = '_TEST_OBJ'


@contextmanager
def obj_translate_assert(obj, extend_rules=None):
    _code, _addon, _name = translate_object(obj, extend_rules)

    with io.StringIO() as _source_file:
        for _import in sorted(set(_addon.import_items), key=lambda x: x.key):
            print(_import, file=_source_file)

        print(f'{_TEST_OBJ} = {_code}', file=_source_file)
        _source_code = _source_file.getvalue()

    _changes = run_script(_source_code)
    _obj = _changes[_TEST_OBJ]

    yield _obj, _name
