# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# DateFiledAdd.py
# Created on: 2017-10-02 13:04:08.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: DateFiledAdd <Date> 
# Description: 
# SolidWaste
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Load required toolboxes
arcpy.ImportToolbox("C:/atlas_shared/AVL/Zonar.gdb/AVL")

# Script arguments
Date = arcpy.GetParameterAsText(0)

# Local variables:
solid_cur = "C:\\atlas_shared\\AVL\\Zonar.gdb\\solid_cur"
solid_cur__2_ = solid_cur
solid_cur__3_ = solid_cur__2_

# Process: Add Field
arcpy.AddField_management(solid_cur, "date2", "DATE", "", "", "", "", "NULLABLE", "REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(solid_cur__2_, "date2", "[date]", "VB", "")

# Process: AllTimeSolidWaste
arcpy.gp.toolbox = "C:/atlas_shared/AVL/Zonar.gdb/AVL";
# Warning: the toolbox C:/atlas_shared/AVL/Zonar.gdb/AVL DOES NOT have an alias. 
# Please assign this toolbox an alias to avoid tool name collisions
# And replace arcpy.gp.AllTimeSolidWaste(...) with arcpy.AllTimeSolidWaste_ALIAS(...)
arcpy.gp.AllTimeSolidWaste(Date)
