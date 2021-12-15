'''
Created on May 24, 2021
Translated May 24, 2021

@author: bleem
'''

from src.common import Constants
from src.common.SampleWoutReplace import SampleWoutReplace
from src.orgs.ETBDOrganism import ETBDOrganism
from src.orgs.NetOneOrganism import NetOneOrganism
from src.orgs.NetTwoOrganism import NetTwoOrganism
from src.orgs.NullOrganism import NullOrganism


class frmBuildOrganism(object):
	'''
	classdocs
	'''

	def __init__(self):

		self.m_intPopulationIndex = None

		self.m_objSampler = SampleWoutReplace()

		self.m_blnExists = None  # Added 10/2017 for error handling

	def exists(self):
		return self.m_blnExists

	def set_exists(self, value):
		self.m_blnExists = value

	def get_creature(self):  # Changed from Public Property to Shared property 10/2017 to make this work with 4.0
		# 											   Changed it back!

		# Envisioned usage:  This form will be part of an MDI application and will be used only to build an
		# organism.  The laboratory part of the form will not be used (although it could be used for testing,
		# etc., or it could be removed altogether).  The user will set all the organism properties on the right
		# hand side of the form by clicking the "Create this population" button for each population (and discriminative
		# stimulus).  This will load up self.m_objOrganism with the desired populations of potential behaviors.

		# Actual experiments will be run by other code.  For example, there might be a schedule form (single,
		# concurrent, chained schedules, with parameters), and an experiment layout and data storage form, and perhaps
		# a data analysis form.  This additional code will access the built organism through the Creature property
		# (this property) of the frmBuildOrganism class (form).  The syntax might be something like this:
		# 	   Dim myOrganism as New AnOrganism
		# 	   myOrganism = frmBuildOrganism.Creature
		# The additional code that actually runs the experiments will have no other contact with this form.

		# In normal operation, the experiment-running code will have only three points of contact with the built organism,
		# let's say, myOrganism.  (The following three points are applicable to Version 3.0.  Version 3.1 implements a simpler method
		# of interacting with the built organism.  See the Guide for an explanation.  The Version 3.0 functionality described below is
		# fully retained in Version 3.1.)
		# 1. The correct population in myOrganism is accessed by "turning on the discriminative stimulus" with
		#   syntax like myOrganism.Item(indexOfDiscriminativeStimulus).  The Item returned by this statement is the
		#   population of potential behaviors associated with that discriminative stimulus.
		# 2. Each time tick the population must be queried for a behavioral emssion (as in DoARun below):
		# 		 emittedBehaviorAsInteger = myOrganism.Item(indexOfDiscriminativeStimulus).EmitBehavior.IntegerValue
		# 3. After the emitted behavior is obtained, the experiment-running code will communicate to myOrganism whether
		#   the behavior is reinforced by setting its Selection property (as in DoARun below).  There are two syntax versions
		#   for doing this:
		# 		 myOrganism.Item(indexOfDiscriminativeStimulus).Selection(selectionParameter, intMidpoint) = True (if reinforced)/False (if not reinforced).
		# 		 myOrganism.Item(indexOfDiscriminativeStimulus).Selection(selectionParameter) = True/False
		#   The first syntax is required if midpoint fitness is being used, in which case intMidpoint is the midpoint of
		#   the target class to which the emitted behavior belongs (which, as the code is currently written, must be an integer).
		#   The second syntax can be used for all other fitness methods.  If the first syntax is used for the other fitness
		#   methods, then the passed value of intMidpoint is ignored.  In both cases, the selectionParameter must be passed to the
		#   Selection property.  This is the mean of the parental choosing function for the continuous selection method, the proportion
		#   of the population to be discarded for the truncation selection method, and the number of competitors for the tournament
		#   selection method.

		# That's it.  Each generation, the organism must be queried for an emitted behavior, and then told whether or not that
		# behavior is reinforced.  The organism code does all the rest.

		# A different approach is to load the populations in myOrganism into separate Behaviors classes:
		# 	   Dim whitePopulation as New Behaviors
		# 	   Dim redPopulation as New Behaviors
		# 	   Dim greenPopulation as New Behaviors
		#
		# 	   whitePopulation = myOrganism.Item(indexOfWhiteSD)
		# 	   redPopulation = myOrganism.Item(indexOfRedSD)
		# 	   greenPopulation = myOrganism.Item(indexOfGreenSD)
		# Then the emission and reinforcement statements are executed for whichever discriminative stimulus is in effect, say the
		# white one:
		# 	   emittedBehaviorAsInteger = whitePopulation.EmitBehavior.IntegerValue
		# 	   whitePopulation.Selection(selectionParameter, intMidpoint) = True or False

		# Although in normal operation these are the only points of contact between the laboratory code and myOrganism, in fact
		# all the properties of all populations are available to the laboratory code from the myOrganism object via the read-only
		# BehaviorsInfo property of each Behaviors class.

		# Finally, note how kickout is handled in the Try...Catch block in DoARun (see "Defunct procedures no longer used" region).
		# Some form of this must be implemented in the laboratory code.  Kickout occurs if there is a problem getting enough distinct
		# fit behaviors to reproduce.  The code in DoARun shows how the population is restarted from a random state, but the laboratory
		# code must also discard all the data collected up to that point and start over again.  This is the way the old code works,
		# although we can discuss ways of handling this differently by, for example, permitting cloning or "next best" parents in the event
		# of insufficient numbers of fit parents.

		return self.m_objOrganism

	def create_an_organism(self, json_data):  # Handles btnDifferent.Click

		ot = json_data.get_organism_type()
		if ot == Constants.ORG_TYPE_ETBD:
			self.m_objOrganism = ETBDOrganism(json_data)
		elif ot == Constants.ORG_TYPE_NET_ONE:
			self.m_objOrganism = NetOneOrganism(json_data)
		elif ot == Constants.ORG_TYPE_NET_TWO:
			self.m_objOrganism = NetTwoOrganism(json_data)
		elif ot == Constants.ORG_TYPE_NULL:
			self.m_objOrganism = NullOrganism(json_data)
		else:
			raise NameError("Unknown type of organism " + str(ot))

		self.set_exists(True)

# Region " Loaders"

