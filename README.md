# org-reports

## Introduction

[org-reports](https://www.github.com/sp1ff/org-reports) is a *very*
preliminary attempt at a tool for generation various sorts of reports
from [Org](https://www.org-mode.org) files.

## Current Sub-commands

[org-reports](https://www.github.com/sp1ff/org-reports) can produce
two reports: contexts & projects.

### Contexts

I use GTD, and I was curious as to how many open tasks I have in each
context. I represent context as an Org property, so really all I want
to do is partition all my open tasks by that property value:

``` shell
org-reports contexts -p Context -s TOOD -s IN-PROGRESS -s WAITING ...
```
This will produce a report like:

``` text

166 tasks in 10 Contexts:

| Context                          | # Tasks |        |
|----------------------------------+---------+--------|
| @online                          |      69 |  41.6% |
...
|----------------------------------+---------+--------|

8 tasks with no contexts:

| Task                      | File                   |
|---------------------------+------------------------|
| establish NAs RE ...      |/Users/.../projects.org |
...
|---------------------------+------------------------|
```

### Projects

I haven't been able to generalize this one: for me, a project is a task
at indent level 2, with the `project` tag, *without* the `inactive` tag.

``` shell
org-reports projects projects.org
```

will produce a little report of such items.

### Properties

This is a generalization of the =contexts= sub-command. You can
specify multiple properties & get a report of all the tasks broken
out by the product of the vector of values for each property.

For instance, suppose you use two properties Foo & Bar. Over all
your tasks, the values of Foo range over [A, B, C] and those of
Bar [X, Y, Z].

``` shell
org-reports properties -p Foo -p Bar projects.org

| Foo, Bar            | # Tasks|
|---------------------+--------|
| A,X                 | 12     |
| A,Y                 | 1      |
| B,X                 | 100    |
...
|---------------------+--------|
```

## Installing & Running

This is also extremely
preliminary. [org-reports](https://www.github.com/sp1ff/org-reports)
uses [PyOrgMode](https://github.com/bjonnh/PyOrgMode/), but requries
a [PR](https://github.com/bjonnh/PyOrgMode/pull/41) that `bjohnh` has
not yet merged. So... to set this up:

``` shell
cd /tmp
git clone git@github.com:sp1ff/PyOrgMode.git
git clone git@github.com:sp1ff/org-reports.git
cd org-reports
virtualenv venv
. venv/bin/activate
cd ../PyOrgMode
git checkout sp1ff-tag-inheritance
python setup.py install
cd ../org-reports
python setup.py develop
```

Lame, I know, but until my PR is merged, I'm not sure what else
to do. Maybe I'll look into producing a `.pex` file.

In the meantime, I've wrapped much of this up in a script `autogen.sh`
(yes, I'd rather be working in C++ using `autotools`).

You _can_ install it normally, as well:

``` shell
cd /tmp
git clone git@github.com:sp1ff/PyOrgMode.git
cd PyOrgMode
git checkout sp1ff-tag-inheritance
sudo -H python setup.py install --record files.txt
cd ..
git clone git@github.com:sp1ff/org-reports.git
cd org-reports
sudo -H python setup.py install --record files.txt
```

## Future Development

I'm not sure what, if anything, I'll do with it, but back when I
was using Emacs Planner, this sort of tool found some use.

Other features that might be useful:

  - produce a list of all Todos moved to DONE this day, week, month, &c
  - identify languishing tasks
    - report on items by time since they entered their current state
