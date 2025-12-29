<!-- HEADER
title: Feature test
date: 2021-03-02 17:55:47 +0900
layout: post
tags: test
plugins: mathjax mermaid
-->

# Feature test

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

---  

[레이텍 문법](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

```ignorelang
$$f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$$
```

$$f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$$

> 달러기호가 자주쓰여 기본적으론 인라인으로 취급안함. 헤더에서 인라인 명시자 확인할것.


인라인1 $f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$
```
인라인1 $f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$
```

인라인2 \\(f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...\\)
```
인라인2 \\(f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...\\)
```

---

[그래핑 문법](https://mermaid-js.github.io/mermaid/#/)  
[그래핑 문법 2](https://mermaid-js.github.io/mermaid/#/flowchart?id=flowcharts-basic-syntax)

렌더링 후엔 mermaid 코드블럭이 남지 않기에 해당 HTML 코드 사용할것.

```html
<div class="mermaid">
graph BT
    id1(기초교양)-->전문교양
    id2(핵심교양)-->전문교양
    id3(일반교양)-->전문교양
    id4(교양선택)
</div>
```

```mermaid
graph BT
    id1(기초교양)-->전문교양
    id2(핵심교양)-->전문교양
    id3(일반교양)-->전문교양
    id4(교양선택)
```

<div class="mermaid">
graph BT
    id1(기초교양)-->전문교양
    id2(핵심교양)-->전문교양
    id3(일반교양)-->전문교양
    id4(교양선택)
</div>

<iframe width="560" height="315" src="https://www.youtube.com/embed/goE8Xnwo0fI?si=ai0W-HB1s1T5vmsQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
