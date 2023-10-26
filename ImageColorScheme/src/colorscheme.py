import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

def get_colorscheme(fin, n):
    def show_imgs(img_1, img_2 ):
        f, ax = plt.subplots(1, 2, figsize=(10,10))
        ax[0].imshow(img_1)
        ax[1].imshow(img_2)
        ax[0].axis('off') #hide the axis
        ax[1].axis('off')
        f.tight_layout()
        plt.show()

    def palette(k_cluster):
        width = 300
        palette = np.zeros((50, width, 3), np.uint8)
        
        n_pixels = len(k_cluster.labels_)
        counter = Counter(k_cluster.labels_) # count how many pixels per cluster
        perc = {}
        for i in counter:
            perc[i] = np.round(counter[i]/n_pixels, 2)
        perc = dict(sorted(perc.items()))
        
        #for logging purposes
        print(perc)
        print(k_cluster.cluster_centers_)
        
        step = 0
        
        for idx, centers in enumerate(k_cluster.cluster_centers_): 
            palette[:, step:int(step + perc[idx]*width+1), :] = centers
            step += int(perc[idx]*width+1)
            
        return palette

    img = cv.cvtColor(cv.imread(fin), cv.COLOR_BGR2RGB)
    clt = KMeans(n_clusters=n)
    clt.fit(img.reshape(-1, 3))
    
    show_imgs(img, palette(clt))

if __name__ == "__main__":
    get_colorscheme("tests/gkmc.jpeg", 5)
