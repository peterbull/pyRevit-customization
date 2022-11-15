"""Calculate total volume of all walls in the model"""

__title__ = 'Total\nVolume'
__author__ = 'Peter Bull'
# __context__ = 'Selection'


from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter

doc = __revit__.ActiveUIDocument.Document

# Creating collector instance and collecting all the walls from the model
wall_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

# Iterate over walls and collect volume data

total_volume = 0.0

for wall in wall_collector:
    vol_param = wall.LookupParameter('Volume')

    if vol_param:
            total_volume = total_volume + vol_param.AsDouble()

# Now that reults are collected print the total
print("Total Volume is: {}".format(total_volume))
