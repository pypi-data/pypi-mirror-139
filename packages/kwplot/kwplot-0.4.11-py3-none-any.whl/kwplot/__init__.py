"""
mkinit ~/code/kwplot/kwplot/__init__.py -w --relative --nomods
mkinit ~/code/kwplot/kwplot/__init__.py --diff --relative --nomods
"""

__version__ = '0.4.11'

from .auto_backends import (BackendContext, autompl, autoplt, autosns,
                            set_mpl_backend,)
from .draw_conv import (make_conv_images, plot_convolutional_features,)
from .mpl_3d import (plot_surface3d,)
from .mpl_color import (Color,)
from .mpl_core import (distinct_colors, distinct_markers, ensure_fnum, figure,
                       imshow, legend, next_fnum, phantom_legend, set_figtitle,
                       show_if_requested,)
from .mpl_draw import (draw_boxes, draw_boxes_on_image, draw_clf_on_image,
                       draw_line_segments, draw_points, draw_text_on_image,
                       plot_matrix,)
from .mpl_make import (make_heatmask, make_legend_img, make_orimask,
                       make_vector_field, render_figure_to_image,)
from .mpl_multiplot import (multi_plot,)
from .mpl_plotnums import (PlotNums,)

__all__ = ['BackendContext', 'Color', 'PlotNums', 'autompl', 'autoplt',
           'autosns', 'distinct_colors', 'distinct_markers', 'draw_boxes',
           'draw_boxes_on_image', 'draw_clf_on_image', 'draw_line_segments',
           'draw_points', 'draw_text_on_image', 'ensure_fnum', 'figure',
           'imshow', 'legend', 'make_conv_images', 'make_heatmask',
           'make_legend_img', 'make_orimask', 'make_vector_field',
           'multi_plot', 'next_fnum', 'phantom_legend',
           'plot_convolutional_features', 'plot_matrix', 'plot_surface3d',
           'render_figure_to_image', 'set_figtitle', 'set_mpl_backend',
           'show_if_requested']
