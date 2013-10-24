# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2012 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
Help class between the ly source parser and the XML creator
"""

from __future__ import unicode_literals


class mediator():
	""" Help class between the ly source parser and the XML creator """

	def __init__(self):
		""" create global lists """
		self.score = []
		self.sections = []
		""" default and initial values """
		self.mustime = [4,4]
		self.clef = ['G',2]
		self.divisions = 1
		self.duration = 4
		self.tied = False	
		
	def new_section(self, name):
		section = score_section(name)
		self.insert_into = section
		self.sections.append(section)
		self.bar = None
		
	def new_part(self):
		self.part = score_part()
		self.score.append(self.part)
		self.insert_into = self.part
		self.bar = None		
		
	def fetch_variable(self, varname):
		for n in self.sections:
			if n.name == varname:
				self.insert_into.barlist.extend(n.barlist)
				
	def check_parts(self):
		if not self.score:
			self.new_part()
			for n in self.sections:
				self.part.barlist.extend(n.barlist)										
		
	def new_bar(self):
		self.current_attr = bar_attr()
		self.bar = [self.current_attr]
		self.insert_into.barlist.append(self.bar)
		
	def new_key(self, key_name, mode_command):
		mode = mode_command[1:]
		self.current_attr.set_key(get_fifths(key_name, mode), mode)		
		
	def new_time(self, fraction):
		self.mustime = fraction.split('/')
		self.current_attr.set_time(self.mustime)
		
	def new_clef(self, clefname):
		self.clef = clefname2clef(clefname)
		self.current_attr.set_clef(self.clef)
		
	def new_note(self, note_name):
		self.current_note = bar_note(note_name, self.duration)
		if self.tied:
			self.current_note.set_tie('stop')
			self.tied = False
		if self.bar is None:
			self.new_bar()
		self.bar.append(self.current_note)
		self.current_attr = bar_attr()
		
	def new_rest(self, rtype, pos=0):
		if rtype == 'r':
			self.current_note = bar_rest(self.duration, pos)
		elif rtype == 'R':
			self.current_note = bar_rest(self.duration, pos, show_type=False)
		elif rtype == 's':
			self.current_note = bar_rest(self.duration, pos, skip=True)
		self.bar.append(self.current_note)
		self.current_attr = bar_attr()
		
	def note2rest(self):
		temp_note = self.current_note
		self.current_note = bar_rest(temp_note.duration, [temp_note.step, str(temp_note.octave)])
		self.bar.pop()
		self.bar.append(self.current_note)
		
	def scale_rest(self, multp, new_bar=True):
		""" create multiple whole bar rests """
		for i in range(1, int(multp)):
			self.part.append(self.bar)
		if new_bar:
			self.new_bar()
		
	def new_duration(self, duration):
		self.current_note.set_duration(duration)
		self.duration = duration
		self.check_divs(duration, self.current_note.tuplet)
		
	def change_to_tuplet(self, fraction, ttype):
		tfraction = fraction.split('/')
		tfraction.reverse() # delete this row with new tuplet notation		
		self.current_note.set_tuplet(tfraction, ttype)
		
	def new_dot(self):
		self.current_note.add_dot()
		
	def tie_to_next(self):
		if self.current_note.tie == 'stop': # only if previous was tied
			self.current_note.set_tie('continue')
		else:
			self.current_note.set_tie('start')
		self.tied = True		
				
	def new_octave(self, octave):
		self.current_note.set_octave(octave)
		
	def new_from_command(self, command):
		print command
		
	def check_divs(self, org_len, tfraction):
		""" The new duration is checked against current divisions """
		divs = self.divisions
		if(not tfraction):
			a = 4
			b = int(org_len)
		else:
			den = int(tfraction[0])
			num = int(tfraction[1])
			a = 4*num
			b = int(org_len)*den
		c = a*divs
		predur, mod = divmod(c,b)
		if mod > 0:
			mult = get_mult(a,b)
			self.divisions = divs*mult
			# print "---"
			# print "div:"+str(divs)
			# print "len:"+str(org_len)
			# print tfraction			
			# print "tupl:"+str(a)+'/'+str(b)
			# print "predur:"+str(predur)
			# print "mod:"+str(mod)
			# print "mult:"+str(mult)


class score_part():
	""" object to keep track of part """
	def __init__(self):
		self.name = "test"
		self.barlist = []			
			
class score_section():
	""" object to keep track of music section """
	def __init__(self, name):
		self.name = name
		self.barlist = []			
							
class bar_note():
	""" object to keep track of note parameters """
	def __init__(self, note_name, durval):
		plist = notename2step(note_name)
		self.step = plist[0]
		self.alter = plist[1]
		self.octave = 3
		self.duration = durval
		self.type = durval2type(durval)
		self.tuplet = 0
		self.dot = 0
		self.tie = 0
		
	def set_duration(self, durval):
		self.duration = durval
		self.type = durval2type(durval)
		
	def set_octave(self, octmark):
		self.octave = octmark2oct(octmark)
		
	def set_tuplet(self, fraction, ttype):
		self.tuplet = fraction
		self.ttype = ttype
		
	def set_tie(self, tie_type):
		self.tie = tie_type
		
	def add_dot(self):
		self.dot = self.dot + 1
				
class bar_rest():
	""" object to keep track of different rests and skips """
	def __init__(self, durval, pos, show_type=True, skip=False):
		self.duration = durval
		self.show_type = show_type
		if self.show_type:
			self.type = durval2type(durval)
		else:
			self.type = None
		self.skip = skip
		self.tuplet = 0
		self.pos = pos
		
	def set_duration(self, durval):
		self.duration = durval
		if self.show_type:
			self.type = durval2type(durval)
		else:
			self.type = None

		
class bar_attr():
	""" object that keep track of bar attributes, e.g. time sign, clef, key etc """
	def __init__(self):
		self.key = -1
		self.time = 0
		self.clef = 0
		self.mode = ''
		
	def set_key(self, muskey, mode):
		self.key = muskey
		self.mode = mode
		
	def set_time(self, mustime):
		self.time = mustime
		
	def set_clef(self, clef):
		self.clef = clef
		
	def has_attr(self):
		check = False	
		if self.key != -1:
			check = True
		elif self.time != 0:
			check = True
		elif self.clef != 0:
			check = True
		return check
		
def get_fifths(key, mode):
	sharpkeys = ['c', 'g', 'd', 'a', 'e', 'b', 'fis', 'cis', 'gis', 'dis', 'ais']
	flatkeys = ['c', 'f', 'bes', 'es', 'as', 'des', 'ges']
	if key in sharpkeys:
		fifths = sharpkeys.index(key)
	elif key in flatkeys:
		fifths = -flatkeys.index(key)
	if mode=='minor':
		return fifths-3
	elif mode=='major':
		return fifths		

def clefname2clef(clefname):
	if clefname == "treble":
		return ['G',2]
	elif clefname == "bass":
		return ['F',4]
	elif clefname == "alt":
		return ['C',3]
		
def notename2step(note_name):
	alter = 0
	if len(note_name)>1:
		is_sharp = note_name.split('i')
		is_flat = note_name.split('e')
		note_name = note_name[0]
		if len(is_sharp)>1:
			alter = 1		
		elif len(is_flat)>1:
			alter = -1
	return [note_name.upper(), alter]

def durval2type(durval):
	if durval == "1":
		return "whole"
	elif durval == "2":
		return "half"
	elif durval == "4":
		return "quarter"	
	elif durval == "8":
		return "eighth"
	elif durval == "16":
		return "16th"
	elif durval == "32":
		return "32nd"
		
def octmark2oct(octmark):
	if octmark == ",,,":
		return 0
	elif octmark == ",,":
		return 1
	elif octmark == ",":
		return 2
	elif octmark == "'":
		return 4	
	elif octmark == "''":
		return 5
	elif octmark == "'''":
		return 6
		
def get_mult(num, den):
	from fractions import Fraction
	simple = Fraction(num, den)
	return simple.denominator
		
		

	
		
	
