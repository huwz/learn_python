URL访问的扩展库—— ``urllib2``
=============================

``urllib2`` 主要用于基础和摘要式的身份验证，网页跳转，网页 cookie 等等。

* ``urllib2.urlopen(url, [,data][,timeout])``

  * ``url``
    
    字符串 / ``Request`` 对象。

    .. warning:: HTTPS 请求不进行服务器认证

  * ``data``
    
    取值为字符串或者 ``None``，定义传递给服务器的用户数据。

    .. important:: 
     目前为止，HTTP 请求是唯一用到 ``data`` 参数的用户请求；

    ``data`` 不为 ``None`` 时，HTTP 请求为 ``POST`` 方式。
    ``data`` 必须符合 ``application/x-www-form-urlencoded`` 格式规范。
    例如：``name='hwz'&region='beijing'``

    可以调用函数 ``urllib.urlencode()`` 做数据格式转换：

    .. code-block:: python
     :linenos:

     import urllib

     dic = {"name":"hwz", "region":"beijing"}
     encoded_data = urllib.urlencode(dic)
     print encoded_data # 'region=beijing&name=hwz'
    
    ``urllib.urlencode()`` 的输入参数为字典或者二元组序列，返回的是 ``application/x-www-form-urlencoded`` 格式的字符串。
    urllib2 模块支持 HTTP/1.1 版本的请求，请求头中带有 **Connection:close** 键值。

  * ``timeout``
  
    指定连接超时时间(s)，等待连接是阻塞式的；
    若没有指定，使用的是全局默认的数值。

    .. important:: 该参数仅对 HTTP, HTTPS 和 FTP 连接起作用。

  * 返回值
    
    返回一个仿文件对象，指向的是服务器的响应消息。

    .. note::
     服务器的 HTTP 响应消息，包括响应头（元信息）和响应体（也就是数据资源）。
     响应体可以是 ``text/html`` 文档，也就是浏览器中的网页的源代码；
     也可以是图片资源，还可以是二进制的数据，或者 ``application/json`` 字符串等等。

    返回对象除了常规文件读写方法之外，还提供两个额外的方法：

    * geturl()
  
      获取服务器返回的资源对应的 URL；URL 指含有该资源的网址；
      比如网页资源，则返回该网页的 URL：

      .. code-block:: python
       :linenos:

       response = urllib2.open('http://www.baidu.com')
       print response.geturl() # 'http://www.baidu.com'

    * info()
  
      返回服务器响应的元信息，比如响应头信息。
      其格式是 ``mimetools.Message``。
      
      可以通过键名获取响应头信息，比如：

      .. code-block:: python
       :linenos:

       response = urllib2.open('http://www.baidu.com')
       meta_data = response.info()
       print meta_data.getheaders('Content-Type') # ['text/html; charset=utg-8']
  
  * 异常
    
    ``URLError``

* ``urllib2.install_opener(opener)``

  手动安装全局访问器。

  .. important:: 
    
    系统默认安装的全局访问器，使用 ``UnknownHandler`` 请求处理器；
    如果设置了 ``*_proxy`` 环境变量(例如 ``set http_proxy=*``)，全局访问器使用的 ``ProxyHandler``。

    用 ``<OpenerDirector instance>.open()`` 代替 ``urlopen()``，可以不用安装全局访问器。

* ``urllib2.build_opener([handler,...])``

  返回一个访问器对象。

  访问器内部设置了请求处理器列表，可以通过 ``handler,...`` 手动设置处理列表。

  ``handler,...`` 是 ``BaseHandler`` 的实例/不带参数的子类。

  以下请求处理器将自动排在 ``handler,...`` 前面（出现在 ``handler,...`` 中的除外）：

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
    
    与 ``urllib2.urlopen()`` 的 ``data`` 参数说明一致

  * ``headers``
 
    ``headers`` 是一个字典。

    对于 ``headers`` 的处理，相当于调用 ``add_header()``；
    表示给请求头添加新的键值对，比如指定 ``User-Agent`` 键值对。

    .. note::
     服务器可以利用 ``User-Agent`` 字段过滤请求。
     例如，Mozilla 火狐浏览器的 ``User-Agent`` 为 ``Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 FireFox/2.0.0.11``；
     而 ``urllib2`` 的 ``User-Agent`` 默认为 ``Python-urllib/*.*``。
     如果某个服务器只接受 ``User-Agent`` 为 ``Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 FireFox/2.0.0.11`` 的请求，
     则使用 ``urllib2`` 的脚本发起的网络请求会被过滤掉。

     这样做的好处是可以让服务器只接受来自浏览器的请求，而不是脚本发起的请求。
     当然这种限制也不是绝对的，可以手动修改 ``User-Agent`` 键值达到目的。
     因此，Python 文档用了 ``spoof`` 这个词（“糊弄” ``User-Agent``）。

  最后两个参数和三方的 ``HTTP cookies`` 解析有关：

  * ``origin_req_host`` 
    
    默认为 ``cookielib.request_host(self)``，表示请求指定的服务器主机名或者 IP 地址。
    例如，如果请求的是 HTML 文档，则该参数是目标网页的主机名：

    .. code-block:: python
     :linenos:

     import urllib2, cookielib
     request = urllib2.Request('http://www.baidu.com')
     host_name = cookielib.request_host(request) # 'www.baidu.com'

  * ``unverifiable`` 表示请求是否可验证（``RFC 2965``），默认为 ``False``。
    对于一个不可验证的请求对应的 URL，用户是无权决定是否访问的。
    例如，请求 HTML 文档中的图片，用户无权决定是否自动获取该图片，则这个参数设为 ``True``

    .. attention::  许多网页就是这样，不受用户控制，自动弹出。

``Request`` 实例
----------------

包含以下公有方法：

* ``add_data(data)``
* ``get_method()`` ``"POST"/"GET"/...``，仅对 HTTP 请求有意义。
* ``has_data()``
* ``get_data()``
* ``add_header(key,val)``
  
  给请求头添加新的键值对，只有 HTTP 处理器会受理这些键值对。

  .. note:: 键名不能相同，如果相同，则后一次的键值会覆盖前一次的键值。

* ``add_unredirected_header(key,header)`` 添加一个键值对；如果需要做重定向，该键值对不会加入到重定向请求头中
* ``has_header(header)`` 请求头中是否含有指定键值对
* ``get_full_url()`` 返回构造函数提供的 URL
* ``get_type()`` 返回协议类型
* ``get_host()`` 返回主机名
* ``get_selector()`` 获取 URL 选择子
* ``set_proxy(host, type)`` 设置一个代理服务器，表示将生成一个代理请求实例。
  
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

``OpenerDirector`` 实例打开 URL 的几个阶段：

1. 调用所有处理器的 ``protocol_request``，预处理请求。
2. 调用所有处理器的 ``protocol_open``，解析请求。
   
   如果某个处理器返回非 ``None`` 值（即服务器响应），或者抛出异常(通常为 ``URLError``)，这个阶段结束。
   发生的异常允许继续传递。

   事实上，以上算法先尝试 ``default_open()``；
   如果都返回 ``None``，再尝试 ``protocol_open()``；
   如果返回 ``None``，则再尝试 ``unknown_open()``。

3. 处理器调用 ``protocol_response``，用于后处理响应。
   
``BaseHandler`` 实例
--------------------

``BaseHandler`` 实例提供两个基础方法，可以直接调用：

* ``add_parent(director)`` 添加一个访问器
* ``close()`` 删除所有访问器

.. important::
 以下属性和方法只能在派生类中实现或使用：

* parent 指定的 ``OpenerDirector`` 实例
* default_open(req)
  
  派生类如果想获取所有的 URL，必须实现这个方法。
  
  派生类如果实现了这个方法，则会被 ``add_parent()`` 指定的访问器对象调用。
  它返回一个仿文件对象（如果没有访问器，则返回 ``None``）。

  抛出异常 ``URLError``。	

  .. important::
   该方法在所有打开方法(``*_open()``)之前调用

* protocol_open(req)
  
  .. note:: 该方法的名称依据协议来定；
   之后凡是 ``protocol_`` 开头的方法都是跟随协议名称的，不再复述。

   比如：
   HTTP 协议的打开方法为 ``http_open()``；
   ftp 协议的打开方法为 ``ftp_open()`` 等。
  
  派生类如果想用指定的协议解析 URL，必须实现这个方法。

  派生类如果实现了这个方法，则会被 ``add_parent()`` 指定的访问器对象调用。
  它返回一个仿文件对象（如果没有访问器，则返回 ``None``）。

* ``unknown_open(req)``
  
  派生类如果想不用任何处理器获取所有的 URL，必须实现这个方法。

  参数说明和返回值以及异常类型和 ``protocol_open()`` 一样。

* http_error_default(req, fp, code, msg, hdrs)
  
  派生类如果想捕获所有 HTTP 错误码，必须实现这个方法。
  
  派生类如果实现了这个方法，则会被 ``add_parent()`` 指定的访问器对象调用。

  .. warning:: 用户不能调用这个方法

  * ``req`` ``Request`` 实例
  * ``fp`` 仿文件对象，指向 HTTP 错误消息体
  * ``code`` 三个数字表示的错误码
  * ``msg`` 用户可见的错误码的解释文字
  * ``hdrs`` 一个字典对象，表示错误头的键值对
  
  返回值与异常类型和 ``urlopen()`` 相同。

* ``http_error_nnn(req, fp, code, msg, hdrs)``
  
  派生类如果想捕获 HTTP 错误码 ``nnn``，必须实现这个方法。
  
  派生类如果实现了这个方法，发生错误码 ``nnn`` 时，``add_parent()`` 指定的访问器对象会自动调用对应的 ``http_error_nnn()`` 方法。

  参数说明和返回值以及异常类型和 ``http_error_default()`` 一样。

* ``protocol_request(req)``
  
  如果派生类想要预处理指定协议的请求实例，必须实现这个方法。
  
  派生类如果实现了这个方法，则会被 ``add_parent()`` 指定的访问器对象调用。
  
  ``req`` 是预处理前的 ``Request`` 实例，返回的是预处理后的 ``Request`` 实例。

* ``protocol_response(req, response)``
  
  派生类如果想后处理指定协议的服务器响应，必须实现这个方法。

  派生类如果实现了这个方法，则会被 ``add_parent()`` 指定的访问器对象调用。

  * ``req`` 是一个 ``Request`` 实例
  * ``response`` 有和 ``urlopen()`` 返回的对象一样的方法。

``HTTPRedircetHandler`` 实例
----------------------------

* ``redirect_request(req, fp, code, msg, hdrs, newurl)``

  返回一个 ``Request`` 实例或者 ``None``。

  如果服务器返回一个重定向的响应(即错误响应消息 ``301`` ``302`` 等等），
  则在方法 ``http_error_30*()`` 中自动调用 ``redirect_request()`` 方法。
  然后用生成的请求实例发出新的网络请求，以重定向到新的 URL。
  如果没有处理器可以解析新的 URL，则抛出 ``HTTPError`` 异常；
  如果 ``HTTPRedircetHandler`` 不能解析新的 URL，但存在其他处理器可以解析，则返回 ``None``。

* ``http_error_301(req, fq, code, msg, hdrs)``
  
  当服务器返回 ``moved permanently`` 消息时，``add_parent()`` 指定的访问器会调用 ``http_error_301()``。

* ``http_error_302(req, fp, code, msg, hdrs)``
  
  当服务器返回 ``found`` 消息时，``add_parent()`` 指定的访问器会调用 ``http_error_301()``。

* ``http_error_303(req, fp,code, msg, hdrs)``
  
  当服务器返回 ``see other`` 消息时，``add_parent()`` 指定的访问器会调用 ``http_error_301()``。

* ``http_error_307(req, fp, code, msg, hdrs)``
   
   当服务器返回 ``temporary redirect`` 消息时，``add_parent()`` 指定的访问器会调用 ``http_error_301()``。
