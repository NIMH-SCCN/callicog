import json

import pytest
import numpy as np

from marmobox_listener import NumpyFloat32Encoder


class FloatEncoderTest(json.JSONEncoder):
    ''' Duplicate logic of NumpyFloat32Encoder but use native float, to confirm
    logic/structure of encoder is correct
    '''
    def default(self, obj):
        if isinstance(obj, float):
            return float(obj)
        return json.JSONEncoder.default(obj)


def test_float32():
    native_float = 2/3
    data = dict(flt=native_float, msg='hello')
    json_str = json.dumps(data)
    json_bytes = bytes(json_str, 'utf8')
    json_dict = json.loads(json_bytes.decode())
    assert json_dict
    assert json_dict['flt'] == native_float

    json_str = json.dumps(data, cls=FloatEncoderTest)
    json_bytes = bytes(json_str, 'utf8')
    json_dict = json.loads(json_bytes.decode())
    assert json_dict
    assert json_dict['flt'] == native_float

    np_float = np.float32(2/3)
    data = dict(flt=np_float, msg='hello')
    json_str = json.dumps(data, cls=NumpyFloat32Encoder)
    json_bytes = bytes(json_str, 'utf8')
    json_dict = json.loads(json_bytes.decode())
    assert json_dict
    assert json_dict['flt'] == np_float
    # print(np_float)

    np_float = np.float32(float('nan'))
    data = dict(flt=np_float, msg='hello')
    json_str = json.dumps(data, cls=NumpyFloat32Encoder)
    json_bytes = bytes(json_str, 'utf8')
    json_dict = json.loads(json_bytes.decode())
    assert json_dict
    assert str(json_dict['flt']) == 'nan'
    print(json_dict)


def test_json_exception_handling():
    bad_json = '{"msg": "boo"'
    with pytest.raises(json.JSONDecodeError) as exc_info:
        json.loads(bad_json)
    try:
        json.loads(bad_json)
    except json.JSONDecodeError as exc:
        assert exc
