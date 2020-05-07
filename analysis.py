import pandas as pd
import numpy as np



class analysis():
    def __init__(self, f):
        self.cp = "('Crash Point',)"
        self.cl = 'consec_loss'
        self.cw = 'consec_wins'
        self.file = f
        self.loss = 0
        self.wins = 0
        self.df = pd.DataFrame()
        self.groupedLoss = None
        self.countLoss = None
        self.countWins = None
        self.optimal = pd.DataFrame()

    def main(self, curr, max_cash_out):
        if (self.df.empty):
            self.df = self.prepData(max_cash_out)
            self.groupedLoss = self.df.groupby(self.cl)
            self.countLoss = self.groupedLoss.agg("count")
            self.countLoss = self.countLoss.drop(self.countLoss.columns[[1,2,3]], axis=1)
            self.groupedWins = self.df.groupby(self.cw)
            self.countWins= self.groupedWins.agg("count")
            self.countWins = self.countWins.drop(self.countWins.columns[[1,2,3]], axis=1)
            self.optimalBets(max_cash_out)

        if (curr < max_cash_out):
            self.loss += 1
            self.wins = 0
        else:
            self.loss = 0
            self.wins += 1


        print("----CL: " + str(self.loss))
        print("----CW: " + str(self.wins))
        if(self.wins == 0):
            a = self.optimal[self.optimal['loss'] == self.loss]
            print("Best cash out point " + str(a.loc[a['loss_profit'].idxmax(), 'cash_out_loss']) + " at profit of " + str(max(a['loss_profit'])))
        else:
            a = self.optimal[self.optimal['win'] == self.wins]
            print("Best cash out point " + str(a.loc[a['win_profit'].idxmax(), 'cash_out_win']) + " at profit of " + str(max(a['win_profit'])))
        print("_________________________________________________________")
        #breakEven(cp)

    def prepData(self, cash_out):
        df = pd.read_csv(self.file)
        a = df[self.cp].str.rstrip("x")
        df[self.cp] = a.astype(float)
        df[self.cl] = 0
        df[self.cw] = 0
        for i in range(len(df[self.cp])):
            if df[self.cp][i] < cash_out:
                self.loss += 1
                self.wins = 0
            else:
                self.loss = 0
                self.wins += 1
            df[self.cl][i] = self.loss
            df[self.cw][i] = self.wins
        return df

    def stats(self, column):
        print("Median: "+ str(np.median(column)))
# Checks if there's a point where you make money regularly
    def breakEven(column):
        for i in range(1, 101):
            bet = 10
            diff = (bet * (i/100) * np.percentile(column, i)) - ((1 - (i/100)) * bet)
            if (diff > bet):
                print("Percentile " + str(i) + " is: " + str(np.percentile(column, i)))

    def optimalBets(self, point=2):
        cash = 1
        index = 0
        self.optimal = pd.DataFrame(index=range(2000))
        self.optimal['cash_out_loss'] = 0.0
        self.optimal['loss'] = 0
        self.optimal['loss_profit'] = 0.0
        self.optimal['cash_out_win'] = 0.0
        self.optimal['win'] = 0
        self.optimal['win_profit'] = 0.0
        while cash <= point:
            for i in range(1, len(self.countLoss)-1):
                perc = self.countLoss["Unnamed: 0.1"][i+1] / self.countLoss["Unnamed: 0.1"][i]
                self.optimal['cash_out_loss'][index] = cash
                self.optimal['loss'][index] = i
                self.optimal['loss_profit'][index] = (1-perc)*(cash - 1) - (perc * 1)
                index += 1
            cash += 0.01
        index = 0
        cash = 1
        while cash <= point:
            for i in range(1, len(self.countWins)-1):
                perc = self.countWins["Unnamed: 0.1"][i+1] / self.countWins["Unnamed: 0.1"][i]
                self.optimal['cash_out_win'][index] = cash
                self.optimal['win'][index] = i
                self.optimal['win_profit'][index] = (perc)*(cash - 1) - ((1-perc) * 1)
                index += 1
            cash += 0.01
        self.optimal.to_csv("optimal.csv")
