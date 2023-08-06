# assert 1,0  #等同于 assert (1,0)  这是个元组  元组不为空 就是真 所以这里是真 -->不对 也不能这么写
# assert ()  AssertionError 断言语句失败
# assert 0  #AssertionError 断言语句失败
# assert 1 == 1
# assert 时间_到文本(), '2020年11月21日'

# assert dic == {'a': 1, 'b': 2, 'c': 1234567890}
# assert dic != {'a': 1, 'b': 2}

# with pytest.raises(AssertionError):
#     assert dic == {'a': 1, 'b': 2, 'c': 3}


def test_func():  # 行首 要空2格 否则代码检查器会报错
    print('\n')
    dic = {'a': 1, 'b': 2}
    print(dic)
    assert dic != {'a': 1, 'b': 2, 'c': 1234567890}
    assert dic == {'a': 1, 'b': 2}
    assert dic != {}
    # with pytest.raises(AssertionError):
    #     assert dic == {'a': 1, 'b': 2, 'c': 3}
