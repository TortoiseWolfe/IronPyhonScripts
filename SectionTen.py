#Copyright(c) 2016 www.Learndynamo.com 
#Please contact at jeremy@learndynamo.com

import clr
clr.AddReference('RevitAPI')
clr.AddReference("RevitServices")
clr.AddReference("RevitNodes")
import RevitServices
import Revit
import Autodesk
from Autodesk.Revit.DB import *
from math import *

clr.ImportExtensions(Revit.GeometryConversion)

from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

toggle = IN[0]

elements = []
names = []
lst = []

#Get Family View Type
vft = 0
collector = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

#eleViews = []
for i in collector:
	if i.ViewFamily == ViewFamily.Elevation:
		elements.append(i)
		#elements.append(i.Name)
		for j in i.Parameters:
			if j.Definition.Name == "Type Name":
				names.append(j.AsString())
		
lst.append(elements)
lst.append(names)
	
OUT = lst