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
import math
from math import *

clr.ImportExtensions(Revit.GeometryConversion)

from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

toggle = IN[0]
point = UnwrapElement(IN[1])
modelPoints = UnwrapElement(IN[2])
cropCurves = UnwrapElement(IN[3])
viewType = UnwrapElement(IN[4])

lst = []

#Get Family View Type
vft = 0
collector = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

#eleViews = []
for i in collector:
	if i.ViewFamily == ViewFamily.Elevation:		
		vft = i.Id
		break
 
if toggle == True:
	
	TransactionManager.Instance.EnsureInTransaction(doc)
	

	
		#Retrieve the mid point of model lines and get X,Y.	
	index = 0
	for modelpoint in modelPoints:	
		modelMP = modelpoint.ToXyz()
		modelMPX = modelMP.X
		modelMPY = modelMP.Y
			
			#Retrieve individual lines of crop window.		
		cropLines = cropCurves[index]
		l1 = cropLines[0].ToRevitType()
		l2 = cropLines[1].ToRevitType()
		l3 = cropLines[2].ToRevitType()
		l4 = cropLines[3].ToRevitType()
						
			# Create a line in the z-Axis for elevation marker to rotate around.			
		elevationPT = point[index].ToXyz()
		elptRotate = XYZ(elevationPT.X, elevationPT.Y, elevationPT.Z+100)
		ln = Line.CreateBound(elevationPT, elptRotate)
	
			#Calculate the angle between Model Mid Point and Elevation Point.
		elevationPTY = elevationPT.Y
		elevationPTX = elevationPT.X	
		
		
		#combY = elevationPTY-modelMPY
		#combX = elevationPTX-modelMPX	
		
		combY = modelMPY-elevationPTY
		combX = modelMPX-elevationPTX			
		ang = -atan2(combX, combY)
		
		comparisonAng = round(degrees(ang))
		newAng = 90
		arrowPos = 2
		eleMarker = ElevationMarker.CreateElevationMarker(doc, viewType.Id, elevationPT, 100)
		#left arrow
		if comparisonAng >= 45 and comparisonAng <= 135:
			arrowPos = 0
			newAng = -90
		#top arrow
		#changed <= to < august 5th 2021
		if comparisonAng <= 45 and comparisonAng > -45:
			arrowPos = 1
			newAng = 0
		#bottom arrow
		if comparisonAng > 135 or comparisonAng < -135:
			arrowPos = 3
			ang = ang + radians(90)
			
		#default is right arrow
		ele = eleMarker.CreateElevation(doc, doc.ActiveView.Id , arrowPos)
		ElementTransformUtils.RotateElement(doc, eleMarker.Id, ln, ang)
		ElementTransformUtils.RotateElement(doc, eleMarker.Id, ln, radians(newAng))
		
		#ElementTransformUtils.RotateElement(doc, eleMarker.Id, ln, ang)
			#Create elevation marker and elevation in position 0.
			
			#Rotate elevation marker towars model line.
		
		#ElementTransformUtils.RotateElement(doc, eleMarker.Id, ln, math.radians(90))
			#	
		crManager = ele.GetCropRegionShapeManager()
			#crShape = crManager.GetCropRegionShape()
	
		newCurveLoop = []
		newCurveLoop.append(l1)
		newCurveLoop.append(l2)
		newCurveLoop.append(l3)
		newCurveLoop.append(l4)
				
		cLoop = CurveLoop.Create(newCurveLoop)
		index+=1

		try:			
			crManager.SetCropShape(cLoop)
			lst.append(ele)
			#lst.append("Elevation Created")
			
		except:
			pass
			lst.append("Missed Elevation")
	
		TransactionManager.Instance.TransactionTaskDone()
		
		#OUT = degrees(ang)
		OUT = lst
	
else:

	OUT = "Set toggle to TRUE"