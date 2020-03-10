### Shell-Script

[https://net2.com/category/linux/ubuntu_tips_and_tricks/](https://net2.com/category/linux/ubuntu_tips_and_tricks/)

#### 1. $PS1 bash custom prompt in Linux

By default most Linux distro displays hostname and current working dir. U can easily customize your prompt ro display information important to you. Prompt is control via a special shell variable. U need to set PS1, PS2, PS3, PS4 variable.

+ PS1:  used as the primary prompt string, the default value is **\s-\v$.**

+ PS2: is expanded as with PS1 and used as the primary prompt string. The default is **>**

+ PS3: used as the prompt for the select command

+ PS4: is expanded as with PS1 and the valye is printed before each command bash displays during an execution trace, The first character od PS4 is replicated multiple times.

**Usage:**

```shell
# date time hostname and current work dir
PS1="[\d \t \u@\h:\w ] $ "
# add colors to my prompt
# append the code as follow to .bashrc
if [ $(id -u) -eq 0];
then
  PS1="\\[$(tput setaf 1)\\]\\u@\\h:\\w #\\[$(tput sgr0)\\]"
else
  PS1="[\\u@\\h:\\w] $"
fi
```

#### 2. some factors of good, clean, quick shell scripts

+ the most important criteria must be a clear, readable layout

+ second is avoiding unnecessary commands

```shell
# weakness
cat /tmp/myfile | grep "mystring"
# much faster
grep "mystring" /tmp/myfile
```

the OS has to load up the **/bin/grep** executable, which is a small 75600 bytes on my system, open a pipe in memory for the transfer, load and run the **/bin/cat** executable, which is an even smaller 9528 bytes on my system, attach it to the input of the pipe, and let it run.

#### 3. a first script 【echo】

```shell
#!/bin/sh
# This is a comment!
echo Hello World    # This is a comment!
```

+ first line tells Unix that the file is to be executed by /bin/sh. It means that even if u are using csh, ksh or anything else as ur interactive shell, that what follows should be interpreted by the Bourne Shell.

+ the second line begins with a special symbol: #. This marks the line as a comment, and it is ignored completely by the shell.

+ 要恶心我可以，但是别给我机会治你的恶心。

+ than run **chmod 755 first.sh** to make the text file executable, and run it.

+ **./first.sh**

```shell
#!/bin/sh
# This is a comment
echo Hello World
echo Hello       World     # many space between Hello and World
echo Hello    World        # a tab space between Hello and World
echo "Hello     World"     # one parameters
```

+ line 3 to line 5, echo has two parameters. but there is only one parameters in line 6. 

```shell
#!/bin/sh
# This is a comment
echo "Hello" World      # Hello World
echo Hello * World      # error
echo Hello "    " World    # Hello          World
echo `Hello` World      # `Hello` command not found
```

#### 4. Varaibles P1

##### what is vars  & basic usage of vars

`variables` - a symbolic name for a chunk of memory to which we can assign values, read and manipulate its contents. 

+ there must be no spaces around the "=" sign: VAR=value works, VAR = value doesn't work. **In firt case**, the shell sees the "=" symbol and treats the command as a variable assignment.**In second case**, the shell assumes that VAR must be the name of a command and tries to execute it.

```shell
#!/bin/sh
MY_MESSAGE_STRING='Hello World'
echo $MY_MESSAGE_STRING
MY_MESSAGE_VAR=Hello World
ehco $MY_MESSAGE_VAR
```

the difference between line2 to line3 and line 4 to line5 is that `MY_MESSAGE_STRING` is a string, and the shell will try to execute the command `World` after assigning  `MY_MESSAGE_VAR = Hello`.

+ the shell dose not care types of vars, they may store strings, integers, real numbers , anything u like.

```shell
# Linux command
# expr [expression] 
# expr evaluates an expression and writes the result on standard output.
expr 2 + 3
expr 'Hello World' : 'Hell\(.*\)rld'
expr index 'hello' 'lo'
```

+ Mac OS X is use BSD(伯克利发行版) expr, but Linux is generally uses GNU expr.

```shell
#!/bin/sh
echo What is ur name?
# read a line from std input into a var supplied
# if not input "caiqingjing", read command will automatically places quotes around its input.
read MY_NAME
echo "Hello $MY_NAME - hole u're well"
# do not use single quote, it's useless，will print Hello $MY_NAME....
```

##### Scope of vars

+ vars in Bourne Shell do not have to be declared.

+ if u read an undeclared var, u get no warning, and the result is an empty string.

+ ./start.sh be equal to source start.sh   # factly "."(dot) is a command. and u can receive environment changes back from the script.

+ touch `${USER_NAME}_file` , and u can create file named caiqingjing_file, just like Python fstring.

#### 5. Wildcards(通配符)

```shell
# copy
cp /tmp/a/* /tmp/b/
cp /tmp/a/*.txt /tmp/b/
cp /tmp/a/*.html /tmp/b/
# rename
mv *.txt *.bak
# ls
ls *.py
# echo 
echo *txt   # means that echo all files end with "txt"
```

#### 6. Escape Charachters

+ `*`  在字符串中不再起作用

+ `\`  在字符串中起转义作用

+ `echo "hello  "world""` 解释器将会echo 后面的解释成三个参数, `"hello "`、`world`、`""` 。

+ shell 中有三种字符会被解释器解释，分别是*, `, $, 只有他们被双引号包裹的时候，才不会被解释。

#### 7. Loops

+ we have `while` and `for` in Bourne Shell.

##### for loops

```shell
#!/bin/sh
for i in 1 2 3 4 5
do
  echo "Looping ... number $i"
done
```

```shell
#!/bin/sh
for i in hello 1 * 2 goodbye
do
  echo "Loop ... i is set to $i"
done
```

```shell
#!/bin/sh
for i in *
do
  echo "Loop ... i is set to $i"
done

# * is mean that all files in current path

i=*
echo "$i"
# u just have TEXT "*"
```

##### while loops

```shell
#!/bin/sh
INPUT_STRING=hello
while [ "$INPUT_STRING" != "bye" ]
do
  echo "Please type something in (bye to quit)"
  read INPUT_SRTING
  echo "You typed: $INPUT_STRING"
done  
```

```shell
#!/bin/sh
while
do
  echo "Please type something in (^C to quit)"
  read INPUT_STRING
  echo "You typed: $INPUT_STRING"
done
```

###### case

```shell
#!/bin/sh
while read f
do
  case $f in
       hello)                echo English           ;;
       howdy)                echo American          ;;
       gday)                 echo Australian        ;;
       bonjour)              echo French            ;;
       "guten tag")          echo German            ;; 
       *)                    echo Unknown Language: $f
                       ;;
  esac
done < myfile
```

+ read from `myfile` and for each line, tells you what language it is.

+ each line must end with LF(newline), if `myfile` doesn't end with blank line, that final line will not be processed.

```shell
#!/bin/sh
# on many Unix system, u also can use that
while f=`line`
do
  process line
done < myfile
# zsh 里不行
```

##### mkdir

```shell
mkdir rc{0,1,2,3,4,5,6,S}.d
# result is rc0.d ~ rcS.d
mkdir rc{S}.d
# result is rc{S}.d
```

##### command `{}`

```shell
echo {1,2,3}{a,b,c}   # result is: 1a,1b,1c,2a,2b,2c,3a,3b,3c
ls -ld {,usr,usr/local}{bin,sbin,lib}    # -d 列出目录信息，将会尝试列出/bin, /sbin, /lib, /usr/bin, /usr/sbin, /usr/lib, /usr/local/bin, /usr/local/sbin, /usr/local/lib 这几种目录信息
```

#### 8. Test

**用于检查某个条件是否成立，可以在数值、字符、文件三个方面进行测试**

`test` is more frequently called as `[`

+ `type test` <=> `type [`    # [ or test is a shell builtin

+ `[` is a symbolic `test` , just to make shell programs more readable.

`test` is actually a **program**, just like `ls`  and other programs, so it must be surrounded by space.

+ `if [$foo = 'bar' ]` is not work, cause it will be interpreted as `if test$foo = 'bar' ]`, which `]` without a beginning `[`. 

+ correct format should be: `if [ "$foo" = "bar" ]` 

#### 9. if...fi

```shell
if [ ... ]
then
    # if-code
else
    # else-code
fi
```

```shell
if [ ... ]; then
  echo "Something"
  elif [ something_else ]; then
    echo "Something else"
  else
    echo "None if the above"
fi
```

+ `;`  to join two lines together. This is often done to save a bit of space in simple if statements.

+ ```shell
  #!/bin/sh
  if [ "$X" -lt "0" ]
  then
    echo "X is less than zero"
  fi
  if [ "$X" -gt "0" ]; then
    echo "X is more than zero"
  fi
  [ "$X" -le "0" ] && \
        echo "X is less than or equal to  zero"
  [ "$X" -ge "0" ] && \
        echo "X is more than or equal to zero"
  [ "$X" = "0" ] && \
        echo "X is the string or number \"0\""
  [ "$X" = "hello" ] && \
        echo "X matches the string \"hello\""
  [ "$X" != "hello" ] && \
        echo "X is not the string \"hello\""
  [ -n "$X" ] && \
        echo "X is of nonzero length"
  [ -f "$X" ] && \
        echo "X is the path of a real file" || \
        echo "No such file: $X"
  [ -x "$X" ] && \
        echo "X is the path of an executable file"
  [ "$X" -nt "/etc/passwd" ] && \
        echo "X is a file which is newer than /etc/passwd"
  ```

```shell
x=''
[ -n $x ] && echo "-${x}-"                   # 输出
[ -n '' ] && echo "-hello world-"            # 不输出
```

+ `-lt` `-gt` `-le` `-ge` comparisions are only designed for integers, and do not work on strings. 

+ check the content of the variable before u test it -.
  
  ```shell
  echo -en "Please guess the magic number: "
  read X
  echo $X | grep "[^0-9]" > /dev/null 2>&1
  if [ "$?" -eq "0" ]; then
    echo "Sorry, wanted a number"
  else
    if [ "$X" -eq "7" ]; then
      echo "You entered the magic number"
    fi
  fi
  ```

+ `$?` 是最后运行的命令的结束代码(返回值)

+ `grep` 
  
  + `grep "[0-9]"` find lines of text which contain digits(0-9) and possibly other characters
  
  + `grep "[^0-9]"` find only those lines which don't consist only of numbers

+ `/dev/null`
  
  + virtual device file, treat it just like real files.
  
  + data written to the `/dev/null` and `/dev/zero` special files is discarded.
  
  + read from `/dev/null` always return end of file; read from `/dev/zero` always return bytes containing zero.
  
  + `cmd > /dev/null` 通常用于忽略掉输出

+ `cmd >/dev/null 2>&1` 
  
  + **0**: stdin; **1**: stdout; **2**: stderr
  
  + 使用`>`或`>>`时，默认为`1>file`，简写为`>file` ;
    
    + `ls -l > a.txt` == `ls -l 1> a.txt`
    
    + `2>&1` 表示把 标准错误输出 重定向到 标准输出。
    
    + `&` 意味着 `&1` 中的 1 是文件描述符，而不是文件名。
  
  + cmd 产生的输出 由标准输出 重定向到 空设备文件，标准错误输出 重定向到 标准输出，所以标准错误输出 也同样重定向到 空设备文件。所以 cmd 执行完不会在屏幕上打印出任何东西。

+ `grep -v "[0-9]"`  参数 `-v` 的结果和上一条一样。这样写更加简洁。

+ test2.sh
  
  ```shell
  #!/bin/sh
  X=0
  # while [ ! -n "$X" ] !取反
  while [ -n "$X" ]
  do
    echo "Enter some text (RETURN to quit)"
    read X
    echo "U said: $X"
  done
  ```
  
  + 如果输入''，实际上变量X的值为"''"，按下回车才是空

#### 10. Case

不常用，就写一个用例。

```shell
#!/bin/sh

echo "Please talk to me ..."
while :
do
  read INPUT_STRING
  case $INPUT_STRING in
    hello)
        echo "Hello yourself!"
        ;;
    bye)
        echo "See you again!"
        break
        ;;
    *)
        echo "Sorry, I don't understand"
        ;;
  esac
done
echo 
echo "That's all folks!"
```

#### 11. Variables - Part 2

+ `$0 .. $9` and `$#` and `$@`
  
  + `$0`: the basename of the program as it was called. output is: -zsh
  
  + `$1 .. $9`: the first additional parameters the script was called with; `$@ and $*` is all parameters `$1 .. whatever`, use `$@` and avoid `$*`
  
  + `$#` is the number of parameters the script was called with
  
  ```shell
  #!/bin/sh
  echo "I was called with $# parameters"
  echo "My name is $0"
  echo "My first parameter is $1"
  echo "My second parameter is $2"
  echo "All parameters are $@"
  
  $ ./var3.sh hello world earth
  I was called with 3 parameters
  My name is ./var3.sh
  My first parameter is hello
  My second parameter is world
  All parameters are hello world earth
  ```

+ **`shift`** command
  
  ```shell
  #!/bin/sh
  while [ "$#" -gt "0" ]
  do
    echo "\$1 is $1"
    shift
  done
  ```
  
  + `./test.sh hello world caiqj hahah`
    
    ```shell
    $1 is hello
    $1 is world
    $1 is caiqj
    $1 is hahahah
    ```

+ `$?` contains the exit value of the last run command.
  
  ```shell
  #!/bin/sh
  /user/local/bin/my-command
  if [ "$?" -ne "0" ];then
    echo "Sorry, we had a problem there!"
  fi
  ```
  
  + exit with a value of zero if all went well;
  
  + `$$` is the PID of the currently running shell. This can be useful for creating temporary files.
  
  + `$!` is the PID of the last run background process. This is useful to keep track of the process as it gets on with its job.
  
  + `IFS` is the *Internal Field Separator*，the default value is `SPACE TAB NEWLINE`
    
    ```shell
    #!/bin/sh
    old_IFS="$IFS"
    IFS=:
    echo "Please input some data separated by colons ..."
    read x
    IFS=$old_IFS
    echo "x is $x y is $y z is $z"
    ```
    
    + `IFS=:` 指定分隔符是一个冒号
    
    + $IFS 是 shell 的环境变量，zsh 会根据 IFS 存储的值，来解析输入和输出的变量值
      
      ```shell
      # 这里要注意其实是不应该这样直接修改IFS系统级的变量的
      # 否则程序会出现不可预料的奇怪的问题
      IFS='|'
      text='a a a a|b b b b|c c c c'
      for i in $text
      do 
        echo "i=$i"
      done
      ```

#### 12. Variables - Part 3

+ In the shell, there's not much difference between `undefined` and `null` 

+ **Using Default Values**
  
  + ```shell
    #!/bin/sh
    echo -en "What is your name [ `whoami` ]"    # -n 不换行输出 -e 处理特殊字符(\n直接输出`\n`而不是换行)
    read myname
    if [ -z "$myname" ];then
      myname=`whoami`
    fi
    echo "Your name is: $myname"
    ```
  
  + `-en` tell bash or csh not to add a linebreak;（`\c` at the end of line in Dash Bourne）
  
  + this could be done better using a shell variable feature.
    
    ```shell
    # whoami command which prints your login name(UID)
    echo "Your name is: ${myname:-`whoami`}"
    ```
  
  + there is another syntax ":=", which sets the variable to the default if it is undefined.
    
    ```shell
    echo "Your name is : ${myname:=John Doe}"
    ```

#### 13. External Porgrams

+ there are a few builtin commands(`echo`,`which`,`test` are commonly builtin), but many useful commands are actually Unix utilities, such as `tr`,`grep`,`expr`,`cut`.

+ the backtick (`) is used to indicated that the enclosed text is to be executed as a command.

+ use an interactive shell to read your full name from `/etc/passwd`

```shell
$ grep "^${USER}:" /etc/passwd | cut -d: -f5
# 等价于
$ MYNAME=`grep "^${USER}:" /etc/passwd | cut -d: -f5`
$ echo $MYNAME
Steve Parker
```

+ so we see that the backtick simply catches the stantard output from any command or set of commands we choose to run.

```shell
#!/bin/sh
find / -name "*.html" -print | grep "index.html$"
find / -name "*.html" -print | grep "/contents.html$"
```

```shell
#!/bin/sh
HTML_FILES=`find / -name "*.html" -print`
echo "$HTML_FILES" | grep "/index.html$"
echo "$HTML_FILES" | grep "/contents.html$"
```

+ `grep` will see one huge long line of text, and not one line per file.

#### 15. grep

+ `grep 'single_world'  first_file_name  second_file_name`

+ `grep -i "Domain" index.html` #  use -i to ignore word case

+ `cat index.html | grep -i 'Domain'`  

+ `dpkg --list | grep -i 'sql'` #  dpkg 是 Debian 系统用来安装用的

+ `cat index.html | grep -A 1 "/head"`  #  显示有/head在的那行的后一行

+ `cat index.html | grep -B 1"/head"` #  显示有/head在的那行的前一行

#### 16. functions

   传统上，函数的定义是返回单个值，并且不会输出任何内容。过程不返回值，但可以产生输出。Shell 函数可能不会执行任何操作，过着两者都执行。通常，在 Shell 脚本中将它们成为函数。

##### 16.1 函数可以通过以下方式返回值

+ Change the state of a variable or variables

+ Use the `exit` command tp end the Shell Script

+ Use the `return` command to end the function, and return the supplied value to the calling section of the shell script

+ Echo output to stdout, which will be caught by the caller just as c=`expr $a+$b` is caught

Shell function cannot change its params, though it can change global params.

##### 16.2 Example

```shell
#!/bin/sh
# A simple script with a function

add_user()
{
    USER=$1
    PASSWORD=$2
    shift; shift;
    echo "Adding user $USER ..."
    echo useradd -c "$COMMENTS" $USER
    echo passwd $USER $PASSWORD
    echo "Added user $USER ($COMMENTS) with pass $PASSWORD"    
}

###
# Main body of script starts here
###
echo "Start of script..."echo 
add_a_user bob letmein Bob Holness the presenter
add_a_user fred badpassword Fred Durst the singer
add_a_user bilko worsepassword Sgt. Bilko the role model
echo "End of script..."
```

+ `useradd` 用于创建或更新用户信息。
+ `/etc/passwd` 文件中，每行的第四个字段指定的就是用户的初始群组。
  + `root:x:0:0:root:/root:/bin/bash` 用户名:口令:用户标识号:注释性描述:主目录:登录shell
  + 口令：真正加密后的用户口令放在 `/etc/shadow` 文件中，而在 `/etc/passwd` 中的口令字段只存放一个特殊的字符。例如'x'或者'*'
  + 用户标识号：一般情况下和用户名是一一对应的。但如果有几个用户名对应的用户标识号是一样的话，系统内部会将它们视作同一个用户。但是他们可以有不同的口令，主目录，以及不同的登录shell等。0是root。1-99由系统保留，作为管理账号。普通用户从100开始。
  + `caiqingjing:x:1005:1005::/home/caiqingjing:/bin/bash` username:pwd:uid:gid:注释性描述:主目录:shell

#### 17. Scope of variable

```shell
#!/bin/sh
myfunc()
{
	echo "I was called as : $@"
	x=2
}
echo "Script was called with $@"
x=1
echo "x is $x"
myfunc 1 2 3
echo "x is $x"

```

+ `$@` was changed within the function to reflect how the function was called.

+ the variable `x` is a global variable. 作用域是这个脚本从开始到结束

+ a function will be called in a sub-shell if its output is piped somewhere else-that is `myfunc 1 2 3 | tee out.log` will still say `x is 1` 

  + `tee` command reads the standard input and writes it to both the standard output and one or more files.

  + Cause a new shell process is called to pipe `myfunc()` 

```shell
#!/bin/sh

myfunc()
{
  echo "\$1 is $1"
  echo "\$2 is $2"
  # cannot change $1 - we'd have to say:
  # 1="Goodbye Cruel"
  # which is not a valid syntax. However, we can
  # change $a:
  a="Goodbye Cruel"
}

### Main script starts here 

a=Hello
b=World
myfunc $a $b
echo "a is $a"
echo "b is $b"
```

+ 传进来的$1这种变量是不能更改的

#### 18.Recursion

```shell
#!/bin/sh

factorial()
{
  if [ "$1" -gt "1" ]; then
    i=`expr $1 - 1`
    j=`factorial $i`
    k=`expr $1 \* $j`
    echo $k
  else
    echo 1
  fi
}


while :
do
  echo "Enter a number:"
  read x
  factorial $x
done 
```

```shell
# common.lib
# Note no #!/bin/sh as this should not spawn 
# an extra shell. It's not the end of the world 
# to have one, but clearer not to.
#
STD_MSG="About to rename some files..."

rename()
{
  # expects to be called as: rename .txt .bak 
  FROM=$1
  TO=$2

  for i in *$FROM
  do
    j=`basename $i $FROM`
    mv $i ${j}$TO
  done
}
```

+ `basename`  可以从一个路径里面取出文件名 
+ `dirname` 可以生成这个文件的相对路径

```shell
#!/bin/sh
# how to use that
. ./common.lib
echo #STD_MSG
rename .txt .bak
```

#### 19. Return Codes

```shell
#!/bin/sh

adduser()
{
  USER=$1
  PASSWORD=$2
  shift ; shift
  COMMENTS=$@
  useradd -c "${COMMENTS}" $USER
  if [ "$?" -ne "0" ]; then
    echo "Useradd failed"
    return 1
  fi
  passwd $USER $PASSWORD
  if [ "$?" -ne "0" ]; then
    echo "Setting password failed"
    return 2
  fi
  echo "Added user $USER ($COMMENTS) with pass $PASSWORD"
}

## Main script starts here

adduser bob letmein Bob Holness from Blockbusters
ADDUSER_RETURN_CODE=$?
if [ "$ADDUSER_RETURN_CODE" -eq "1" ]; then
  echo "Something went wrong with useradd"
elif [ "$ADDUSER_RETURN_CODE" -eq "2" ]; then 
   echo "Something went wrong with passwd"
else
  echo "Bob Holness added to the system."
fi

```

#### 20. Hints and Tips

```shell
#!/bin/sh
steves=`grep -i steve /etc/passwd | cut -d: -f1`
# grep -i 忽略大小写
# cut -d 指定字段的分隔符，默认的字段分隔符是 TAB
# cut -f 选取指定的是第几个域，如果是 cut -f1 意思就是显示第一个域
```

```shell
# \r\n 什么要先回车再换行呢，先把指向当前的坐标转到行首，然后再换行。因为这个是以前用来控制打印机针头的。
echo 'steves' | tr 'e' '\012'   #\012 就是 \n 的八进制形式
# tr 是 replace 的意思
tr '[a-z]' '[A-Z]'   # 转成大写
```

#### 21. Cheating

+ `awk` 

  + `wc` counts the number of characters, lines, and words in a text file.

  + ```shell
    wc example.txt
        4       5      99 example.txt
    ```

  + if we want to get the number of lines into a variables, using that

  + ```shell
    NO_LINES=`wc -l file`
    # awk 的默认域分隔符是whitespace或是tab，$1、$2 表示第几个域，$0表示所有域
    a=`wc -l example.txt | awk '{ print $1 }'`
    ```

+ `sed`

  + Means that stream editor; Perl is very good at dealing with regular expressions, the shell isn't. So we can quickly use the `s/from/to/g` construct by invoking `sed` .

  + ```shell
    # change every instance of eth0 in file1 to eth1 and write into file2
    sed s/eth0/eth1/g file1 > file2
    # if we were only changing a single character, tr would be the tool to use.
    echo ${SOMETHING} | sed s/"bad word"//g
    # grep 也可以替换字符，但是替换的是文件中的字符。sed 替换的是缓冲区中的字符，并不修改文件中的内容。
    ```

#### 21. Telnet hint

+ telnet命令通常用来远程登录。telnet程序是基于TELNET协议的远程登录客户端程序。Telnet协议是TCP/IP协议族中的一员，是Internet远程登陆服务的标准协议和主要方式。它为用户提供了在本地计算机上完成远程主机工作的 能力。在终端使用者的电脑上使用telnet程序，用它连接到服务器。终端使用者可以在telnet程序中输入命令，这些命令会在服务器上运行，就像直接在服务器的控制台上输入一样。可以在本地就能控制服务器。要开始一个 telnet会话，必须输入用户名和密码来登录服务器。Telnet是常用的远程控制Web服务器的方法。
+ 但是，telnet因为采用明文传送报文，安全性不好，很多Linux服务器都不开放telnet服务，而改用更安全的ssh方式了。

#### 22. Quick Reference

|   command   |                       description                       |             example              |
| :---------: | :-----------------------------------------------------: | :------------------------------: |
|      &      |                     在后台运行命令                      |               ls &               |
| && and \|\| |                    逻辑与 和 逻辑或                     |           If [] && []            |
|   ^ and $   |                       行首和行尾                        |    grep "^foo" 和 grep "foo$"    |
|  = and !=   |             等于和不等于(用于字符串的比较)              |      if [ "$foo" != "bar" ]      |
|  $$ and $!  |          当前shell的PID和最后执行的后台进程PID          |        echo "my PID = $$"        |
|     $?      |                  最后一条命令的返回码                   |  ls ; echo "ls returned code $?  |
|     $0      |                     当前shell的name                     |          echo "I am $0"          |
|     $@      | 执行当前脚本所传入的所有参数(保留whitesapce 和 quoting) |    echo "My arguments are $@"    |
|     $*      |           同上，但不保留whitespace 和 quoting           |    echo "My arguments are $@"    |
|     -eq     |                    Numeric equality                     |      If [."$foo" -eq "9" ]       |
|     -ne     |                   Numeric Inequality                    |      If [."$foo" -ne "9" ]       |
|     -lt     |                        less than                        |      if [ "$foo" -lt "9" ]       |
|     -le     |                   Less than or equal                    |      if [ "$foo" -le "9" ]       |
|     -gt     |                      Greater than                       |      if [ "$foo" -gt "9" ]       |
|     -ge     |                  Greater than or equal                  |      if [ "$foo" -ge "9" ]       |
|     -z      |                  string is zero length                  |         if [ -z "$foo" ]         |
|     -n      |                String is not zero length                |         if [ -n "$foo" ]         |
|     -nt     |                       Newer than                        |  if [ \"$file1" -nt "$file2" ]   |
|     -d      |                     Is a directory                      |          if [ -d /bin ]          |
|     -f      |                        Is a file                        |        if [ -f /bin/ls ]         |
|     -r      |                   is a readable file                    |        if [ -r /bin/ls ]         |
|     -w      |                   Is a writable file                    |        if [ -w /bin/ls ]         |
|     -x      |                  is a executable file                   |        if [ -x /bin/ls ]         |
|     ()      |                   function definition                   | function myfunc() { echo hello } |

#### 24. Interactive Shell

However the root shell should always be `/bin/sh`, whether that points to bash or Bourne shell. `ctrl+r` 可以反向搜索历史命令使用。

+ press `ctrl+r`. 
+ if u want search cut, just enter 'cut'.
+ If current command in shell is not ur want, press`ctrl+r` some times.

##### bash

if u want to repeat a command u ran before, and u know what characters it started with, 你就可以输入`!g`, if the result is not u want, 你可以按上下键翻页。

```shell
bash$ ls /tmp
(list of files in /tmp)
bash$ touch /tmp/foo
bash$ !l
ls /tmp
(list of files in /tmp, now including /tmp/foo)
```

+ `cd -` + `TAB` 可以显示出最近跳转过的路径

#### zsh

[zsh的一些使用技巧](https://www.zhihu.com/question/21418449)

