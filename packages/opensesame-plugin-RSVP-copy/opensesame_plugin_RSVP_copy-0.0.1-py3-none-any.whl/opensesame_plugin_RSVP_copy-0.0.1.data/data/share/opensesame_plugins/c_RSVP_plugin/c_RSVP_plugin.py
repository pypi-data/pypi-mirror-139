from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
import numpy as np

# Class to handle the basic functionality of the item:
class c_RSVP_plugin(item):
	description = u'Add an RSVP to your experiment'


	# Reset plug-in to initial values:
	def reset(self):

		self.var._targets = u'4;8'
		self.var._distractors = u'q;w;e;r;t;y;u;i;o;p;a;s;d;f;g;h'
		self.var._ntargets = 2
		self.var._ndistractors = 15
		self.var._target_positions = u'5;7'
		self.var._stimdur = 300
		self.var._fixdur = 1000

	def prepare(self):

		# Call the parent constructor
		item.prepare(self)

		target_positions = [int(x) - 1 for x in self.var._target_positions.split(';')]
		targets = self.var._targets.split(';')
		distractors = self.var._distractors.split(';')

		self.cnvs_stream = {}
		for i in range(self.var._ndistractors + self.var._ntargets):
			if i in target_positions:
				t = targets.pop(0)
				self.cnvs_stream[str(i)] = canvas(self.experiment)
				self.cnvs_stream[str(i)].text(
					"<span style = 'color:rgba(0, 0, 0, .01)' >gb</span>{}<span style = color:rgba(0, 0, 0, .01)' >gb</span>".format(t),
					font_size = 48,
					color = u'rgb(190, 190, 190)',
					x = 0,
					y = 0
					)
				self.var.set('stim_%d' % i, t)

			else:
				d = distractors.pop(0)
				self.cnvs_stream[str(i)] = canvas(self.experiment)
				self.cnvs_stream[str(i)].text(
					"<span style = 'color:rgba(0, 0, 0, .01)' >gb</span>{}<span style = color:rgba(0, 0, 0, .01)' >gb</span>".format(d),
					font_size = 48,
					color = u'rgb(190, 190, 190)',
					x = 0,
					y = 0
					)
				self.var.set('stim_%d' % i, d)

		# Create fixation canvas
		self.cnvs_fix = canvas(self.experiment)
		self.cnvs_fix.fixdot()

	def run(self):

		# Fixation dot
		self.set_item_onset(self.cnvs_fix.show())

		self.sleep(self.var._fixdur)

		for i in range(self.var._ndistractors + self.var._ntargets):
			t = self.cnvs_stream[str(i)].show()

			self.sleep(self.var._stimdur)

# Class to handle the GUI aspect of the plug-in:
class qtc_RSVP_plugin(c_RSVP_plugin, qtautoplugin):

	def __init__(self, name, experiment, script = None):
		c_RSVP_plugin.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)