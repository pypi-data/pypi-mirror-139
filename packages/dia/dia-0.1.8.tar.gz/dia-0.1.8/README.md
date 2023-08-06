Dia
===

Have you ever spent a long day at work, only to wonder at the end of it what you
actually got done? Do you wish you remembered why you made a decision way back when?
Do you want to find the day you worked on a specific thing, but haven't left any trace?

Dia solves all those problems by helping you keep a work diary.


Installation
------------

Installing Dia is simple. You can use `pipx` (recommended):

```bash
$ pipx install dia
```

Or `pip` (less recommended):

```bash
$ pip install dia
```


Usage
-----

To log a task you've completed, you can use `dia log`:

```bash
$ dia log "Completed the diary feature."
```

This will generate the following `diary.txt` in the current directory (or append to it
if it already exists):

```md
Work diary
==========


2022-02-09
----------

* Completed the diary feature.
```

If you want to specify a fixed file to always work on, you can do that by setting the
`diary` option in `~/.config/dia/config`:

```ini
diary="/home/stavros/diary.txt"
```

You can similarly override any other options.


Semantic tags
-------------

Dia supports (though currently very tenuously) semantic tags. This means it can
understand people, projects, and tags. For example, you can say:

```bash
$ dia log "Worked on the %Dia #data-model with @JohnK."
```

You can show all items with:

```bash
$ dia show projects

Projects
========
* Dia
* Foo
* Bar
* Baz
```

Same with `tags` and `people`.

# Changelog


## v0.1.8 (2022-02-20)

### Features

* Add the "show week" command. [Stavros Korokithakis]

### Fixes

* Fix calling "standup" with an empty log. [Stavros Korokithakis]


## v0.1.7 (2022-02-16)

### Features

* Add the "standup" command. [Stavros Korokithakis]

* Add the "show people|tags|projects" commands. [Stavros Korokithakis]

* Allow passing a regex to the "search" command. [Stavros Korokithakis]

* Add the "edit" command. [Stavros Korokithakis]

### Fixes

* Reduce whitespace between elements. [Stavros Korokithakis]


## v0.1.6 (2022-02-11)

### Features

* Refactor "show" and add "show previous" command. [Stavros Korokithakis]

### Fixes

* Don't use pager on search. [Stavros Korokithakis]

* Don't show empty days in the "search" command. [Stavros Korokithakis]


## v0.1.5 (2022-02-11)

### Features

* Wrap long task text. [Stavros Korokithakis]

* Add "search" command. [Stavros Korokithakis]

### Fixes

* Fix diary config name. [Stavros Korokithakis]


