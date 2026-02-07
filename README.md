# Very site, much wow

Almost entirely handcrafted site, excluding:

- fonts
- mermaid.js (graph display)
- mathjax (math display)
- github-markdown-css (for markdown styling since I'm still mere human)


## Scripts

- [build.py](build.py) - Actual generator using `markdown-it-py`
- [auto-rebuild.py](auto-rebuild.py) - For live-rebuild & refresh on file change using selenium
- [dumb_trio_server_O.py](dumb_trio_server_O.py) - Handwritten (probably unsecure) HTTP server from [my other repo](https://github.com/jupiterbjy/ProjectIncubator/tree/main/SingleScriptTools#readme)
- [watchdog_file_events.py](watchdog_file_events_m.py) - File watcher using watchdog, from [my other repo](https://github.com/jupiterbjy/ProjectIncubator/tree/main/SingleScriptTools#readme) 


## [But Whyyyyy!](https://youtu.be/oiuyhxp4w9I)

Sane person would be just using `jekyll` or something equivalent (like once I did).

But I am the person who'd go hard way and reinvent the wheel from scratch, all the way down to HTTP server!

It's been painful but fun journey, and hope this somehow helps someone else.

...though now I'm realizing I should've separated generator from site itself considering commit logs.


## TODO for self

- Tag system
- Better way to edit post (I mean, pycharm do works but something better)
- Archive bunch more VN song lyrics
