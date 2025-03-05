
```bash
export LD_LIBRARY_PATH=./build
ipython
```

```python
from go_cool import http_test, add
from go_cool import map_test,map_test2
import go_cool
import random
import string
import requests

%timeit http_test("http://127.0.0.1:8000")
%timeit requests.get("http://127.0.0.1:8000")
%timeit request2("http://127.0.0.1:8000")

session = requests.Session()
%timeit session.get("http://127.0.0.1:8000")



%%timeit
import msgpack
map_test()
%timeit msgpack.unpackb(map_test2())
f2str(12.3456789)
go_cool.random_string(1_000).replace("a","b")
"".join(random.choices(string.ascii_lowercase, k=1_000)).replace("a","b")

myFunc(199,"12"*1_000_000)


%timeit 
import time
for a in range(100):
    t1=time.time()
    request2("http://127.0.0.1:8000/")
    t2=time.time()
    print(t2-t1)

```


# TODO
 - [] warn the use if it uses string or other dynamicly allocated types as result
 - [] unexported function warn + export with space (`// export`) 
 - [] python type definition file
