"""
Copyright (c) 2010 cmiVFX.com <info@cmivfx.com>

This file is part of AtomSplitter.

AtomSplitter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AtomSplitter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AtomSplitter.  If not, see <http://www.gnu.org/licenses/>.

Written by: Justin Israel
			justinisrael@gmail.com
			justinfx.com

"""


def getTemplate(objectType = 'null', objectData=[]):
	""" Returns the FBX file template """
	
	if objectType == 'null':
		objectdata = nullType()
		objectName = "null1"
	
	elif objectType == 'camera':
		objectdata = cameraType()
		objectName = "camera1"
   
	else:
		return ""
	
		
	connectionList = []
	connectionList.append('\tConnect: "OO", "Model::%s", "Model::Scene"' % objectName)
	
	if objectData:
		
		for thisData in objectData:
			objectdata = "%s\n%s" % (objectdata, thisData['data'])
			connectionList.append('\tConnect: "OO", "Model::%(name)s", "Model::%(parent)s"' % \
									{'name' : thisData['name'], 
									 'parent' : thisData.get('parent', 'Scene')})
	
	connections = '\n'.join(connectionList)
	
	# main template
	template = """
		; FBX 6.1.0 project file
		; Created by AtomSplitter (cmiVFX.com & JustinFX.com)
		; 
		; ----------------------------------------------------
		
		FBXHeaderExtension:  {
			FBXHeaderVersion: 1003
			FBXVersion: 6100
			CreationTimeStamp:  {
				Version: 1000
				Year: %(date_year)s
				Month: %(date_month)s
				Day: %(date_day)s
				Hour: %(date_hour)s
				Minute: %(date_minute)s
				Second: %(date_second)s
				Millisecond: 0
			}
			Creator: "cmiVFX.com & JustinFX.com: AtomSplitter v1.5"
			OtherFlags:  {
				FlagPLE: 0
			}
		}
		CreationTime: "%(date_timestamp)s"
		Creator: "cmiVFX.com & JustinFX.com: AtomSplitter v1.5"
		
		; Document Description
		;------------------------------------------------------------------
		
		Document:  {
			Name: ""
		}
		
		; Document References
		;------------------------------------------------------------------
		
		References:  {
		}
		
		; Object definitions
		;------------------------------------------------------------------
		
		Definitions:  {
			Version: 100
			Count: %(totalObjCount)d
			ObjectType: "Model" {
				Count: %(totalModelCount)d
			}
			ObjectType: "GlobalSettings" {
				Count: 1
			}
		}
		
		; Object properties
		;------------------------------------------------------------------
		
		Objects:  {  
		""" + objectdata + \
		"""
			GlobalSettings:  {
				Version: 1000
				Properties60:  {
					Property: "UpAxis", "int", "",1
					Property: "UpAxisSign", "int", "",1
					Property: "FrontAxis", "int", "",2
					Property: "FrontAxisSign", "int", "",1
					Property: "CoordAxis", "int", "",0
					Property: "CoordAxisSign", "int", "",1
					Property: "UnitScaleFactor", "double", "",1
				}
			}
		}
		
		; Object connections
		;------------------------------------------------------------------
		
		Connections:  {
		""" + connections + \
		"""
		}
		;Takes and animation section
		;----------------------------------------------------
		
		Takes:  {
			Current: "Take 001"
			Take: "Take 001" {
				FileName: "Take_001.tak"
				LocalTime: %(fbxTime_start)s,%(fbxTime_end)s
				ReferenceTime: %(fbxTime_start)s,%(fbxTime_end)s
				
				;Models animation
				;----------------------------------------------------
				%(animationData)s
			}
		}
		;Version 5 settings
		;------------------------------------------------------------------
		
		Version5:  {
			AmbientRenderSettings:  {
				Version: 101
				AmbientLightColor: 0,0,0,1
			}
			FogOptions:  {
				FlogEnable: 0
				FogMode: 0
				FogDensity: 0.002
				FogStart: 0.3
				FogEnd: 1000
				FogColor: 1,1,1,1
			}
			Settings:  {
				FrameRate: "%(fps)s"
				TimeFormat: 1
				SnapOnFrames: 0
				ReferenceTimeIndex: -1
				TimeLineStartTime: %(fbxTime_start)s
				TimeLineStopTime: %(fbxTime_end)s
			}
			RendererSetting:  {
				DefaultCamera: "Producer Perspective"
				DefaultViewingMode: 0
			}
		}

	""" 
	
	return template.replace('\n\t\t', '\n').lstrip()


def cameraType():
	""" """
	data = """
			Model: "Model::camera1", "Camera" {
				Version: 232
				Properties60:  {
					Property: "QuaternionInterpolate", "bool", "",0
					Property: "RotationOffset", "Vector3D", "",0,0,0
					Property: "RotationPivot", "Vector3D", "",0,0,0
					Property: "ScalingOffset", "Vector3D", "",0,0,0
					Property: "ScalingPivot", "Vector3D", "",0,0,0
					Property: "TranslationActive", "bool", "",0
					Property: "TranslationMin", "Vector3D", "",0,0,0
					Property: "TranslationMax", "Vector3D", "",0,0,0
					Property: "TranslationMinX", "bool", "",0
					Property: "TranslationMinY", "bool", "",0
					Property: "TranslationMinZ", "bool", "",0
					Property: "TranslationMaxX", "bool", "",0
					Property: "TranslationMaxY", "bool", "",0
					Property: "TranslationMaxZ", "bool", "",0
					Property: "RotationOrder", "enum", "",%(rotationOrder)s
					Property: "RotationSpaceForLimitOnly", "bool", "",0
					Property: "RotationStiffnessX", "double", "",0
					Property: "RotationStiffnessY", "double", "",0
					Property: "RotationStiffnessZ", "double", "",0
					Property: "AxisLen", "double", "",10
					Property: "PreRotation", "Vector3D", "",0,0,0
					Property: "PostRotation", "Vector3D", "",-0,-90,0
					Property: "RotationActive", "bool", "",1
					Property: "RotationMin", "Vector3D", "",0,0,0
					Property: "RotationMax", "Vector3D", "",0,0,0
					Property: "RotationMinX", "bool", "",0
					Property: "RotationMinY", "bool", "",0
					Property: "RotationMinZ", "bool", "",0
					Property: "RotationMaxX", "bool", "",0
					Property: "RotationMaxY", "bool", "",0
					Property: "RotationMaxZ", "bool", "",0
					Property: "InheritType", "enum", "",1
					Property: "ScalingActive", "bool", "",0
					Property: "ScalingMin", "Vector3D", "",0,0,0
					Property: "ScalingMax", "Vector3D", "",0,0,0
					Property: "ScalingMinX", "bool", "",0
					Property: "ScalingMinY", "bool", "",0
					Property: "ScalingMinZ", "bool", "",0
					Property: "ScalingMaxX", "bool", "",0
					Property: "ScalingMaxY", "bool", "",0
					Property: "ScalingMaxZ", "bool", "",0
					Property: "GeometricTranslation", "Vector3D", "",0,0,0
					Property: "GeometricRotation", "Vector3D", "",0,0,0
					Property: "GeometricScaling", "Vector3D", "",1,1,1
					Property: "MinDampRangeX", "double", "",0
					Property: "MinDampRangeY", "double", "",0
					Property: "MinDampRangeZ", "double", "",0
					Property: "MaxDampRangeX", "double", "",0
					Property: "MaxDampRangeY", "double", "",0
					Property: "MaxDampRangeZ", "double", "",0
					Property: "MinDampStrengthX", "double", "",0
					Property: "MinDampStrengthY", "double", "",0
					Property: "MinDampStrengthZ", "double", "",0
					Property: "MaxDampStrengthX", "double", "",0
					Property: "MaxDampStrengthY", "double", "",0
					Property: "MaxDampStrengthZ", "double", "",0
					Property: "PreferedAngleX", "double", "",0
					Property: "PreferedAngleY", "double", "",0
					Property: "PreferedAngleZ", "double", "",0
					Property: "LookAtProperty", "object", ""
					Property: "UpVectorProperty", "object", ""
					Property: "Show", "bool", "",1
					Property: "NegativePercentShapeSupport", "bool", "",1
					Property: "DefaultAttributeIndex", "int", "",0
					Property: "Lcl Translation", "Lcl Translation", "A+",0,0,0
					Property: "Lcl Rotation", "Lcl Rotation", "A+",0,0,0
					Property: "Lcl Scaling", "Lcl Scaling", "A+",1,1,1
					Property: "Visibility", "Visibility", "A+",1
					Property: "Position", "Vector", "A+N",0,0,-50
					Property: "UpVector", "Vector", "A+N",0,1,0
					Property: "InterestPosition", "Vector", "A+N",0,0,-1
					Property: "Roll", "Roll", "A+N",0
					Property: "OpticalCenterX", "OpticalCenterX", "A+N",0
					Property: "OpticalCenterY", "OpticalCenterY", "A+N",0
					Property: "BackgroundColor", "Color", "A+N",0,0,0
					Property: "TurnTable", "Number", "A+N",0
					Property: "DisplayTurnTableIcon", "bool", "N",0
					Property: "UseMotionBlur", "bool", "N",0
					Property: "UseRealTimeMotionBlur", "bool", "N",1
					Property: "Motion Blur Intensity", "Number", "A+N",1
					Property: "AspectRatioMode", "enum", "N",0
					Property: "AspectWidth", "double", "N",%(width)s
					Property: "AspectHeight", "double", "N",%(height)s
					Property: "PixelAspectRatio", "double", "N",1
					Property: "FilmOffset", "Vector2D", "N",0,0
					Property: "FilmWidth", "double", "N",%(filmWidth)s
					Property: "FilmHeight", "double", "N",%(filmHeight)s
					Property: "FilmAspectRatio", "double", "N",%(aspect).6f
					Property: "FilmSqueezeRatio", "double", "N",1
					Property: "FilmFormatIndex", "enum", "N",0
					Property: "ApertureMode", "enum", "N",3
					Property: "GateFit", "enum", "N",3
					Property: "FieldOfView", "FieldOfView", "A+N",%(fov)s
					Property: "FieldOfViewX", "FieldOfViewX", "A+N",40
					Property: "FieldOfViewY", "FieldOfViewY", "A+N",40
					Property: "FocalLength", "Number", "A+N",%(focalLength)s
					Property: "CameraFormat", "enum", "N",0
					Property: "UseFrameColor", "bool", "N",0
					Property: "FrameColor", "ColorRGB", "N",0.3,0.3,0.3
					Property: "ShowName", "bool", "N",1
					Property: "ShowInfoOnMoving", "bool", "N",1
					Property: "ShowGrid", "bool", "N",1
					Property: "ShowOpticalCenter", "bool", "N",0
					Property: "ShowAzimut", "bool", "N",1
					Property: "ShowTimeCode", "bool", "N",0
					Property: "ShowAudio", "bool", "N",0
					Property: "AudioColor", "ColorRGB", "N",0,1,0
					Property: "NearPlane", "double", "N",0.01
					Property: "FarPlane", "double", "N",1000
					Property: "AutoComputeClipPanes", "bool", "N",1
					Property: "ViewFrustum", "bool", "N",1
					Property: "ViewFrustumNearFarPlane", "bool", "N",0
					Property: "ViewFrustumBackPlaneMode", "enum", "N",2
					Property: "BackPlaneDistance", "double", "N",100
					Property: "BackPlaneDistanceMode", "enum", "N",0
					Property: "ViewCameraToLookAt", "bool", "N",1
					Property: "LockMode", "bool", "N",0
					Property: "LockInterestNavigation", "bool", "N",0
					Property: "FitImage", "bool", "N",0
					Property: "Crop", "bool", "N",0
					Property: "Center", "bool", "N",1
					Property: "KeepRatio", "bool", "N",1
					Property: "BackgroundMode", "enum", "N",0
					Property: "BackgroundAlphaTreshold", "double", "N",0.5
					Property: "FrontPlateFitImage", "bool", "N",0
					Property: "FrontPlateCrop", "bool", "N",0
					Property: "FrontPlateCenter", "bool", "N",1
					Property: "FrontPlateKeepRatio", "bool", "N",1
					Property: "ShowFrontPlate", "bool", "N",0
					Property: "ViewFrustumFrontPlaneMode", "enum", "N",2
					Property: "FrontPlaneDistance", "double", "N",100
					Property: "ForegroundAlpha", "double", "N",0.5
					Property: "DisplaySafeArea", "bool", "N",0
					Property: "DisplaySafeAreaOnRender", "bool", "N",0
					Property: "SafeAreaDisplayStyle", "enum", "N",1
					Property: "SafeAreaAspectRatio", "double", "N",%(aspect).6f
					Property: "Use2DMagnifierZoom", "bool", "N",0
					Property: "2D Magnifier Zoom", "Number", "A+N",100
					Property: "2D Magnifier X", "Number", "A+N",50
					Property: "2D Magnifier Y", "Number", "A+N",50
					Property: "CameraProjectionType", "enum", "N",0
					Property: "OrthoZoom", "double", "N",1
					Property: "UseRealTimeDOFAndAA", "bool", "N",0
					Property: "UseDepthOfField", "bool", "N",0
					Property: "FocusSource", "enum", "N",0
					Property: "FocusAngle", "double", "N",3.5
					Property: "FocusDistance", "double", "N",5
					Property: "UseAntialiasing", "bool", "N",0
					Property: "AntialiasingIntensity", "double", "N",0.77777
					Property: "AntialiasingMethod", "enum", "N",0
					Property: "UseAccumulationBuffer", "bool", "N",0
					Property: "FrameSamplingCount", "int", "N",7
					Property: "FrameSamplingType", "enum", "N",1
					Property: "Color", "ColorRGB", "N",0.8,0.8,0.8
				}
				MultiLayer: 0
				MultiTake: 0
				Shading: Y
				Culling: "CullingOff"
				TypeFlags: "Camera"
				GeometryVersion: 124
				Position: 0,0,-50
				Up: 0,1,0
				LookAt: 0,0,-1
				ShowInfoOnMoving: 1
				ShowAudio: 0
				AudioColor: 0,1,0
				CameraOrthoZoom: 1
				NodeAttributeName: "NodeAttribute::camera1_ncl1_1"
			}
			"""
	return data


def nullType():
	""" """
	data = """
			Model: "Model::%(name)s", "Null" {
				Version: 232
				Properties60:  {
					Property: "QuaternionInterpolate", "bool", "",0
					Property: "RotationOffset", "Vector3D", "",0,0,0
					Property: "RotationPivot", "Vector3D", "",0,0,0
					Property: "ScalingOffset", "Vector3D", "",0,0,0
					Property: "ScalingPivot", "Vector3D", "",0,0,0
					Property: "TranslationActive", "bool", "",0
					Property: "TranslationMin", "Vector3D", "",0,0,0
					Property: "TranslationMax", "Vector3D", "",0,0,0
					Property: "TranslationMinX", "bool", "",0
					Property: "TranslationMinY", "bool", "",0
					Property: "TranslationMinZ", "bool", "",0
					Property: "TranslationMaxX", "bool", "",0
					Property: "TranslationMaxY", "bool", "",0
					Property: "TranslationMaxZ", "bool", "",0
					Property: "RotationOrder", "enum", "",0
					Property: "RotationSpaceForLimitOnly", "bool", "",0
					Property: "RotationStiffnessX", "double", "",0
					Property: "RotationStiffnessY", "double", "",0
					Property: "RotationStiffnessZ", "double", "",0
					Property: "AxisLen", "double", "",10
					Property: "PreRotation", "Vector3D", "",0,0,0
					Property: "PostRotation", "Vector3D", "",0,0,0
					Property: "RotationActive", "bool", "",1
					Property: "RotationMin", "Vector3D", "",0,0,0
					Property: "RotationMax", "Vector3D", "",0,0,0
					Property: "RotationMinX", "bool", "",0
					Property: "RotationMinY", "bool", "",0
					Property: "RotationMinZ", "bool", "",0
					Property: "RotationMaxX", "bool", "",0
					Property: "RotationMaxY", "bool", "",0
					Property: "RotationMaxZ", "bool", "",0
					Property: "InheritType", "enum", "",1
					Property: "ScalingActive", "bool", "",0
					Property: "ScalingMin", "Vector3D", "",0,0,0
					Property: "ScalingMax", "Vector3D", "",0,0,0
					Property: "ScalingMinX", "bool", "",0
					Property: "ScalingMinY", "bool", "",0
					Property: "ScalingMinZ", "bool", "",0
					Property: "ScalingMaxX", "bool", "",0
					Property: "ScalingMaxY", "bool", "",0
					Property: "ScalingMaxZ", "bool", "",0
					Property: "GeometricTranslation", "Vector3D", "",0,0,0
					Property: "GeometricRotation", "Vector3D", "",0,0,0
					Property: "GeometricScaling", "Vector3D", "",1,1,1
					Property: "MinDampRangeX", "double", "",0
					Property: "MinDampRangeY", "double", "",0
					Property: "MinDampRangeZ", "double", "",0
					Property: "MaxDampRangeX", "double", "",0
					Property: "MaxDampRangeY", "double", "",0
					Property: "MaxDampRangeZ", "double", "",0
					Property: "MinDampStrengthX", "double", "",0
					Property: "MinDampStrengthY", "double", "",0
					Property: "MinDampStrengthZ", "double", "",0
					Property: "MaxDampStrengthX", "double", "",0
					Property: "MaxDampStrengthY", "double", "",0
					Property: "MaxDampStrengthZ", "double", "",0
					Property: "PreferedAngleX", "double", "",0
					Property: "PreferedAngleY", "double", "",0
					Property: "PreferedAngleZ", "double", "",0
					Property: "LookAtProperty", "object", ""
					Property: "UpVectorProperty", "object", ""
					Property: "Show", "bool", "",1
					Property: "NegativePercentShapeSupport", "bool", "",1
					Property: "DefaultAttributeIndex", "int", "",0
					Property: "Freeze", "bool", "",0
					Property: "LODBox", "bool", "",0
					Property: "Lcl Translation", "Lcl Translation", "A+",%(x)s,%(y)s,%(z)s
					Property: "Lcl Rotation", "Lcl Rotation", "A+",0,0,0
					Property: "Lcl Scaling", "Lcl Scaling", "A+",1,1,1
					Property: "Visibility", "Visibility", "A+",1
					Property: "Color", "ColorRGB", "N",0.8,0.8,0.8
					Property: "Size", "double", "N",100
					Property: "Look", "enum", "N",1
				}
				MultiLayer: 0
				MultiTake: 1
				Shading: Y
				Culling: "CullingOff"
				TypeFlags: "Null"
				NodeAttributeName: "NodeAttribute::%(name)s_ncl1_1"
			}
			"""
	return data




