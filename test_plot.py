'''
# deux maniere de faire des graph ..
# la premiere pylab et la deuxime plus traditionnel

from pylab import *


x = array([1,3,4,6])
y = array([2,3,5,1])

plot(x,y)
i = 0
show()

import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 3, 4, 6])
y = np.array([2, 3, 5, 1])
plt.plot(x, y)

plt.show()

from pylab import *

x = linspace(0, 2*pi, 30)
y = cos(x)
plot(x, y)

show()


import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
plt.plot(x, y)

plt.show() # affiche la figure a l'ecran

# changer les nums de x et y

from pylab import *

x = linspace(0, 2*pi, 30)
y = cos(x)
plot(x, y)
xlim(-1, 5)
ylim(-2, 2)

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
plt.plot(x, y)
plt.xlim(-1, 5)

plt.show()

#metre un titre

from pylab import *

x = linspace(0, 2*pi, 30)
y = cos(x)
plot(x, y)
title("Fonction cosinus")

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
plt.plot(x, y)
plt.title("Fonction cosinus")

plt.show()

#en ajoutant le label, il le prend et le met dans la legent()
from pylab import *

x = linspace(0, 2*pi, 30)
y = cos(x)
plot(x, y, label="cos(x)")
legend()

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
plt.plot(x, y, label="cos(x)")
plt.legend()

plt.show()


#mettre un label aux axes
from pylab import *

x = linspace(0, 2*pi, 30)
y = cos(x)
plot(x, y)
xlabel("abscisses")
ylabel("ordonnees")

show()


import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
plt.plot(x, y)
plt.xlabel("abscisses")
plt.ylabel("ordonnees")

plt.show()

# affichage de 2 courbes

from pylab import *

x = linspace(0, 2*pi, 30)
y1 = cos(x)
y2 = sin(x)
plot(x, y1)
plot(x, y2)

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y1 = np.cos(x)
y2 = np.sin(x)
plt.plot(x, y1)
plt.plot(x, y2)

plt.show()

# plusieurs courbes avec legende

from pylab import *

x = linspace(0, 2*pi, 30)
y1 = cos(x)
y2 = sin(x)
plot(x, y1, label="cos(x)")
plot(x, y2, label="sin(x)")
legend()

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y1 = np.cos(x)
y2 = np.sin(x)
plt.plot(x, y1, label="cos(x)")
plt.plot(x, y2, label="sin(x)")
plt.legend()

plt.show()

#en ajoutant "r-- on choisis la couleur et le type de ligne
#couleur b g r c m y b w

from pylab import *

x = linspace(0, 2*pi, 30)
y1 = cos(x)
y2 = sin(x)
plot(x, y1, "r--", label="cos(x)")
plot(x, y2, "b:o", label="sin(x)")
legend()

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y1 = np.cos(x)
y2 = np.sin(x)
plt.plot(x, y1, "y--o", label="cos(x)")
plt.plot(x, y2, "g:o", label="sin(x)")
plt.legend()

plt.show()

# l'essai de tous les types
#les types sont : - -- : -.
# type de marker : . , o v ^ < > 1 2 3 4 s p * h H + x D d | _

from pylab import *

x = linspace(0, 2*pi, 20)
y = sin(x)
plot(x, y, "m-D", label="ligne -")
plot(x, y-0.5, "c--v", label="ligne --")
plot(x, y-1, "k:.", label="ligne :")
plot(x, y-1.5, "w-.*", label="ligne -.")
plot(x, y-2, "|", label="pas de ligne")
legend()

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 20)
y = np.sin(x)
plt.plot(x, y, "o-", label="ligne -")
plt.plot(x, y-0.5, "o--", label="ligne --")
plt.plot(x, y-1, "o:", label="ligne :")
plt.plot(x, y-1.5, "o-.", label="ligne -.")
plt.plot(x, y-2, "o", label="pas de ligne")
plt.legend()

plt.show()


#changer la largeur de la ligne

from pylab import *

x = linspace(0, 2*pi, 30)
y1 = cos(x)
y2 = sin(x)
plot(x, y1, label="cos(x)")
plot(x, y2, label="sin(x)", linewidth=4)
legend()

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 30)
y1 = np.cos(x)
y2 = np.sin(x)
plt.plot(x, y1, label="cos(x)")
plt.plot(x, y2, label="sin(x)", linewidth=4)
plt.legend()

plt.show()


# plusieurs points avec le meme abscisse donc ce n'est pas une droite

from pylab import *

x = array([0, 1, 1, 0, 0])
y = array([0, 0, 1, 1, 0])
plot(x, y)
xlim(-1, 2)
ylim(-1, 2)

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.array([0, 1, 1, 0, 0])
y = np.array([0, 0, 1, 1, 0])
plt.plot(x, y)
plt.xlim(-1, 2)
plt.ylim(-1, 2)

plt.show()


# le axis("equal") met les abcisses et les ordonnees egal
from pylab import *

x = array([0, 1, 1, 0, 0])
y = array([0, 0, 1, 1, 0])
plot(x, y)
axis("equal")

show()

import numpy as np
import matplotlib.pyplot as plt

x = np.array([0, 1, 1, 0, 0])
y = np.array([0, 0, 1, 1, 0])
plt.plot(x, y)
plt.axis("equal")

plt.show()


#trace d'un cercle avec axis("equal") et sans
#en plus avec un xlim on modifie indirectement y aussi
from pylab import *

theta = linspace(0, 2*pi, 40)

x = cos(theta)
y = sin(theta)
axis("equal")
xlim(-4,4)
plot(x, y)

show()

import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 40)

x = np.cos(theta)
y = np.sin(theta)
plt.plot(x, y)

plt.show()


print 'ok'

# exemple de changement de courbe en photo

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage

from matplotlib._png import read_png
import matplotlib.colors
from matplotlib.cbook import get_sample_data


class RibbonBox(object):

    original_image = read_png(get_sample_data("Minduka_Present_Blue_Pack.png",
                                              asfileobj=False))
    cut_location = 70
    b_and_h = original_image[:, :, 2]
    color = original_image[:, :, 2] - original_image[:, :, 0]
    alpha = original_image[:, :, 3]
    nx = original_image.shape[1]

    def __init__(self, color):
        rgb = matplotlib.colors.colorConverter.to_rgb(color)

        im = np.empty(self.original_image.shape,
                      self.original_image.dtype)

        im[:, :, :3] = self.b_and_h[:, :, np.newaxis]
        im[:, :, :3] -= self.color[:, :, np.newaxis]*(1. - np.array(rgb))
        im[:, :, 3] = self.alpha

        self.im = im

    def get_stretched_image(self, stretch_factor):
        stretch_factor = max(stretch_factor, 1)
        ny, nx, nch = self.im.shape
        ny2 = int(ny*stretch_factor)

        stretched_image = np.empty((ny2, nx, nch),
                                   self.im.dtype)
        cut = self.im[self.cut_location, :, :]
        stretched_image[:, :, :] = cut
        stretched_image[:self.cut_location, :, :] = \
            self.im[:self.cut_location, :, :]
        stretched_image[-(ny - self.cut_location):, :, :] = \
            self.im[-(ny - self.cut_location):, :, :]

        self._cached_im = stretched_image
        return stretched_image


class RibbonBoxImage(BboxImage):
    zorder = 1

    def __init__(self, bbox, color,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 filternorm=1,
                 filterrad=4.0,
                 resample=False,
                 **kwargs
                 ):

        BboxImage.__init__(self, bbox,
                           cmap=cmap,
                           norm=norm,
                           interpolation=interpolation,
                           origin=origin,
                           filternorm=filternorm,
                           filterrad=filterrad,
                           resample=resample,
                           **kwargs
                           )

        self._ribbonbox = RibbonBox(color)
        self._cached_ny = None

    def draw(self, renderer, *args, **kwargs):

        bbox = self.get_window_extent(renderer)
        stretch_factor = bbox.height / bbox.width

        ny = int(stretch_factor*self._ribbonbox.nx)
        if self._cached_ny != ny:
            arr = self._ribbonbox.get_stretched_image(stretch_factor)
            self.set_array(arr)
            self._cached_ny = ny

        BboxImage.draw(self, renderer, *args, **kwargs)


if 1:
    from matplotlib.transforms import Bbox, TransformedBbox
    from matplotlib.ticker import ScalarFormatter

    fig, ax = plt.subplots()

    years = np.arange(2004, 2009)
    box_colors = [(0.8, 0.2, 0.2),
                  (0.2, 0.8, 0.2),
                  (0.2, 0.2, 0.8),
                  (0.7, 0.5, 0.8),
                  (0.3, 0.8, 0.7),
                  ]
    heights = np.random.random(years.shape) * 7000 + 3000

    fmt = ScalarFormatter(useOffset=False)
    ax.xaxis.set_major_formatter(fmt)

    for year, h, bc in zip(years, heights, box_colors):
        bbox0 = Bbox.from_extents(year - 0.4, 0., year + 0.4, h)
        bbox = TransformedBbox(bbox0, ax.transData)
        rb_patch = RibbonBoxImage(bbox, bc, interpolation="bicubic")

        ax.add_artist(rb_patch)

        ax.annotate(r"%d" % (int(h/100.)*100),
                    (year, h), va="bottom", ha="center")

    patch_gradient = BboxImage(ax.bbox,
                               interpolation="bicubic",
                               zorder=0.1,
                               )
    gradient = np.zeros((2, 2, 4), dtype=np.float)
    gradient[:, :, :3] = [1, 1, 0.]
    gradient[:, :, 3] = [[0.1, 0.3], [0.3, 0.5]]  # alpha channel
    patch_gradient.set_array(gradient)
    ax.add_artist(patch_gradient)

    ax.set_xlim(years[0] - 0.5, years[-1] + 0.5)
    ax.set_ylim(0, 10000)

    fig.savefig('ribbon_box.png')
    plt.show()

#sauvegarder le graph

from pylab import *

x = array([0, 1, 1, 0, 0])
y = array([0, 0, 1, 1, 0])
plot(x, y)
xlim(-5, 2)
ylim(-1, 2)

savefig('test.png')
'''
def split_int(number, separator=' ', count=3):
    return separator.join(
        [str(number)[::-1][i:i+count] for i in range(0, len(str(number)), count)]
    )[::-1]
a = '200000000000'
b = a.split()
print b
c = split_int(a)
print c