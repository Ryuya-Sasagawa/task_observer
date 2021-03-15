# TODO: ・念を引数に、その年がうるう年かどうかをTFで返す
#  ・年月を引数にして、その月の末日を返す
#  ・(基準として、2020/1/1 0:00:00のfloat値を保持しておき、)
#  年月日時を引数にして上記のfloat値に従って引数をfloat値に変換して返す

from typing import Final

DATESTANDARD:Final[float] = 18262 # 2020/1/1 0:00:00

def isleapyear(y):
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                return True
            return False
        return True
    return False

def lastdate(y, m):
    leap = isleapyear(y)
    feb = 28
    if leap is True:
        feb = 29

    lastDate = {1:31, 2:feb, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    return lastDate[m]

def datetimeToFloat(date='2020-01-01 0'):
    y,m,d = date.split('-')
    d,h = d.split(' ')
    y = int(y)
    m = int(m)
    d = int(d)
    h = int(h)
    # print(y, m ,d, h)
    ans = DATESTANDARD
    for i in range(2020, y):
        if isleapyear(i) is True:
            ans += 366
        else:
            ans += 365

    for i in range(1,m):
        ans += lastdate(y, i)

    ans += d-1
    ans += h/24
    return ans

# if __name__ == '__main__':
#     ans = datetimeToFloat('2021-03-10 13')
#     print(ans)
