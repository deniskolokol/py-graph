"""
A simple utility to center the axes of a plot at an arbitrary point, and add
arrows at the end of the axes. This is a common style for math plots, but is not
directly supported by matplotlib.

Adapted from:
https://stackoverflow.com/questions/4694478/center-origin-in-matplotlib
"""

from typing import cast

import numpy as np
from numpy.typing import NDArray

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as patheffects
import matplotlib.ticker as mticker
from matplotlib.path import Path as mPath
from matplotlib.transforms import Affine2D
from matplotlib.typing import ColorType
from matplotlib.backend_bases import RendererBase, GraphicsContextBase
from matplotlib.axes import Axes


class EndArrow(patheffects.AbstractPathEffect):
    """A matplotlib patheffect to add arrows at the end of a path."""
    def __init__(self,
                 headwidth: float = 5,
                 headheight: float = 5,
                 facecolor: ColorType = (0,0,0),
                 **kwargs):
        super().__init__()
        self.width, self.height = headwidth, headheight
        self._gc_args = kwargs
        self.facecolor = facecolor

        self.trans = Affine2D()
        # Warning: incorrect position! Fix it!
        self.arrowpath = mPath(
            np.array([[-0.005, -0.002],
                      [0.0, 0.0],
                      [0.005, -0.002],
                      [0.0, 0.001],
                      [-0.005, -0.002]]),
            np.array([1, 2, 2, 2, 79])
            )

    def draw_path(self,
                  renderer: RendererBase,
                  gc: GraphicsContextBase,
                  tpath: mPath,
                  affine: Affine2D,
                  rgbFace: ColorType | None
                  ) -> None:
        scalex = renderer.points_to_pixels(self.width)
        scaley = renderer.points_to_pixels(self.height)

        # At runtime it is a NumPy array, but may also be possible int, complex,
        # buffer, etc. Here used an explicit NumPy conversion + shape guard
        # before indexing/unpacking.
        verts = cast(NDArray[np.float64], np.asarray(tpath.vertices, dtype=np.float64))
        if verts.ndim != 2 or verts.shape[0] < 2 or verts.shape[1] < 2:
            renderer.draw_path(gc, tpath, affine, rgbFace)
            return

        x0, y0 = verts[-1, 0], verts[-1, 1]
        dx, dy = verts[-1] - verts[-2]
        azi =  np.arctan2(dy, dx) - np.pi / 2.0 
        trans = (affine + self.trans.clear()
                                    .scale(scalex, scaley) # type: ignore
                                    .rotate(azi)
                                    .translate(x0, y0))
        gc0 = renderer.new_gc()
        gc0.copy_properties(gc)
        self._update_gc(gc0, self._gc_args) # type: ignore

        if self.facecolor is None:
            color = rgbFace
        else:
            color = self.facecolor

        renderer.draw_path(gc0, self.arrowpath, trans, color)
        renderer.draw_path(gc, tpath, affine, rgbFace)
        gc0.restore()


class CenteredFormatter(mticker.ScalarFormatter):
    """
    Acts exactly like the default Scalar Formatter, but yields an empty
    label for ticks at "center".
    """
    def __init__(self, center: float = 0.0) -> None:
        super().__init__()
        self.center: float = center

    def __call__(self, value, pos=None):
        if value == self.center:
            return ""
        return mticker.ScalarFormatter.__call__(self, value, pos)


def center_spines(ax: Axes | None = None,
                  centerx: float = 0,
                  centery: float = 0) -> None:
    """
    Centers the axis spines at <centerx, centery> on the axis "ax", and
    places arrows at the end of the axis spines.
    """
    if ax is None:
        ax = plt.gca()

    # Set the axis's spines to be centered at the given point
    # (Setting all 4 spines so that the tick marks go in both directions)
    ax.spines['left'].set_position(('data', centerx))
    ax.spines['bottom'].set_position(('data', centery))
    ax.spines['right'].set_position(('data', centerx + 0.001))
    ax.spines['top'].set_position(('data', centery + 0.001))

    # Draw an arrow at the end of the spines
    ax.spines['left'].set_path_effects([EndArrow()])
    ax.spines['bottom'].set_path_effects([EndArrow()])

    # Hide the line (but not ticks) for "extra" spines
    for side in ['right', 'top']:
        ax.spines[side].set_color('none')

    # On both the x and y axes...
    for axis, center in zip([ax.xaxis, ax.yaxis], [centerx, centery]):
        # Turn on minor and major gridlines and ticks
        axis.set_ticks_position('both')
        axis.grid(True, 'major', ls='solid', lw=0.5, color='gray')
        axis.grid(True, 'minor', ls='solid', lw=0.1, color='gray')
        axis.set_minor_locator(mticker.AutoMinorLocator())

        # Hide the ticklabels at <centerx, centery>
        formatter = CenteredFormatter(center=float(center))
        axis.set_major_formatter(formatter)

    # Add offset ticklabels at <centerx, centery> using annotation
    # (Should probably make these update when the plot is redrawn...)
    def _format_coord(value):
        try:
            return formatter.format_data(value)
        except ValueError:
            if value == 0:
                return '0'
            return f'{value:g}'

    xlabel, ylabel = map(_format_coord, [centerx, centery])
    ax.annotate('(%s, %s)' % (xlabel, ylabel), (centerx, centery),
            xytext=(-4, -4), textcoords='offset points',
            ha='right', va='top')


if __name__ == '__main__':
    # Example - plot the function 1/(1-x) with centered axes at (0, 0)
    x1 = np.linspace(0, 0.9, 5)
    x2 = np.linspace(1.1, 2, 5)

    _y = lambda x: 1 / (1-x)

    plt.plot(x1, _y(x1), linestyle='-', marker='o', color='c')
    plt.plot(x2, _y(x2), linestyle='-', marker='o', color='c')
    center_spines()

    # Uncomment this to make the axes have equal aspect ratio, i.e. put the
    # origin at the center of a square plot. This is not necessary to have the
    # axes centered, but it can be aesthetically pleasing for some plots.
    # Note that the aspect ratio of the plot will not be preserved when resizing
    # the window!
    #
    # plt.axis('equal')

    plt.show()
