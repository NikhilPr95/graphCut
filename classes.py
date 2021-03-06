#node class representing each pixel
class Node:
	def __init__(self, x, y, val):
		self.x = x
		self.y = y
		self.val = val

	def coordinates(self):
		return (self.x, self.y)
		
	def val(self):
		return val

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()