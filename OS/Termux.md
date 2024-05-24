# Termux

Set of instructions to setup Termux locally on Android to work productively

## Python/PIP 

Simply follow the link:
[Python instructions for Termux](https://wiki.termux.com/wiki/Python)

## Open Interpreter 


To install open-interpter on android just follow the instruction from 

[Github open-interprter-termux](https://github.com/MikeBirdTech/open-interpreter-termux)

## Failed to build  Kiwi 



[Github Link]( https://github.com/MikeBirdTech/open-interpreter-termux/issues/15)

```bash
_file="$(find $PREFIX/lib/python3.11 -name "_sysconfigdata*.py")"
rm -rf $PREFIX/lib/python3.11/__pycache__
cp $_file "$_file".backup
sed -i 's|-fno-openmp-implicit-rpath||g' "$_file"
```
