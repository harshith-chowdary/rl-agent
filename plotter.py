import matplotlib.pyplot as plt
import numpy as np

class line_graph:
    def draw(self,xs,ys,title,xlab,ylab):
        x=np.array(xs)
        y=np.array(ys)

        plt.plot(x,y,'*:m',mec='k',mfc='green',ms=10)

        font_title={'family':'serif','color':'darkblue','size':20}
        font_label={'family':'serif','color':'red','size':15}

        plt.title(title,fontdict=font_title)
        plt.xlabel(xlab,fontdict=font_label)
        plt.ylabel(ylab,fontdict=font_label)

        return plt.show()
