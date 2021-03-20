import os
import datetime

import file

class fileOperator:
    def __init__(self):
        self.password = 'OiC&0~ktz1%i4nUg1ZodLM+XUPf(f|E9ez_vys9p'
        self.operatorfilename = '../data/operator.txt'
        if os.path.exists(self.operatorfilename) is False:
            with open(self.operatorfilename, mode='w') as f:
                f.write('../data/log_1 ' + datetime.datetime.now().strftime("%Y-%m-%d-%H") + ' ')
            with open('../data/log_1', mode='wb') as f:
                pass
            pass
        self.logfile = self._readoparator(self.operatorfilename)

    def _readoparator(self, operatorfilename):
        logfile = []
        with open(operatorfilename, mode='r') as f:
            for line in f:
                d = line.split(' ')
                d[1] = datetime.datetime.strptime(d[1], '%Y-%m-%d-%H')
                if len(d[2]) == 0:
                    d[2] = d[1]
                else:
                    d[2] = datetime.datetime.strptime(d[2], '%Y-%m-%d-%H\n')
                logfile.append(d)
        return logfile

    def getlogfile(self):
        return self.logfile

    def _makenewlog(self, start):
        newfilename = '../data/log_' + str(len(self.logfile)+1)
        with open(newfilename, mode='wb') as f:
            pass
        latestfilename = self.logfile[-1][0]
        t = file.read(latestfilename, self.password).split('\n')
        end = datetime.datetime.strptime(t[-4][2:], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H')
        with open(self.operatorfilename, mode='a') as f:
            f.write(end + '\n' + newfilename + ' ' + start.strftime('%Y-%m-%d-%H') + ' ')
        self.logfile = self._readoparator(self.operatorfilename)

    def readlogfile(self, date):
        # １，datetime型のdateをfor lf in logfile : lf[1]と比較する
        # ２，初めてlf[i]<=dateになったlfを読み出す
        # ３，読み出したデータを返す
        pass

    def addlog(self, data):
        filetext = ''
        if os.path.getsize(self.logfile[-1][0]) > 16:
            filetext = file.read(self.logfile[-1][0], self.password)
        print(filetext)
        if len(filetext) >= 300000:
            print(data.split('\n')[1][2:])
            self._makenewlog(datetime.datetime.strptime(data.split('\n')[1][2:], '%Y-%m-%d %H:%M:%S'))
            filetext = ''
        file.write(self.logfile[-1][0], self.password, filetext+data)


if __name__ == '__main__':
    fo = fileOperator()
    # print(fo.getlogfile())
    fo.addlog("n test\ns 2021-03-21 12:00:00\ne 2021-03-21 14:23:45\nt\no\n")
    # print(fo.getlogfile())







