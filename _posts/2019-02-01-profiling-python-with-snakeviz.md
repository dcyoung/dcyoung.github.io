---
title: "Profiling Python w/ cProfile & Snakeviz"
date: 2019-02-01T00:00:00-00:00
last_modified_at: 2019-02-01T00:00:00-00:00
categories:
  - software notes
permalink: /post-profiling-python/
classes: wide
excerpt: Debugging and profiling python code using cProfile & snakeviz.
header:
  og_image: https://jiffyclub.github.io/snakeviz/img/icicle.png
  teaser: https://jiffyclub.github.io/snakeviz/img/icicle.png
---

Developer time is precious. The pragmatic approach involves making an informed decision about if or when to improve and refactor code. In the case of performance, this means:

- profiling the code
- identifying bottlenecks
- fixing low hanging fruit
- moving on!

Some languages and IDEs make this easy as the tooling encourages profiling. However python tooling lags behind. To profile python programs and prioritize refactors/ improvements, I use the following tooling:

- cProfile: a profiler which comes w/ python by default
- snakeviz: a visualization tool to inspect profile results (`pip install snakeviz`)

## An example

Consider the following naive python program:

```py
""" add_two_lists.py """
from time import perf_counter
from typing import List

def add_lists(a: List[int], b: List[int]) -> List[int]:
    return [x + y for x, y in zip(a, b)]

def main():
    length = 10000
    a = list(range(length))
    b = list(range(length))
    for _ in range(1000):
        _ = add_lists(a, b)

if __name__ == "__main__":
    tic = perf_counter()
    main()
    toc = perf_counter()
    print(f"Took {int(1000*(toc-tic))}ms")
```

Running the script:

```bash
$ python add_two_lists.py
$ Took 349ms
```

We can see that it takes ~350ms to complete, which is too slow. We'd like to improve the runtime but let's be smart about it.

First, profile the code and dump result to a file:

```bash
$ python -m cProfile -o before.cProfile add_two_lists.py
$ Took 410ms
```

Then visualize the profiling result (snakeviz will host a server you can visit in your browser to inspect the results):

```bash
$ snakeviz before.cProfile
```

![before](/images/profiling-python/before.jpg)

It looks like the majority of time is spent on line 6, in the list comprehension of method `add_lists`.

Armed with this information, let's focus our efforts on improving this method. I'll use numpy to speed things up:

```py
import numpy as np
from time import perf_counter

def add_lists(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a + b

def main():
    length = 10000
    a = np.asarray(list(range(length)))
    b = np.asarray(list(range(length)))
    for _ in range(1000):
        _ = add_lists(a, b)

if __name__ == "__main__":
    tic = perf_counter()
    main()
    toc = perf_counter()
    print(f"Took {int(1000*(toc-tic))}ms")
```

Running the updated program: 

```bash
$ python add_two_lists.py
$ Took 4ms
```

We made an an improvement on the order of 100x. Obviously this is toy example, but the technique is very powerful. Prioritize your time... its valuable!
