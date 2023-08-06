# filecoin-lotus
A simple python package interacts with the filecoin lotus node, python version >=3.6 is recommend
# Install
```
pip3 install filecoin-lotus
```

# Groups
* [connect](#connect)


# connect 
```
from filecoin_lotus.filecoin import FileCoin
fc = FileCoin(FileCoin.HttpProvider())
```

# Tips
- The default parameters of these functions are not specified in the document, you need to check the source code by yourself.
- The current document is incomplete, I will gradually improve the document later.