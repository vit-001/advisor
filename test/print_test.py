# -*- coding: utf-8 -*-
__author__ = 'Vit'

def print2(*data,**kw):
    print(kw)
    _end=kw.get('end','\n')
    _sep=kw.get('sep',' ')
    first=True
    for t in data:
        if first:
            first=False
        else:
            print(_sep,end="")
        print(t,end="")

    print(end=_end)

if __name__ == "__main__":
    print('222','1111',end=' zzz\n',sep='..')
    print2('222','1111',end=' zzz\n',sep='..')
