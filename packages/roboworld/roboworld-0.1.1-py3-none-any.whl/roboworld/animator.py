import copy
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import animation
from .cellstate import CellState

class Animator:
    """
    A helper class that generates a displayable representation of the robo world.

    Attributes
    ----------
    stack: list
        the stack contains the recording of the changes of the world, that is, copies of the past.
    active: bool
        a mark that activates and deactivates the recording.
    """

    def __init__(self) -> None:
        self.stack = []
        self.active = True

    def disbale(self):
        """Deactivate recording."""
        self.active = False
        self.stack.clear()

    def enable(self):
        """Activate recording"""
        self.active = True

    def get_animation(self, interval:int=150, save:bool=False, dpi:int=80) -> animation.FuncAnimation:
        """
        Returns a displayable animation of the movement of the roboter.
        Note that this call will clear the animation stack such that the next anmiation starts with the current situation.  

        Parameters
        ----------
        interval: int
            Delay between animation frames in milliseconds.
        save: bool
            If True a gif will be saved at './robo-world-animation.gif'.
        dpi: int
            Controls the dots per inch for the movie frames. Together with the figure's size in inches, this controls the size of the movie.
        """

        if len(self.stack) <= 1:
            raise Exception("Recording is to short to generate an animation.")
        stack_copy = copy.deepcopy(self.stack)
        #stack_copy = self.stack
        nrows = len(stack_copy[0])
        ncols = len(stack_copy[0][0])
        
        scale = 0.5

        fig = plt.figure(figsize=(ncols * scale, nrows * scale), dpi=dpi)
        fig.subplots_adjust(left=0, bottom=0, right=1,
                            top=1, wspace=None, hspace=None)
        ax = fig.add_subplot(1, 1, 1)
        ax.grid(which='both')
        matplt = ax.matshow(
            stack_copy[0], interpolation='nearest', vmin=0, vmax=3)
        x_ticks = np.arange(-0.5, ncols+1, 1)
        y_ticks = np.arange(-0.5, nrows+1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticks(x_ticks, minor=True)
        ax.set_yticks(y_ticks, minor=True)
        ax.set_xlim(-0.5, ncols-0.5)
        ax.set_ylim(-0.5, nrows-0.5)

        i = {'index': 0}  # trick to enforce sideeffect

        def updatefig(*args):
            i['index'] += 1
            if i['index'] >= len(stack_copy):
                i['index'] = 0
            matplt.set_array(stack_copy[i['index']])
            return matplt,

        plt.close()
        anim = animation.FuncAnimation(fig, updatefig, interval=interval, blit=True, save_count=len(stack_copy))
        if save:
            anim.save('robo-world-animation.gif',dpi=dpi, writer='imagemagick')
        self.stack.clear()
        return anim

    def show(self, world) -> Figure:
        """Returns a displayabel representation of the world."""

        scale = 0.5
        fig = plt.figure(figsize=(world.ncols * scale,
                         world.nrows * scale), dpi=80)
        ax = fig.add_subplot(1, 1, 1)
        x_ticks = np.arange(-0.5, world.ncols+1, 1)
        y_ticks = np.arange(-0.5, world.nrows+1, 1)
        values = world.cells
        # values = np.random.random((self.nrows, self.ncols))
        ax.grid(which='both')
        ax.matshow(values,  interpolation='nearest', vmin=0,
                   vmax=CellState.GOAL.value)  # vmin=0, vmax=5,cmap='gray',
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticks(x_ticks, minor=True)
        ax.set_yticks(y_ticks, minor=True)
        ax.set_xlim(-0.5, world.ncols-0.5)
        ax.set_ylim(-0.5, world.nrows-0.5)
        plt.close()
        return fig

    def _push(self, world) -> None:
        if self.active:
            int_list = [[state.value for state in row] for row in world.cells]
            self.stack.append(int_list)

    def _pop(self) -> None:
        if len(self.stack) > 0:
            return self.stack.pop()
        return None