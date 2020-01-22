### Shell-Script

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
while ["$INPUT_STRING" != "bye"]
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

#### Test

**用于检查某个条件是否成立，可以在数值、字符、文件三个方面进行测试**

`test` is more frequently called as `[`

+ `type test` <=> `type [`    # [ or test is a shell builtin

+ `[` is a symbolic `test` , just to make shell programs more readable.

`test` is actually a **program**, just like `ls`  and other programs, so it must be surrounded by space.

+ `if [$foo = 'bar' ]` is not work, cause it will be interpreted as `if test$foo = 'bar' ]`, which `]` without a beginning `[`. 

+ correct format should be: `if [ "$foo" = "bar" ]` 

#### if...fi

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






