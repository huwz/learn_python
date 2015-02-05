subprocess模块
==============

``subprocess.Popen``
--------------------

.. note:: 类

构造函数常用参数：

* ``args`` 字符串或者参数序列。
* ``shell=False`` 是否打开命令窗口执行命令行
* ``stdin=None`` 可以取 ``PIPE``，文件句柄，文件描述符和 ``None``
* ``stdout=None`` 可以取 ``PIPE``，文件句柄，文件描述符和 ``None``
* ``stderr=None`` 可以取 ``PIPE``，文件句柄，文件描述符， ``STDOUT`` 和 ``None``
  
.. important:: 流对象为 ``None`` 时，子进程将继承父进程的标准流。

.. code-block:: python
 :linenos:

 #D:\hello_world.py
 print hello,world

 #D:\test_subprocess.py
 from subprocess import *

 # ``shell = True`` cannot be skipped, as it uses shell to run the command line
 open_obj = Popen('hello_world.py', shell = True, stdout = PIPE) 
 # If you want to ignore ``shell`` parameter, you can use executable parameter as below:
 # open_obj = Popen('python hello_world.py', stdout = PIPE)

 out_obj = open_obj.communicate()
 print open_obj[0]

``Popen`` 实例
--------------

* ``poll()``  子进程是否结束，返回 ``returncode`` 属性值
* ``wait()``  等待子进程结束，返回 ``returncode`` 属性值
  
  .. warning:: 构造 ``Popen`` 对象时，不要使用 ``PIPE`` 参数，会死锁。
  
* ``communicate()`` 阻塞式执行命令行，返回元组 ``(stdoudata, stderrdata)``。
  
  .. note:: 要返回元组 ``(stdoudata, stderrdata)``，实例化时，必须设置 ``stdout=PIPE``；
   要想将数据传递给子进程的输入流，必须设置 ``stdin=PIPE``。

* ``send_signal()`` 发信号给子进程(``SIGTERM``)
* ``terminate()`` 终止子进程
* ``kill()`` 杀死子进程
  
.. note:: 
   Windows 中 ``kill()/terminate()`` 一样，都是调用 Windows API：``TerminateProcess``；
   Unix 中 ``terminate()`` 发送消息 ``SIGTERM``， ``kill()`` 发送消息 ``SIGKILL``

* ``pid`` 表示子进程的 ID；如果使用 ``shell=True``，则表示命令窗进程的 ID
* ``returncode`` ``None`` 表示子进程未结束；Unix 中，``-N`` 表示等待信号 ``N`` 结束子进程。
* ``stdout`` 如果实例化时，设置 ``stdout=PIPE``，则 ``stdout`` 为子进程的输出流；否则为 ``None``
* ``stderr`` 如果实例化时，设置 ``stderr=PIPE``，则 ``stderr`` 为子进程的错误流；否则为 ``None``
* ``stdin`` 如果实例化时，设置 ``stdin=PIPE``，则 ``stdin`` 为子进程的输入流；否则为 ``None``

.. code-block:: python
 :linenos:

 open_obj = Popen('python hello_world.py', stdout=PIPE)
 print open_obj.stdout.read()

``subprocess`` 的便捷接口
-------------------------

* ``call()`` 阻塞式执行命令行，返回 ``returncode`` 属性值
  
  .. warning:: 不能设置参数 stdout=PIPE/stderr=PIPE，会死锁

* ``check_call()`` 阻塞式执行命令行，返回0，表示子进程正常退出；
  否则抛出异常 ``CalledProcessError``
* ``check_output()`` 阻塞式执行命令行，正常情况下返回命令行输出（字节数组）；
  否则抛出异常 ``CalledProcessError``

  .. note:: 不能使用 ``stdout=PIPE``，可以使用 ``stderr=STDOUT`` 来捕获并输出错误信息。
  
