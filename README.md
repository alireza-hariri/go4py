
```bash
export LD_LIBRARY_PATH=./build
ipython
```

```python
import go_cool
import random
import string

%%timeit
go_cool.random_string(1_000).replace("a","b")
"".join(random.choices(string.ascii_lowercase, k=1_000)).replace("a","b")
```


# TODO
 - [] warn the use if it uses string or other dynamicly allocated types as result
 - [] unexported function warn + export with space (`// export`) 