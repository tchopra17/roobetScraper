import pandas as pd
import numpy as np



class analysis():
    def __init__(self, f):
        self.cp = "('Crash Point',)"
        self.cl = 'consec_loss'
        self.file = f
        self.loss = 0

    def main(self):
        df = self.prepData(1.5)
        cl = df.groupby(self.cl)
        counts = cl.agg("count")
        counts = counts.drop(counts.columns[[1,2]], axis=1)
        print(counts)
        print("----CL: " + str(self.loss))
        if (self.loss != (len(counts)-1)):
            perc = counts["Unnamed: 0.1"][self.loss+1] / counts["Unnamed: 0.1"][self.loss]
            print("----Win Percentage: " + str((1-perc)*100 )+ "%")
        print("_________________________________________________________")
        #breakEven(cp)


    def prepData(self, cash_out):
        df = pd.read_csv(self.file)
        a = df[self.cp].str.rstrip("x")
        df[self.cp] = a.astype(float)
        df[self.cl] = 0
        for i in range(len(df[self.cp])):
            if df[self.cp][i] < cash_out:
                self.loss += 1
                df[self.cl][i] = self.loss
            else:
                self.loss = 0
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
