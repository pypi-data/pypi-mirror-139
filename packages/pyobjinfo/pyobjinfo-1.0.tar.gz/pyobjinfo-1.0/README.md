## PyObjInfo

This package is intended to learn how python stores big integers in memory


### Install

    pip install pyobjinfo


### Examples

Get object info

```py
from pprint import pprint
import pyobjinfo

pprint(
    pyobjinfo.inspect(1234567890)
)
```

Expected output

> {'ob_base': {'ob_base': {'ob_refcnt': 4, 'ob_type': 'int'}},
> 'ob_digit': [160826066, 1],
> 'ob_size': 2}


Get object's `ob_digit` items separatelly

```py
import pyobjinfo

print(
    pyobjinfo.get_parts(1234567890)
)
```

Expected output

> [160826066, 1]