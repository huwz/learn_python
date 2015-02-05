URL访问的扩展库—— ``urllib2``
=============================

``urllib2`` 主要用于基础和摘要式的身份验证，网页跳转，网页 cookie 等等。

* ``urllib2.urlopen(url, [,data][,timeout])``

  * ``url``
    
    字符串 / ``Request`` 对象。

    .. warning:: HTTPS 请求不进行服务器认证

  * ``data``
    
    字符串 / ``None``。
  
    传递给服务器的用户数据。
    目前为止，HTTP 请求是唯一用到 ``data`` 参数的用户请求；
    ``data`` 不为 ``None``，则 HTTP 请求为 ``POST`` 方式。
    ``data`` 必须符合 ``application/x-www-form-urlencoded`` 格式规范。
    可以调用函数 ``urllib.urlencode()`` 做数据格式转换；
    该函数的输入参数为字典或者二元组，返回的是 ``application/x-www-form-urlencoded`` 格式的字符串。
    urllib2 模块支持 HTTP/1.1 版本的请求，请求头中带有 **Connection:close** 字段。

  * ``timeout``
  
    指定连接超时时间(s)，等待连接是阻塞式的；
    若没有指定，使用的是全局默认的数值。

    .. important:: 该参数仅对 HTTP, HTTPS 和 FTP 连接起作用。

  * 返回值
  
    .. note:: 
     未设置请求处理器，``urlopen()`` 返回 ``None``；
     设置了全局的访问器(``OpenerDirector``)，则使用 ``UnknownHandler`` 处理器；
  
    仿文件对象，该对象增加两个方法：

    * geturl()
  
      获取资源 URL，以便决定是否重定向。
      资源 URL 是指含有该资源的网页网址；
      例如请求一幅图片，则 ``geturl()`` 可以获取包含该图片的网页 URL。

    * info()
  
      返回请求页的元信息，比如头。
      其格式是 ``mimetools.Message``
  
  * 异常
    
    ``URLError``

* ``urllib2.install_opener(opener)``

  设置全局的访问器。

  .. note:: 
   用 ``<OpenerDirector instance>.open()`` 代替 ``urlopen()``，可以不用设置全局访问器。

* ``urllib2.build_opener([handler,...])``

  构建一个访问器。

  ``handler,...`` 设置处理器列表，访问器使用处理器处理请求；
  ``handler,...`` 是 ``BaseHandler`` 的实例/不带参数的子类。

  以下处理器将自动排在 ``handler,...`` 前面（出现在 ``handler,...`` 中的除外）：

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

  .. note:: 请求类

  * ``url``
    
    URL 字符串。

  * ``data``
    
    字符串 / ``None``

    传递给服务器的用户数据。
    ``data`` 不为 ``None``，则 HTTP 请求为 ``POST`` 方式。
    ``data`` 必须符合 ``application/x-www-form-urlencoded`` 格式规范。
    可以调用函数 ``urllib.urlencode()`` 做数据格式转换；
    该函数的输入参数为字典或者二元组，返回的是 ``application/x-www-form-urlencoded`` 格式的字符串。

    urllib2 模块支持 HTTP/1.1 版本的请求，请求头中带有 ``Connection:close`` 字段。

  * headers
    
    字典。
 
    相当于调用 ``add_header()`` 以添加多个请求头，常常用于指定 ``User-Agent`` 请求头。
    某些 HTTP 服务器只接受公共浏览器的请求，拒绝脚本。

    例如，Mozilla 火狐浏览器的 ``User-Agent`` 为 ``Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 FireFox/2.0.0.11``；
    ``urllib2`` 的 ``User-Agent`` 默认为 ``Python-urllib/*.*``。

  最后两个参数和三方的 ``HTTP cookies`` 解析有关：

  * ``origin_req_host`` 为原始事物的请求主机（``RFC 2965``）。
    默认为 ``cookielib.request_host(self)``，是由用户请求的主机名或者 IP 地址。
    例如，如果请求的是 HTML 文档中的图片，则该参数是请求目标网页的主机名。

  * ``unverifiable`` 表示请求是否可验证（``RFC 2965``），默认为 ``False``。
    对于一个不可验证的请求对应的 URL，用户是无权决定是否访问的。
    例如，请求 HTML 文档中的图片，用户无权决定是否自动获取该图片，则这个参数设为 ``True``

    .. attention::  许多网页就是这样，不受用户控制，自动弹出。

``Request`` 实例
----------------

包含以下公有接口：

* ``add_data(data)``
* ``get_method()`` ``"POST"/"GET"/...``，仅对 HTTP 请求有意义。
* ``has_data()``
* ``get_data()``
* ``add_header(key,val)``
  
  给请求再添加一个头，仅对 HTTP 处理器有效。
  ``key`` 表示头名称，``val`` 是对应的头的内容。

  .. note:: 头名称不能相同，如果相同，后一次修改会覆盖前一次。

* ``add_unredirected_header(key,header)`` 添加一个不进行重定向的请求头
* ``has_header(header)`` 请求实例是否含有指定名称的头（检测是否常规头/不可重定向头）
* ``get_full_url()`` 构造函数提供的 URL
* ``get_type()`` 返回协议类型
* ``get_host()`` 返回主机名
* ``get_selector()`` 获取 URL 选择子
* ``set_proxy(host, type)`` 设置一个代理服务器。
  
  .. note::
   ``host`` 覆盖 ``get_host()`` 的返回值；
   ``type`` 覆盖 ``get_type()`` 的返回值；
   选择子是 ``get_full_url()`` 的返回值。

* ``get_origin_req_host()`` 返回原始主机名(``RFC 2965``)。
* ``is_unverifiable()`` 请求是否可验证。

``OpenerDirector`` 实例
-----------------------

* ``add_handler(handler)``
  
  增加一个处理器。
  
  处理器将添加以下操作序列：

  * ``protocol_open()`` 打开协议 URLs；
  * ``http_error_type()`` 处理 HTTP 错误对应的错误类型；
  * ``protocol_error()`` 处理协议错误（HTTP 处理器会忽略该函数）；
  * ``protocol_request()`` 预处理协议请求；
  * ``protocol_response()`` 后处理协议响应；

* ``open(url[,data][,timeout])``
  
  .. note:: 和 ``urlopen()`` 一样，不同的是，本函数使用局部访问器

* ``error(proto[,arg[,...]])``
  
  ``proto`` 指定协议类型；
  
  用协议指定的错误处理器处理当前协议错误。
  返回一个收集错误信息的仿文件对象。

  .. note:: 
   HTTP 协议使用响应状态码指定错误处理器。

``OpenerDirector`` 实例打开 URL 的步骤：

1. 调用所有处理器的 ``protocol_request`` 预处理请求。
2. 调用所有处理器的 ``protocol_open`` 处理请求。
   如果某个处理器返回非 ``None`` 值（响应），或者抛出异常(``URLError``)。
   异常对象允许向下传递。

   事实上，以上算法先尝试 ``default_open()``。
   如果都返回 ``None``，再尝试 ``protocol_open()``。
   如果返回 ``None``，则再尝试 ``unknown_open()``。

   注意这些方法的内部调用 ``OpenerDirector`` 实例的 ``open()`` 和 ``error()``。
3. 处理器调用 ``protocol_response``，用于后处理响应。