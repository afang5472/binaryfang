## binaryfang


Binaryfang is a binary exploitation auxliary tool which currently supports:

- memory inspection 
- memory expression constrain check
- memory modification 
- embedded tiny native debugger
- enhanced io with a pty simulator
- automation debugging(under develop && thinking:) )

### Why Creating This

-----

When I first taste pwnable about 1.5 year ago, 
I , just like other beginners, enjoy the convenience 
with pwntools that helps io, gef or peda that helps debug.

But when I get deeper into pwnables, 
I found some relative extreme scene requires 
me to be equipped with more automatic or powerful tools to 
increase my effiency than simple handy debugging techniques.

And pwntools io is not always stable as I expect :(

So, I added a module for pwntools on a boring Sunday afternoon
at my dormitory. named it as `binaryfang` , some habits to name 
things with a connection to my id :)

This module will continue under the support of pwntools `process` 
module, and `ptyprocess` for tty simulator. So it's install procedure just requires serveral lines of bash.

### Dependency

-----

This tool currently rely on default python, pwntools, and ptyprocess.
Will remove requirements from pwntools soon.

### Install 

-----

```bash 

git clone https://github.com/0xcc-Since2016/binaryfang

cd binaryfang

chmod +x ./update && ./update

pip install ptyprocess

```

### Usage

-----

```bash 

>>> from binaryfang import *

>>> you've got pwntools all functionality and binaryfang's at the same time.

```

For detailed usage example, please see examples folder inside this repo. the examples folder gives serveral usage sample in CTFs which might give you some inspiration :)


### Functionality

-----


- July,15 2018 Adding basic materials (basic mem reader, inspector)

- Oct, 31 2018 Finish mapping parse submodule

- Nov, 16 2018 Add embedded debugger first version

- Dec, 6  2018 add some examples

- Dec, 8  2018 add enhanced io module
