URL访问的扩展库—— ``urllib2``
=============================

``urllib2`` 模块定义了一些更复杂的函数和类（绝大多数都是 ``HTTP`` 协议）。
主要用于基础和摘要式的身份验证，网页跳转，网页曲奇等等。

``urllib2`` 模块定义了以下函数：

* ``urllib2.urlopen(url, [,data][,timeout])``

  * ``url`` 字符串 / ``Request`` 对象

    .. warning:: HTTPS 请求不做服务器认证确认

  * ``data`` 字符串/ ``None``
  
    传递给服务器的用户数据。
    目前为止，HTTP 请求是唯一用到 ``data`` 的用户请求；
    ``data`` 不为 ``None``，则 HTTP 请求为 ``POST`` 方式。
    ``data`` 必须符合 ``application/x-www-form-urlencoded`` 格式规范。
    可以调用函数 ``urllib.urlencode()`` 做数据格式转换；
    该函数的输入参数为字典或者二元组，返回的是 ``application/x-www-form-urlencoded`` 格式的字符串。
    urllib2 模块支持 HTTP/1.1 版本的请求，请求头中带有 **Connection:close** 字段。

  * ``timeout``
  
    指定连接超时时间(s)，等待连接是阻塞式的；
    若没有指定，使用的是全局默认的数值。

    .. important:: 该参数仅对 HTTP, HTTPS 和 FTP 连接起作用。

    ``urlopen()`` 返回一个仿文件对象，对象有两个方法：

    * geturl()
  
      获取资源 URL，以便决定是否重定向。
      资源 URL 是指含有该资源的网页网址；
      例如请求一幅图片，则 ``geturl()`` 可以获取包含该图片的网页 URL。
  
    * info()
  
      返回请求页的元信息，比如头。
      其格式是 ``mimetools.Message``

   ``urlopen()`` 抛出 ``URLError`` 异常。

   .. note:: 
    如果未指定请求处理器，``urlopen()`` 返回 ``None``。
    全局的 ``OpenerDirector`` 对象，使用 ``UnknownHandler`` 处理器。
    如果请求设置了代理，则代理服务器使用 ``ProxyHandler`` 处理请求。

* ``urllib2.install_opener(opener)``

  使用 ``OpenerDirector`` 实例作为全局的 URL 访问者。

  .. attention:: URL 访问者对象包含请求处理器(``Handler``)。
   只有用 ``urlopen()`` 打开 URL，才需要定义一个访问者。

  一般情况下，可以用 ``<OpenerDirector instance>.open()`` 代替 ``urlopen()``。
  好处是不用显示地指定 URL 访问者。

* ``urllib2.build_opener([handler,...])``

  返回一个 ``OpenerDirector`` 实例，作为 URL 访问者。
  ``[handler,...]`` 用于设置 URL 访问者的请求处理器（访问者按照参数顺序使用处理器处理请求）。
  ``[handler,...]`` 为 ``BaseHandler`` 实例/子类(构造函数不带参数)。

  以下请求处理器自动置于 ``[handler,...]`` 前面（排除出现在 ``[handler,...]`` 中的）：

  * ``ProxyHandler``
  * ``UnknownHandler``
  * ``HttpHandler``
  * ``HttpDefaultErrorHandler``
  * ``HttpRedircetHandler``
  * ``FTPHandler``
  * ``FileHandler``
  * ``HTTPErrorProcessor``
  
  如果安装 Python 的时候支持 SSL（即可以加载 ``ssl`` 模块），还会加入 ``HTTPSHandler``。

* ``urllib2.Request(url, [data][,headers][,origin_req_host][,unverifiable])``

  .. note:: ``urllib2.Request`` 是网络请求的抽象

  * ``url`` 是一个有效的 URL 字符串。
  * ``data`` 字符串/ ``None``

    传递给服务器的用户数据。
    ``data`` 不为 ``None``，则 HTTP 请求为 ``POST`` 方式。
    ``data`` 必须符合 ``application/x-www-form-urlencoded`` 格式规范。
    可以调用函数 ``urllib.urlencode()`` 做数据格式转换；
    该函数的输入参数为字典或者二元组，返回的是 ``application/x-www-form-urlencoded`` 格式的字符串。
    urllib2 模块支持 HTTP/1.1 版本的请求，请求头中带有 ``Connection:close`` 字段。

  * headers 是一个字典
 
    ``urllib2.Request`` 类将每个键值对添加到请求中（类似调用 ``add_header()``)。
    它常用来“糊弄” ``User-Agent`` 头，浏览器通过它识别自身（是否该浏览器发送的请求）；
    某些 HTTP 服务器只接受公共浏览器的请求，拒绝脚本。
    例如，Mozilla 火狐浏览器通过 ``Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 FireFox/2.0.0.11`` 来识别自身；
    ``urllib2`` 默认的 ``User-Agent`` 是 ``Python-urllib/2.6`` (Python 2.6)。

  最后两个参数和三方的 ``HTTP cookies`` 解析有关：

  * ``origin_req_host`` 为原始事物的请求主机（``RFC 2965``）。
    默认为 ``cookielib.request_host(self)``，是由用户请求的主机名或者 IP 地址。
    例如，如果请求的是 HTML 文档中的图片，则该参数是请求目标网页的主机名。

  * ``unverifiable`` 表示请求是否可验证（``RFC 2965``），默认为 ``False``。
    对于一个不可验证的请求对应的 URL，用户是无权决定是否访问的。
    例如，请求 HTML 文档中的图片，用户无权决定是否自动获取该图片，则这个参数设为 ``True``

    .. attention::  许多网页就是这样，不受用户控制，自动弹出。

* ``urllib2.OpenerDirector``

  该类通过多个请求处理器打开多个 URL，管理处理器链表，并从出错状态中恢复。

* ``urllib2.BaseHandler``

  所有注册的请求处理器的基类，它只处理简单的注册请求

* ``urllib2.HttpDefaultErrorHandler``

  定义了 HTTP 错误响应的默认处理器；所有的错误响应都转化为 ``HTTPError`` 异常。

``Request`` 类
--------------

包含以下公有接口，必须在子类中实现：

* ``Request.add_data(data)``
  
  ``data`` 设置请求数据，只有 HTTP 处理器识别。
  ``data`` 是一个字节数组，非 ``None`` 时，请求方式变为 ``POST``。

* ``Request.get_method()``
  
  返回请求方式(``"POST"/"GET"/...``)，仅对 HTTP 请求有意义。

* ``Request.has_data()``
  
  请求中是否含有非空数据

* ``Request.get_data()``
  
  返回请求中的数据

* ``Request.add_header(key,val)``
  
  给请求再添加一个头，仅对 HTTP 处理器有效。
  ``key`` 表示头名称，``val`` 是对应的头的内容。

  .. note:: 头名称不能相同，如果相同，后一次修改会覆盖前一次。

  多次使用的头可以指定一种方式，可以让同一个头对应固定相同的请求方式。

* ``Request.add_unredirected_header(key,header)``
  
  添加一个不进行重定向的请求头

* ``Request.has_header(header)``
  
  请求实例是否含有指定名称的头（检测是否常规头/不可重定向头）

* ``Request.get_full_url()``
  
  返回构造函数给出的 URL

* ``Request.get_type()``
  
  返回 URL 类型，即协议

* ``Request.get_host()``
  
  返回进行连接的主机名

* ``Request.get_selector()``
  
  返回选择子，URL 的一部分

* ``Request.set_proxy(host, type)``
  
  准备发起一个连接代理服务器的请求。
  ``host`` 和 ``type`` 将取代请求实例中的主机和类型，实例选择子是构造函数提供的原始 URL。

* ``Request.get_origin_req_host()``
  
  返回原始事物的请求主机名(``RFC 2965``)。

* ``Request.is_unverifiable()``
  
  该请求是否可验证。

``OpenerDirector`` 类
---------------------

类实例的方法：

* ``OpenerDirector.add_handler(handler)``
  
  ``handler`` 是 ``BaseHandler`` 的实例。
  搜索以下方法，加到可能的操作链中（注意 HTTP 错误是特例）：

  * ``protocol_open()`` 打开协议 URLs
  * ``http_error_type()`` 处理 HTTP 错误码对应的 HTTP 错误信息
  * ``protocol_error()`` 处理（非 http）协议错误
  * ``protocol_request()`` 预处理协议请求
  * ``protocol_response()`` 后处理协议响应

* ``OpenerDirector.open(url[,data][,timeout])``

  参数和异常类型和 ``urlopen()`` 一样（``urlopen()`` 基于全局的 ``OpenerDirector`` 对象调用 ``open()`` 方法）。

* ``OpenerDirector.error(proto[,arg[,...]])``
  
  解决给定协议的一个错误，调用的是注册的错误处理器。
  HTTP 协议是特例，使用 HTTP 响应状态码决定特定的错误处理器。

  返回的值和异常类型和 ``urlopen()`` 一样。

``OpenerDirector`` 对象打开 URLs 分三个过程：

1. 调用所有处理器的 ``protocol_request`` 预处理请求。
2. 调用所有处理器的 ``protocol_open`` 处理请求。
   如果某个处理器返回非 ``None`` 值（响应），或者抛出异常(``URLError``)。
   异常对象允许向下传递。

   事实上，以上算法先尝试 ``default_open()``。
   如果都返回 ``None``，再尝试 ``protocol_open()``。
   如果返回 ``None``，则再尝试 ``unknown_open()``。

   注意这些方法的内部调用 ``OpenerDirector`` 实例的 ``open()`` 和 ``error()``。
3. 处理器调用 ``protocol_response``，用于后处理响应。