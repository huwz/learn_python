URL访问的扩展库—— ``urllib2``
=============================

``urllib2`` 模块定义了一些更复杂的函数和访问 URL 地址（绝大多数都是 ``HTTP`` 协议）的类。
主要用于基础和摘要式的身份验证，网页跳转，网页曲奇等等。

``urllib2`` 定义了以下函数

``urllib2.urlopen(url, [,data][,timeout])``
-------------------------------------------

打开一个 URL，参数 url 是一个字符串，或者一个 ``Request`` 对象。

.. warning:: HTTPS 请求不做任何的服务器认证确认

参数 data 是字符串或者或者 None，传递给服务器。
现在，HTTP 请求是唯一用到 *data* 的用户请求；
如果数据参数不为 None，则 HTTP 请求将为 POST 方式。
数据参数必须是一个 ``application/x-www-form-urlencoded`` 格式的缓冲区。
为了保证数据格式的正确性，可以调用函数 ``urllib.urlencode()`` 转换。
该函数接收一个字典映射或者二元组，返回一个满足 ``application/x-www-form-urlencoded`` 要求的字符串。
urllib2 模块发送 HTTP/1.1 版本的请求，请求头中带有 *Connection:close* 字段。

参数 timeout 是可选的，指定等待连接的时间，单位是秒，这个过程是阻塞式的。
若没有指定，使用的是全局默认的数值。
这个参数仅对 HTTP, HTTPS 和 FTP 连接起作用。

这个函数返回一个类文件对象，该对象有两个方法：

* geturl()
  
  返回查找到的资源对应的 URL，以便决定是否要重定向。

* info()
  
  返回请求页的元信息，比如头。
  其格式是 ``mimetools.Message``

``urllib2.urlopen()`` 函数抛出 ``URLError`` 异常。

注意如果没有请求解析器，则该函数返回 None。
默认情况下，安装的是全局的 URL 访问器（``OpenerDirector``对象）。
使用的是 ``UnknownHandler`` 解析器，保证不会发生这种情况。

另外，如果设置了代理，则默认安装 ``ProxyHandler`` 解析器来分析请求。

``urllib2.install_opener(opener)``
----------------------------------

安装一个 ``OpenerDirector`` 实例作为默认的全局 URL 访问器。
只有在使用 ``urlopen()`` 函数的情况下，才会自定义一个访问器。
一般情况下，只要用 ``OpenerDirector.open()`` 代替 ``urlopen()`` 即可。
它不会检测是否有 ``OpenerDirector`` 对象，直接通过类对象调用 ``open()`` 即可用。

``urllib2.build_opener([handler,...])``
---------------------------------------

返回一个 ``OpenerDirector`` 实例，将句柄集合 ``[handler,...]`` 顺序连接起来。
句柄集合可以是 ``BaseHandler`` 实例，也可以是 ``BaseHandler`` 的子类。
后一种情况，要求子类的构造函数不带参数。
以下类的实例句柄会自动加入到句柄集合的前面，除非出现在了句柄集合中：

* ``ProxyHandler``
* ``UnknownHandler``
* ``HttpHandler``
* ``HttpDefaultErrorHandler``
* ``HttpRedircetHandler``
* ``FTPHandler``
* ``FileHandler``
* ``HTTPErrorProcessor``
  
如果安装 Python 的时候支持 SSL（即 ``ssl`` 模块可以加载），还会加入 ``HTTPSHandler``。

``urllib2.Request(url, [data][,headers][,origin_req_host][,unverifiable])``
---------------------------------------------------------------------------

.. note:: 这是一个类，参数是构造函数的参数

它是一个抽象类。

url 是一个有效的 URL 字符串。

data 是字符串或者 None，表示传递给服务器的额外数据。
如果数据参数不为 None，则 HTTP 请求将为 POST 方式。
数据参数必须是一个 ``application/x-www-form-urlencoded`` 格式的缓冲区。
为了保证数据格式的正确性，可以调用函数 ``urllib.urlencode()`` 转换。
该函数接收一个字典映射或者二元组，返回一个满足 ``application/x-www-form-urlencoded`` 要求的字符串。

headers 是一个字典，处理时相当于调用 ``add_header()`` 处理每一个键值对。
