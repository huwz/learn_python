BaseHTTPServer
==============

.. note::
 本模块针对的是 HTTP 协议。

``BaseHTTPServer`` 模块定义了两个类，用于构造 HTTP  服务器。
通常这两个类不直接拿来使用，而作为基类进行派生。

* ``BaseHTTPServer.HTTPServer(server_address, RequestHandlerClass)``
  
  ``SocketServer.TCPServer`` 的子类，实现了 ``SocketServer.BaseServer`` 的接口。

  ``HTTPServer`` 创建和监听 ``HTTP socket``，分发请求给处理器。

  创建和运行服务器的代码示例：

  .. code-block:: python
   :linenos:

   def run(server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
       server_address = ('', 3000)
       httpd = server_class(server_address, handler_class)
       httpd.server_forever()

  构造函数参数说明：

  * server_address 二元组 ``(server_name, server-port)``；
    如果 ``server_name`` 是 ''，表示服务器为本主机。
  * RequestHandlerClass 请求处理器类名，可以传递 ``BaseHTTPServer.BaseHTTPRequestHandler``。
    
* ``BaseHTTPServer.BaseHTTPRequestHandler``
  
  定义处理器对象，用于解析服务器接收的 HTTP 请求。
  它的实例不参与解析 HTTP 请求，一般是通过它的子类实例来完成。

  处理器解析请求和头信息之后，调用与请求类型对应的方法。
  例如：请求类型为 ``SPAM``，则对应的方法为 ``do_SPAM()``。
  该方法不带任何参数。
  
  .. important::
   ``BaseHTTPServer.BaseHTTPRequestHandler`` 的子类不需要修改 ``__init__()`` 方法。

``BaseHTTPRequestHandler`` 的实例变量
-------------------------------------

* ``client_address`` 是一个二元组 ``(host, port)``，表示客户端主机地址
* ``server`` 服务器实例
* ``command`` 请求类型，如 ``GET``
* ``path`` 请求路径
* ``request_version`` 请求的协议版本，例如：``HTTP/1.0``
* ``headers``
    
  类变量 :ref:`MessageClass<message_class>`` 的值是一个类对象。
  ``headers`` 就是这个类对象的实例，用于解析和管理 HTTP 请求头。

* ``rfile`` 输入流，指向用户请求中附带数据的起始位置
* ``wfile`` 输出流，指向服务器响应数据的起始位置，返回给客户端

``BaseHTTPRequestHandler`` 的类变量
-----------------------------------

* ``server_version``
    
  表示服务器软件版本，可以修改它的值；
  ``server_version`` 由多个字符串构成，字符串之间以空格隔开。
  每个字符串的格式：``<name>[/<version>]``，例如：``BaseHTTP/0.2``

* ``sys_version``
    
  表示 Python 系统版本，采取 ``server_version`` 或者 ``version_string()`` 支持的格式。如 ``Python/1.4``。

* ``error_message_format``
    
  指定一个格式化字符串，用于构建错误响应消息，发送给客户端。

  其格式为：``{code:(message, explain)}``。

  ``code`` 是整数，表示 HTTP 错误码；``message`` 为错误简略信息，``explain`` 为错误详细解释。

  默认的 ``message`` 和 ``explain`` 可以从类变量 ``responses`` 中获取。

* ``error_content_type``
    
  指定服务器错误响应头的 ``Content-Type`` 值。
  默认值为 ``text/html``。

* ``protocol_version``
    
  定义服务器响应的 HTTP 协议版本。
  如果设为 ``HTTP/1.1``，则服务器允许 HTTP 长连接；
  服务器所有响应的 HTTP 头必须设置准确的 ``Content-Length`` （``send_header()``）。
  出于后向兼容的考虑，默认版本为 ``HTTP/1.0``。

.. _message_class:

* ``MessageClass``
     
  表示仿 ``rfc822.Message`` 类，用于解析 HTTP 头。
  默认值为 ``mimetools.Message``，子类一般不会修改它。

* ``resposnes``
    
  ``{code:(shormessage, longmessage)}``

  它是一个字典，表示错误码到 ``(短信息, 长信息)`` 的映射。

``BaseHTTPRequestHandler`` 的方法
---------------------------------

* ``handle()``
  
  处理接收的 HTTP 请求，会调用一次 ``handle_one_request()`` ，启动长连接之后，会调用多次。
  子类不用修改它；只要实现合适的 ``do_*()`` 方法即可。

* ``handle_one_request()``
  
  解析和分发请求到合适的 ``do_*()`` 方法中。
  子类不用修改它。

* ``send_error(code[,message])``
  
  发送错误码和错误信息给客户端。
  ``code`` 表示 HTTP 错误码；
  ``message`` 是可选的。

  发完头信息之后，发送错误信息文本（由 ``error_message_format`` 构建）。

* ``send_response(code[,message])``
  
  发送响应头和响应日志。
  发送完 HTTP 响应行之后，发送服务器头和数据头。
  可以分别通过方法 ``version_string()`` 和 ``data_time_string()`` 获取。

* ``send_header(keyword, value)``
  
  给输出流的 HTTP 头增加一个键值对。

* ``end_headers()``
  
  给输出流的 HTTP 头增加一个空白行，表示结束

* ``log_request([code][,size])``
  
  成功接收请求时，打印日志。

  ``code`` 为 HTTP 响应状态码；
  ``size`` 表示响应消息体的长度。

* ``log_error(...)``
  
  不能完成请求时，打印错误日志。
  默认情况下，将信息传递给 ``log_message()``。

* ``log_message(format, ...)``
  
  将任意信息发送给 ``sys.stderr``。

  每个打印消息都会在前面加上客户端的 ip 地址，当前日期和时间。

* ``version_string()``
  
  返回服务器软件版本字符串；
  由 ``server_version`` 和 ``sys_version`` 组合而成。

* ``data_time_string([timestamp])``
  
  返回指定时间戳(``time.time()``)的日期和时间；用于消息头。

  如果参数 ``timestamp`` 省略，则使用当前日期和时间。

  其格式类似于：``Sun, 08, Feb 2015 23:09:30 GMT``

* ``log_data_time_string()``
  
  返回当前日期和时间，用于日志打印。

* ``address_string()``
  
  返回客户端的地址，用于日志打印。
  主机名称通过客户端 IP 地址查找。

.. note:: ``log_message()`` 内部调用 ``log_data_time_string()`` 和 ``address_string()`` 方法