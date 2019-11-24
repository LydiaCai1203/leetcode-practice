# shell script

    就之前发现shell脚本自己一点都看不懂，实在是很惭愧了，随意学一下，认真学一下。

## shell
    shell 是一种程序，能够从键盘上接收命令， 然后把它们交给操作系统去执行。如: sh、bash、zsh。实际上就是Command Line Interface。
    bash 的全拼是 Bourne Again SHell.基于 sh 的扩展，原先写 sh 的人是 Steve Bourne。

## terminal emulators
    termial emulators 可以打开一个窗口，让你和 shell 进行互动。如: iTerm。

## root and others
    [username@machine_name path]#     superuser
    [username@machine_name path]$     others

## file system organization
    Unix-like OS 是树结构文件模式，但是没有盘符(drive letter)的概念，可以理解为只有单棵树。不管有多少 devices，始终是一棵树。
    Legacy OS 的文件系统结构模式是多树结构，盘符会将文件系统分隔开来。
    
    # what is legacy OS?
    A legacy platform, also called a legacy operating system, is an operating system (OS) no longer in widespread use, or that has been supplanted by an updated version of earlier technology.For example, Windows XP.

## commands
### pwd (print working directory)
    