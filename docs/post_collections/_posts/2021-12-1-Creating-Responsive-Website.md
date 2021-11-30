---
layout: post
title: "Struggle of creating responsive Webpage"
date: 2021-12-01 00:02:00 +0900
categories: personal diary web
mermaid: true
---

This is really frustrating.

Look at this.

![image](https://user-images.githubusercontent.com/26041217/144096617-4743b600-a017-46ea-970b-40b5fe318e9e.png)

This margin collapse into other's margin, aka margins are overlapping.

However...

![image](https://user-images.githubusercontent.com/26041217/144096756-8687d2de-58be-410d-a85f-e54e46269a27.png)

What a Suprise! This clearly against of "least suprise".

Turns out, margin *DOES NOT* collapse horizontally.

Therefore, following setup is needed.

```css
...

#live2d_canvas {
    background: white;
    border: 0.2rem dotted lightcoral;
    box-sizing: border-box;
}

.right_panel {
    background: darkgrey;
    border: 0.2rem dotted #3C3F41;
    box-sizing: border-box;
}


@media all and (orientation: landscape){
    #live2d_canvas {
        float: left;
        margin: 1em;
        width: calc(75% - 1.5em);
        height: calc(100% - 2em);
    }

    .right_panel {
        float: right;
        margin: 1em 1em 1em 0;
        width: calc(25% - 1.5em);
        height: calc(100% - 2em);
    }
}

@media all and (orientation: portrait){
    #live2d_canvas {
        margin: 1em;
        width: calc(100% - 2em);
        height: calc(75% - 1.5em);
    }
    .right_panel {
        margin: 1em;
        width: calc(100% - 2em);
        height: calc(25% - 1.5em);
    }
}
```

Yes, by explicitly removing left side's margin of side pannel. This took a good amount of my important time, sadly

Check out [this jsfiddle](https://jsfiddle.net/jupiterbjy/pxLea6sm/5/) if below embed doesn't work.

<script async src="//jsfiddle.net/jupiterbjy/pxLea6sm/2/embed/js,html,css,result/dark/" markdown="1"></script>

