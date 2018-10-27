"""
closures application
cpython how to implement closures please ref: http://www.wklken.me/posts/2015/09/04/python-source-closure.html

def index():
    pass
index.__closure__
index.__globals__
"""
import datetime
import time
from functools import wraps
import unittest
import copy


class empty:
    pass


class cache(object):
    def __init__(self, max_age=5, decorate_method=False):
        """
        :param max_age: cache expired age
        :param decorate_method: cache class method， whether instance is component of identified key or not
        """
        self.max_age = max_age
        self.decorate_method = decorate_method
        self.memorize = {}
        self.data_template = {'data': empty, 'expired_time': None}

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            if self.decorate_method:
                # self_ = args[0]
                identified_key = str(args[1:])+str(kwargs)
            else:
                identified_key = str(args)+str(kwargs)
            val = self.memorize.get(identified_key, self.data_template)
            if val['expired_time'] and val['expired_time'] > datetime.datetime.now():
                ret = val['data']
            else:
                ret = func(*args, **kwargs)
                val = copy.deepcopy(self.data_template)
                val['data'] = ret
                val['expired_time'] = datetime.datetime.now()+datetime.timedelta(seconds=self.max_age)
                self.memorize[identified_key] = val
            return ret
        return inner


class CacheTestCase(unittest.TestCase):
    def test_decorate_func(self):
        count = {'count': 0}
        @cache(2)
        def incr(name, sex):
            count['count'] += 1
            return name, sex
        # test cache
        ret = incr('zhangchi', 'nan')
        self.assertEqual(ret, ('zhangchi', 'nan'))
        self.assertEqual(count['count'], 1)
        ret = incr('zhangchi', 'nan')
        self.assertEqual(count['count'], 1)
        # test expired
        time.sleep(3)
        ret = incr('zhangchi', 'nan')
        self.assertEqual(count['count'], 2)

    def test_decorator_method_one_instance(self):
        count = {'count': 0}
        class A(object):
            @cache(2)
            def index(self, name, sex):
                count['count'] += 1
                return name, sex
        a = A()
        incr = a.index
        # test cache
        ret = incr('zhangchi', 'nan')
        self.assertEqual(ret, ('zhangchi', 'nan'))
        self.assertEqual(count['count'], 1)
        ret = incr('zhangchi', 'nan')
        self.assertEqual(count['count'], 1)
        # test expired
        time.sleep(3)
        ret = incr('zhangchi', 'nan')
        self.assertEqual(count['count'], 2)

    def test_decorator_method_mult_instance(self):
        count = {'count': 0}
        class A(object):
            @cache(2, decorate_method=True)
            def index(self, name, sex):
                count['count'] += 1
                return name, sex
        incr1 = A().index
        incr2 = A().index
        # test cache
        ret = incr1('zhangchi', 'nan')
        self.assertEqual(ret, ('zhangchi', 'nan'))
        self.assertEqual(count['count'], 1)
        ret = incr2('zhangchi', 'nan')
        self.assertEqual(count['count'], 1)
        # test expired
        time.sleep(3)
        ret = incr1('zhangchi', 'nan')
        self.assertEqual(count['count'], 2)



def main():
    unittest.main()


if __name__ == '__main__':
    main()









