
```bash
export LD_LIBRARY_PATH=./build
ipython
```

```python
from go_cool import fff, random_string, replace, f2str, str2f, map_test
import random
import string

%%timeit
str2f("12.3456789")
f2str(12.3456789)
go_cool.random_string(1_000).replace("a","b")
"".join(random.choices(string.ascii_lowercase, k=1_000)).replace("a","b")

myFunc(199,"12"*1_000_000)
```


# TODO
 - [] warn the use if it uses string or other dynamicly allocated types as result
 - [] unexported function warn + export with space (`// export`) 
 - [] python type definition file
