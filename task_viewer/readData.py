import datetime
import file

class work_per_hour:
    def __init__(self, date):
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H')
        self.works = []

    def addwork(self, work):
        work_name = work.getname()
        # TODO: workクラス又はaddwork関数で設定ファイルに従い、無題.txt-メモ帳と＊無題.txt-メモ帳などを同じ名前に変換する。
        if work_name not in [r[0] for r in self.works]:
            self.works.append([work_name, work])
        else:
            index = [r[0] for r in self.works].index(work_name)
            self.works[index][1].join(work)
        self.sortworks()

    def getworklist(self):
        return self.works

    def getdate(self):
        return self.date

    def sortworks(self):
        timedelta_list = [[self.works[i][1].getdata()[0], i] for i in range(len(self.works))]
        timedelta_list = sorted(timedelta_list)
        timedelta_list.reverse()
        sort_index = [r[1] for r in timedelta_list]
        new_works = []
        for i in sort_index:
            new_works.append(self.works[i])
        self.works = new_works

class work:
    def __init__(self, name, time, opperation):
        self.name = name
        self.time = time
        self.opperation = opperation

    def join(self, work):
        time, opperation = work.getdata()
        self.time += time
        self.opperation[0] += opperation[0]
        self.opperation[1] += opperation[1]
        self.opperation[2] += opperation[2]

    def getname(self):
        return self.name

    def getdata(self):
        return self.time, self.opperation

class work_per_free(work_per_hour):
    def __init__(self, date):
        super(work_per_free, self).__init__(date)

    def addworkList(self, worklist):
        for i in [r[1] for r in worklist]:
            self.addwork(i)
# TODO: 必要になったらテストを行う


def parseData(filename, password):
    wphList = []
    t = file.read(filename, password)
    cmd = t.split('\n')

    for c in range(int(len(cmd) / 5)):
        name = cmd[c * 5][2:]
        start = datetime.datetime.strptime(cmd[c * 5 + 1][2:], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(cmd[c * 5 + 2][2:], '%Y-%m-%d %H:%M:%S')
        op = list(map(int, cmd[c * 5 + 4].split()[1:]))
        while True:
            start_hour = start.strftime('%Y-%m-%d %H')
            if start_hour not in [r[0] for r in wphList]:
                wphList.append([start_hour, work_per_hour(start_hour)])
                wphList = sorted(wphList)
            index = [r[0] for r in wphList].index(start_hour)
            if start_hour != end.strftime('%Y-%m-%d %H'):
                start_nextHour = datetime.datetime.strptime(start_hour, '%Y-%m-%d %H') + datetime.timedelta(hours=1)
                time = start_nextHour - start
                percentage = time / (end - start)
                # print(percentage, [round(n * (1 - percentage)) for n in op])
                w = work(name, time, [round(n * percentage) for n in op])
                wphList[index][1].addwork(w)
                op = [round(n * (1 - percentage)) for n in op]
                start = start_nextHour
            else:
                time = end - start
                w = work(name, time, op)
                wphList[index][1].addwork(w)
                break

    return wphList

if __name__ == '__main__':
    wphList = []
    password = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'
    t = file.read('../task_checker2/data/applicationLog', password)
    cmd = t.split('\n')
    # samplelist = ['n 無題 - メモ帳', 's 2021-03-10 14:07:10', 'e 2021-03-10 16:07:10', 't 0:00:00.183674', 'o 0 999 2']
    # cmd[2175:2175] = samplelist ←最後尾-1
    # print(cmd)
    for c in range(int(len(cmd) / 5)):
        # print(cmd[c*5:c*5+5])
        name = cmd[c * 5][2:]
        start = datetime.datetime.strptime(cmd[c * 5 + 1][2:], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(cmd[c * 5 + 2][2:], '%Y-%m-%d %H:%M:%S')
        op = list(map(int, cmd[c * 5 + 4].split()[1:]))
        while True:
            # print([r[0] for r in wphList])
            start_hour = start.strftime('%Y-%m-%d %H')
            if start_hour not in [r[0] for r in wphList]:
                wphList.append([start_hour, work_per_hour(start_hour)])
                wphList = sorted(wphList)
            index = [r[0] for r in wphList].index(start_hour)
            if start_hour != end.strftime('%Y-%m-%d %H'):
                start_nextHour = datetime.datetime.strptime(start_hour, '%Y-%m-%d %H') + datetime.timedelta(hours=1)
                time = start_nextHour - start
                percentage = time / (end - start)
                print(percentage, [round(n*(1-percentage)) for n in op])
                w = work(name, time, [round(n*percentage) for n in op])
                wphList[index][1].addwork(w)
                op = [round(n*(1-percentage)) for n in op]
                start = start_nextHour
            else:
                time = end - start
                w = work(name, time, op)
                wphList[index][1].addwork(w)
                break

    for wl in wphList:
        print(wl[0])
        for w in wl[1].getworklist():
            print('  ', w[0], w[1].getdata())

    # プログラム案
    # for i in range(タスクの個数):
    #     y, m, d, h = cmdのstartから年、月、日、時間を抽出
    #     while True:
    #         if wphListにy, m, d, hが同じクラスが存在しない:
    #             wph = work_per_hour(y, m, d, h)
    #             wphList.append(wph)
    #             wphリストのソート
    #         if startとendが違う時間帯:
    #             wphList.get(y,m,d,h).addTime(name, startの次の0分0秒（例：startが12時30分なら13時0分） - start)
    #             (addTime関数内で、work_per_hourクラスに同じ名前のタスクがあれば統合、なければ新規で登録)
    #             start = startの次の0分0秒
    #         else:(startとendが同じ時間帯)
    #             wphList.get(y,m,d,h).addTime(name, end-start)
    #             break
