from numpy import *
import matplotlib.pyplot as plt
data = array([[98, 99], [76, 60], [60, 60], [30, 97], [66, 80], [66, 50], [70, 80], [69, 90]])
label = ['r', 'b', 'b', 'b', 'r', 'b', 'r', 'black']
def draw (x, y, label):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y, c=label, marker='o')
    plt.show()
draw(data[:,0], data[:,1], label)