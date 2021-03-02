---
layout: post
title:  "feature_test"
date:   2021-03-02 17:55:47 +0900
categories: jekyll update
---

```python
import functools
from typing import Callable 

def wrapper(func: Callable):
    
    @functools.wraps(func)
    def inner(*args):
        print(*args)    
        return func()
    
    return inner
    
```

$$f(x) = f(c) + f'(c)(x - c) + (f''(c)(x - c)^2)2! + ...$$  

[라텍스 문법](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
