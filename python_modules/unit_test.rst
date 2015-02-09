``unittest``
============

.. code-block:: python
 :linenos:

 import unittest

 class TestAdd(unittest.TestCase):
     def setUp(self):
         print 'hello'
     def tearDown(self):
         print 'world'
     def test_add(self):
         self.assertEqual(3, 12)
     def test_sub(self):
         self.assertEqual(4, 4)
	
 if __name__ == '__main__':
     unittest.main()

在执行每个测试案例之前，都是执行 ``setUp()``；
案例运行结束之后，都会执行 ``tearDown()``。
以上的案例会运行两次 ``setUp()`` 和两次 ``tearDown()``

可以定义类函数 ``setupClass()`` 和 ``tearDownClass()``：

.. code-block:: python
 :linenos:

 @classmethod
 def setupClass(cls):
     <code here>

 @classmethod
 def tearDownClass(cls):
     <code here>

所有测试案例执行之前执行一次 ``setupClass()``；
所有测试案例执行之后执行一次 ``tearDownClass()``。

.. note::
 测试类中以 ``test_`` 开始的类方法都是一个测试案例。
