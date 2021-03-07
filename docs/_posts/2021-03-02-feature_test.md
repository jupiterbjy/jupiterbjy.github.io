---
layout: post
title:  "Feature test"
date:   2021-03-02 17:55:47 +0900
categories: jekyll update
mathjax: true
mermaid: true
console: true
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

---  

[라텍스 문법](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

```ignorelang
$$f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$$
```

$$f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...$$

> 달러기호가 자주쓰여 기본적으론 인라인으로 취급안함. 헤더에서 인라인 명시자 확인할것.  
> 여기서 설정된 명시자는 $@ @$. 뭔짓을해도 우연히 이걸 치는 일은 없을거란 판단.


인라인1 $@f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...@$
```
인라인1 $@f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...@$
```

인라인2 \\(f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...\\)
```
인라인2 \\(f(x) = f(c) + f'(c)(x - c) + \frac{f''(c)(x - c)^2}{2!} + ...\\)
```

---

[그래핑 문법](https://mermaid-js.github.io/mermaid/#/)  
[그래핑 문법 2](https://mermaid-js.github.io/mermaid/#/flowchart?id=flowcharts-basic-syntax)

그래프도 모종의 이유로 mermaid 를 무시해 해당 HTML 코드 사용할것.

```ignorelang
<div class="mermaid">
graph BT
    id1(기초교양)-->전문교양
    id2(핵심교양)-->전문교양
    id3(일반교양)-->전문교양
    id4(교양선택)
</div>
```

<div class="mermaid">
graph BT
    id1(기초교양)-->전문교양
    id2(핵심교양)-->전문교양
    id3(일반교양)-->전문교양
    id4(교양선택)
</div>
