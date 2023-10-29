import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

def get_palette(fin, n):
    """
    fin: filepath of image
    n: number of colors to be put into palette
    """
    img = cv.cvtColor(cv.imread(fin), cv.COLOR_BGR2RGB)
    k_cluster = KMeans(n_clusters=n, n_init=10)
    k_cluster.fit(img.reshape(-1, 3))
    
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_) # count how many pixels per cluster
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels, 2)
    perc = dict(sorted(perc.items()))
    
    return (img, perc, k_cluster.cluster_centers_)

if __name__ == "__main__":
    def show_imgs(img_1, img_2 ):
        f, ax = plt.subplots(1, 2, figsize=(10,10))
        ax[0].imshow(img_1)
        ax[1].imshow(img_2)
        ax[0].axis('off') #hide the axis
        ax[1].axis('off')
        f.tight_layout()
        plt.show()

    (img, perc, cluster_centers) = get_palette("tests/gkmc.jpeg", 5)

    #prints out RGB color codes and proportion of each color on image
    for i in range (len(perc)):
        color = cluster_centers[i]
        print(f"Proportion: {perc[i]} Color: RGB({color[0]}, {color[1]}, {color[2]})")

    # showing image + palette for testing purposes
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)

    step = 0
    for idx, centers in enumerate(cluster_centers): 
        palette[:, step:int(step + perc[idx]*width+1), :] = centers
        step += int(perc[idx]*width+1)
        
    show_imgs(img, palette)
