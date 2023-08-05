# ez2bruteforce
**ez2bruteforce** is a python package that allows you to bruteforce the POW(proof of the work) stage in CTF game.
You can specify the char table, bruteforce length and the position and then use bruteforce to crack its hash digtest.   
[![codecov](https://codecov.io/gh/syheliel/ez2bruteforce/branch/main/graph/badge.svg?token=CD20F10MRO)](https://codecov.io/gh/syheliel/ez2bruteforce)

## Example
If you have known the hash of the digtest, like this:
```python
import hashlib
cipher = hashlib.sha1("Dear XXX:")
# cipher = b"\xf0\x1d\xb9\xe9|Xh\x84\xdb\r\xb0'\xa7\x80\xdc\x07\xbc\xca_`"
```

Then you can use ez2bruteforce to crack it:

```python
from ez2bruteforce.problem import BfItem,Problem
from ez2bruteforce.solver import sha1_solver
import string
problem = Problem(["Dear ",BfItem(),":"])
sha1_solver()
```