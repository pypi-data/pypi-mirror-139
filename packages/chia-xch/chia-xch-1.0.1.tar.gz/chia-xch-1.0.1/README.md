# chia-xch
A simple python package interacts with the chia node, python version >=3.6 is recommend
# Install
```
pip3 install chia-xch
```

# Groups
* [connect](#connect)


# connect 
```
from chia_xch.xch import Xch
from chia_xch.providers import *
fnp = FullNodeProvider()
fn = Xch.full_node(fnp)

wp = WalletProvider()
wa = Xch.wallet(wp)
```

# Tips
- The default parameters of these functions are not specified in the document, you need to check the source code by yourself.
- The current document is incomplete, I will gradually improve the document later.