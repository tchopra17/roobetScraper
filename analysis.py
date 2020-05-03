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

    def main(self, curr, cash_out):
        if (self.df.empty):
            self.df = self.prepData(cash_out)
            self.groupedLoss = self.df.groupby(self.cl)
            self.countLoss = self.groupedLoss.agg("count")
            self.countLoss = self.countLoss.drop(self.countLoss.columns[[1,2,3]], axis=1)
            self.groupedWins = self.df.groupby(self.cw)
            self.countWins= self.groupedWins.agg("count")
            self.countWins = self.countWins.drop(self.countWins.columns[[1,2,3]], axis=1)

        if (curr < cash_out):
            self.loss += 1
            self.wins = 0
        else:
            self.loss = 0
            self.wins += 1

        self.wins = 0

        print("----CL: " + str(self.loss))
        print("----CW: " + str(self.wins))
        if (self.loss != (len(self.countLoss)-1) and self.wins != (len(self.countWins)-1)):
            if self.wins == 0:
                for i in range(1, len(self.countLoss)-1):
                    perc = self.countLoss["Unnamed: 0.1"][i+1] / self.countLoss["Unnamed: 0.1"][i]
                    print(str(cash_out) + "----Profit at " +str(i) + "loss: " + str((1-perc)*(cash_out - 1) - (perc * 1)))
                for i in range(1, len(self.countWins)-1):
                    perc = self.countWins["Unnamed: 0.1"][i+1] / self.countWins["Unnamed: 0.1"][i]
                    print(str(cash_out) + "----Profit at " +str(i) + "wins: " + str((perc)*(cash_out - 1) - ((1-perc) * 1)))
            else:
                perc = self.countWins["Unnamed: 0.1"][self.wins+1] / self.countWins["Unnamed: 0.1"][self.wins]
                print("----Win Percentage: " + str((perc)*100 )+ "%")
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
a = analysis('scraped.csv')
a.main(1, 2)
