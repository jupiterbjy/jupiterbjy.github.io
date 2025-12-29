# Very site, much wow

> Currently under heavy reconstruction from scratch

Almost entirely handcrafted site, excluding:

- fonts
- mermaid.js (graph display)
- mathjax (math display)
- github-markdown-css (for rendered markdown since I'm still mere human)

Uses homebuilt static site generator that only relies on `markdown-it-py`:

- [build.py](build.py) - Actual generator
- [auto-rebuild.py](auto-rebuild.py) - For live-rebuild & refresh on file change using selenium
- [dumb_trio_server_O.py](dumb_trio_server_O.py) - Handwritten (probably unsecure) HTTP server from [my other repo](https://github.com/jupiterbjy/ProjectIncubator/tree/main/SingleScriptTools#readme)
- [watchdog_file_events.py](watchdog_file_events_m.py) - File watcher using watchdog, from [my other repo](https://github.com/jupiterbjy/ProjectIncubator/tree/main/SingleScriptTools#readme) 


## But Whyyyyy!

Sane person would be just using `jekyll` or something equivalent (like once I did).
But I am the person
who'd go hard way and reinvent the wheel from scratch - all the way down to HTTP server!

