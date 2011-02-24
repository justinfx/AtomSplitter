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


import sys
from time import localtime, strftime
from collections import deque

class ChanToAction(object):
	"""
	Class ChanToAction
	
	Methods for converting an input nuke .chan file into
	a flame .action format. Optionally can accept a nuke-exported
	.obj file containing pointCloud data, to be included in the
	action file.
	
	"""
	SCALE = 100
	WIDTH = 1920
	HEIGHT = 1080
	FRAME_PIXEL_FORMAT = 124
	FRAME_ASPECT_RATIO = 1.777780175
	
	
	def __init__(self, chanfile, objfile=None, **kwargs):
		"""
		Args:
			str chanfile - .chan file for camera data
			str objfile - optional .obj file of pointcloud export
			
			int width - frame width
			int height - frame height
			float aspect - pixel aspect ratio		
		"""
		self.__result = []
		self.__cDate = strftime("%a %b %d %H:%M:%S %Y ", localtime())
		self.__sourceLines = []
		
		self.__childCount = 0
		
		self.chanfile = chanfile
		self.objfile  = objfile
		
		self.width = kwargs.get('width', self.WIDTH)
		self.height = kwargs.get('height', self.HEIGHT)
		self.framePixelFormat = self.FRAME_PIXEL_FORMAT
		self.frameAspectRatio = kwargs.get('aspect', self.FRAME_ASPECT_RATIO)	
		self.scale = self.SCALE	
	
	def convert(self):
		"""
		convert() -> string 
		Generates the .action output and returns a string
		"""
		self.__cDate = strftime("%a %b %d %H:%M:%S %Y ", localtime())
		self.__sourceLines = open(self.chanfile, 'r').readlines()
		self.__childCount = 0
		
		result = self.__result

		#-------------- Header -----------------
		self._outputHeader()
		
		#-------------- Node Group --------------
		self._outputNodeGroup()  
	
		result.append( "Node Camera\n")
		result.append( "\tName camera\n")
		result.append( "\tNumber 1\n")
		result.append( "\tMotionPath no\n")
		result.append( "\tPosX 0\n")
		result.append( "\tPosY 100\n")
		result.append( "\tSpecifics\n")
		result.append( "\t{\n")
		result.append( "\t\tType Free\n")
		result.append( "\t\tCamChannel\n")
		result.append( "\t\t{\n")
		
		for i in 'xyz':
			self._outputChannel("\t\t", "t%s" % i, "position/%s" % i)

		self._outputSingleValue("\t\t", "speed", 0 )
		self._outputSingleValue("\t\t", "interest/x", 0.000000000 )
		self._outputSingleValue("\t\t", "interest/y", 0.000000000 )
		self._outputSingleValue("\t\t", "interest/z", 0.000000000 )	
		self._outputSingleValue("\t\t", "int_speed", 0 )	
		
		for i in ('xyz'):
			self._outputChannel("\t\t", "r%s" % i, "rotation/%s" % i, -1 )

		self._outputSingleValue("\t\t", "roll", 0.000000000 )
		self._outputChannel("\t\t", "fov", "fov", 1 )
		self._outputSingleValue("\t\t", "near", 1 )
		self._outputSingleValue("\t\t", "far", 10000 )
		self._outputSingleValue("\t\t", "distance", 1483.64 )
		self._outputSingleValue("\t\t", "lens_distortion/x", 0 )
		self._outputSingleValue("\t\t", "lens_distortion/y", 0 )
		self._outputSingleValue("\t\t", "lens_distortion/magnitude", 0 )
		self._outputSingleValue("\t\t", "lens_distortion/adjustment", 0)
		self._outputSingleValue("\t\t", "lens_distortion/anamorph", 1 )

		result.append( "\t\tChannelEnd\n")
		result.append( "\t\t}\n")
		result.append( "\t\tCamLensFitRes 0\n")
		result.append( "\t\tCamLensFilter 1\n")
		result.append( "\t\tCamLensMode 0\n")
		result.append( "\t\tCamMotionPathMode no\n")
		result.append( "\t\tCamMotionPath\n")
		result.append( "\t\t{\n")
		result.append( "\t\tPath pos_path\n")
		result.append( "\t\t\tDimension 3\n")
		result.append( "\t\t\tClosed no\n")
		result.append( "\t\t\tSize 0\n")
		result.append( "\t\t\tEnd\n\n")
		result.append( "\t\tPath poi_path\n")
		result.append( "\t\t\tDimension 3\n")
		result.append( "\t\t\tClosed no\n")
		result.append( "\t\t\tSize 0\n")
		result.append( "\t\t\tEnd\n\n")
		result.append( "\t\t}\n")
		result.append( "\t\tCamIndex 0\n")
		result.append( "\t\tCamPhysicalParameters\n")
		result.append( "\t\tPhysicalCameraEnabled no\n")
		result.append( "\t\tFStop FStop_1\n")
		result.append( "\t\tFilm_Type 35mm_Full_Frame\n")	
		result.append( "\t}\n")
		result.append( "End\n")
				
		#-------------- Axis Nodes -------------
		self._outputFromObjFile()
		
		#-------------- Footer -----------------
		self._outputFooter()
		
		
		return ''.join(result)

		
	def _outputHeader(self):	
		"""
		Builds header info for .action format
		"""
		result = self.__result
		
		result.append( "Module Action\n" )
		result.append( "Program flame\n" )
		result.append( "Version 2010.1\n" )
		result.append( "FileVersion 2\n")
		result.append( "CreationDate " +self.__cDate +"\n\n")
		result.append( "FrameWidth "+str(self.width)+"\n")
		result.append( "FrameHeight "+str(self.height)+"\n")
		result.append( "FramePixelFormat "+str(self.framePixelFormat)+"\n")	
		result.append( "FrameAspectRatio "+str(self.frameAspectRatio)+"\n")
		result.append( "FrameDominance 2\n\n")	
		result.append( "\tMinFrame " + (self.__sourceLines[0].split())[0] + "\n")
		result.append( "\tCurrentFrame " + (self.__sourceLines[(len(self.__sourceLines)-1)].split())[0] + "\n") # i will use the last frame
		result.append( "\tMaxFrames " + str(len(self.__sourceLines)) + "\n")
		result.append( "\tShadingMode no\n" )
		result.append( "\tTextureMode yes\n" )
		result.append( "\tWireframeMode no\n" )
		result.append( "\tZBufferMode yes\n" )
		result.append( "\tLinetestMode no\n" )
		result.append( "\tMultiSample no\n" )
		result.append( "\tCurrentCamera 5\n" )
		result.append( "\tGridMode 3\n" )
		result.append( "\tGrid3DColour 0.3 0.3 0.3\n" )
		result.append( "\tCameraPlaneType 0\n" )
		result.append( "\tPlayLockMode no\n" )
		result.append( "\tBackupMode yes\n" )
		result.append( "\tBackupTime 30\n" )
		result.append( "\tQuickResolution 12\n" )
		result.append( "\tAntiAliasingLevel 0\n" )
		result.append( "\tAntiAliasingSoftness 1\n" )
		result.append( "\tMotionBlurEditor\n")
		result.append( "\t\tChannel\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 1\n")
		result.append( "\t\t\tSize 3\n")
		result.append( "\t\t\tKeyVersion 1\n")
		result.append( "\t\t\tKey 0\n")
		result.append( "\t\t\t\tFrame 50\n")
		result.append( "\t\t\t\tValue 1\n")
		result.append( "\t\t\t\tFrameLock yes\n")
		result.append( "\t\t\t\tDeleteLock yes\n")
		result.append( "\t\t\t\tInterpolation hermite\n")
		result.append( "\t\t\t\tEnd\n")
		result.append( "\t\t\tKey 1\n")
		result.append( "\t\t\t\tFrame 100\n")
		result.append( "\t\t\t\tValue 1\n")
		result.append( "\t\t\t\tInterpolation hermite\n")
		result.append( "\t\t\t\tEnd\n")
		result.append( "\t\t\tKey 2\n")
		result.append( "\t\t\t\tFrame 150\n")
		result.append( "\t\t\t\tValue 1\n")
		result.append( "\t\t\t\tFrameLock yes\n")
		result.append( "\t\t\t\tDeleteLock yes\n")
		result.append( "\t\t\t\tInterpolation hermite\n")
		result.append( "\t\t\t\tEnd\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "\tTopLevelChannel\n")
		result.append( "\t\tChannel scene\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\tResultCamChannel\n")
		result.append( "\t\tChannel ResultCamera\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 0\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "MotionBlurPhaseChannel\n")
		result.append( "\t\tChannel phase\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 0\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "\tMotionBlurEnableChannel\n")
		result.append( "\t\tChannel enable\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 0\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "\tMotionBlurShutterChannel\n")
		result.append( "\t\tChannel shutter\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 1\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "\tMotionBlurSamplesChannel\n")
		result.append( "\t\tChannel samples\n")
		result.append( "\t\t\tExtrapolation constant\n")
		result.append( "\t\t\tValue 5\n")
		result.append( "\t\t\tUncollapsed\n")
		result.append( "\t\t\tEnd\n")
		result.append( "\t\tChannelEnd\n")
		result.append( "\t\tDofMode no\n")
		result.append( "\t\tDofSoftness 1\n")
		result.append( "\t\tFogMode Off\n")
		result.append( "\t\tFogColour 0 0 0\n")
		result.append( "\t\tFogStart 0\n")
		result.append( "\t\tFogEnd 1\n")
		result.append( "\t\tFogRange 1\n")
		result.append( "\t\tProjectorMotionPathMode no\n")
		result.append( "\t\tCamMotionPathMode no\n")
		result.append( "\t\tAxisMotionPathMode no\n")
		result.append( "\t\tLightMotionPathMode no\n")
		result.append( "\t\tPropScalingMode yes\n")
		result.append( "\t\tSPropScalingMode yes\n")
		result.append( "\t\tYSnapMode no\n")
		result.append( "\t\tYGridSize 1\n")
		result.append( "\t\tAutoKeyMode yes\n")
		result.append( "\t\tUpdateMode yes\n")
		result.append( "\t\tAutoParentMode yes\n")
		result.append( "\t\tForceProxyUpdate yes\n")
		result.append( "\t\tUndoLevels 10\n")
		result.append( "\t\tDrawIconsMode IconsOn\n")
		result.append( "\t\tIconTransparency 0\n")
		result.append( "\t\tSchematicTransparency 0\n")
		result.append( "\t\tClipInfo 0\n")
		result.append( "\t\tSubMenu AXIS_MENU\n")
		result.append( "\t\tOutputView Result\n")
		result.append( "\t\tColourClamping yes\n")
		result.append( "\t\tEnd\n\n")
		result.append( "#\n")
		result.append( "# node database\n")
		result.append( "#\n")
		result.append( "ConcreteFileVersion 1.4\n")
		result.append( "CreationDate " +self.__cDate+"\n\n\n")
		result.append( "WorldScale 1\n\n");
	
	def _outputNodeGroup(self):	
		"""
		Builds Node Group info for .action format
		"""
		result = self.__result
		
		result.append( "Node Group\n")
		result.append( "\tName scene\n")
		result.append( "\tNumber 0\n")
		
		result.append( "\tChild 1\n")
		self.__childCount += 1
		if self.objfile:
			result.append( "\tChild 2\n")
			self.__childCount += 1
		
		result.append( "\tMotionPath no\n")
		result.append( "\tPosX 0\n")
		result.append( "\tPosY 200\n")
		result.append( "\tFlags SCHEMATIC_HIDDEN\n")
		result.append( "\tSpecifics\n")
		result.append( "\t{\n")
		result.append( "\t}\n")
		result.append( "End\n")
	
		
	def _outputChannel(self, prefix, Attr, discAttr, globalScale=None):
		"""
		Builds a block of info representing channel data 
		"""
		result = self.__result
		sourceFileLines = self.__sourceLines
		if globalScale == None:
			globalScale = self.scale
		
		result.append( prefix+"Channel " +discAttr +"\n" )
	
		if (Attr == "tx") :
			attributeToRead = 1
		if (Attr == "ty") :
			attributeToRead = 2
		if (Attr == "tz") : 
			attributeToRead = 3
		if (Attr == "rx") : 
			attributeToRead = 4
		if (Attr == "ry") : 
			attributeToRead = 5
		if (Attr == "rz") : 
			attributeToRead = 6
		if (Attr == "fov") : 
			attributeToRead = 7
		
		result.append( prefix+"\tExtrapolation constant\n")
		tempS = sourceFileLines[(len(sourceFileLines)-1)].split()
	
		# here since i used the first frame for current frame i will use the value for the first frame
		result.append( prefix+"\tValue "+ str(float(tempS[attributeToRead]) * globalScale) +"\n" ) 
		result.append( prefix+"\tSize "+str(len(sourceFileLines))+"\n" )
		result.append( prefix+"\tKeyVersion 1\n" )
		key = 0
		#loop that goes through all lines and parses specified text
		for line in sourceFileLines:
			tempS = line.split()
			result.append( prefix+"\tKey "+str(key)+"\n" )
			result.append( prefix+"\t\tFrame "+tempS[0]+"\n" )	
			result.append( prefix+"\t\tValue "+(str(float(tempS[attributeToRead]) * globalScale))+"\n")
			result.append( prefix+"\t\tInterpolation hermite\n" )
			result.append( prefix+"\t\tEnd\n" )
			key = key + 1
			
		result.append( prefix+"\tEnd\n" )
		
	def _outputSingleValue(self, prefix, discAttr, value ):
		"""
		Builds a single line channel value
		"""
		result = self.__result
		result.append( prefix+"Channel " +discAttr +"\n" )
		result.append( prefix+"\tExtrapolation constant\n" )
		result.append( prefix+"\tValue "+str(value)+"\n" )
		result.append( prefix+"\tEnd\n" )
		
	def _outputFooter(self):	
		"""
		Builds footer info for .action format
		"""
		result = self.__result	
		result.append( "ConcreteEnd\n\n")
	
		#-------------- Layers -----------------
		result.append( "#\n")
		result.append( "# layers\n")
		result.append( "#\n")
		result.append( "ActionLayerFileVersion 1.4\n")
		result.append( "CreationDate " +self.__cDate +"\n\n")
	
		result.append( "LayerCount 2\n")
		result.append( "ProxyMode PROXY_OFF\n")
		result.append( "ProcessAlpha PROCESS_NO_ALPHA\n\n")
	
		result.append( "Layer 0\n")
		result.append( "\tFrontClipName 	\"(None)\"\n")
		result.append( "\tFrontClipUID 0 0 0\n")
		result.append( "\tFrontClipSlip 0\n")
		result.append( "\tFrontMode 1\n")
		result.append( "\tMatteClipName 	\"(None)\"\n")
		result.append( "\tMatteClipUID 0 0 0\n")
		result.append( "\tMatteClipSlip 0\n")
		result.append( "\tMatteMode 1\n")
		result.append( "\tFrontLock -1\n")
		result.append( "\tCropMode no\n")
		result.append( "\tCropSoftnessMode no\n")
		result.append( "\tFilterMode ACTION_BLUR_BOX\n")
		result.append( "\tProxyMode no\n")
		result.append( "\tProcessAlpha PROCESS_NO_ALPHA\n")
		result.append( "\tFrameMode AS_INPUT\n")
		result.append( "\tPredivide no\n")
		result.append( "\tResWidth "+str(self.width)+"\n")
		result.append( "\tResHeight "+str(self.height)+"\n")
		result.append( "\tResPixelFormat "+str(self.framePixelFormat)+"\n")
		result.append( "\tResAspect "+str(self.frameAspectRatio)+"\n")
	
		result.append( "\tResScanMode SCAN_FORMAT_FRAME\n")
		result.append( "\tCCFActive yes\n")
		result.append( "\tCCMActive yes\n")
		result.append( "\tKeyerActive yes\n")
		result.append( "\tAnimation\n")
		self._outputSingleValue( "\t\t", "slip", 0 )
		self._outputSingleValue( "\t\t", "matte_slip", 0 )
		self._outputSingleValue( "\t\t", "blur/x", 0 )
		self._outputSingleValue( "\t\t", "blur/y", 0 )
		self._outputSingleValue( "\t\t", "blur/mx", 0 )
		self._outputSingleValue( "\t\t", "blur/my", 0 )
		self._outputSingleValue( "\t\t", "shadowSoftness", 0 )
		result.append( "\t\tChannelEnd\n")
		result.append( "End\n")
		result.append( "LayerEnd\n\n")
	
		#-------------- multitracks -----------------
		result.append( "#\n")
		result.append( "# multitracks\n")
		result.append( "#\n")
		result.append( "ActionMTFileVersion 1.4\n")
		result.append( "CreationDate " +self.__cDate +"\n\n\n")
		result.append( "Layer 0\n")
		result.append( "\tEnd\n")
		result.append( "MultiTrackEnd\n\n")
	
		#-------------- Drawing order -----------------
		result.append( "#\n")
		result.append( "# drawing order\n")
		result.append( "#\n")
		result.append( "DrawingOrderFileVersion 1.0\n")
		result.append( "CreationDate " +self.__cDate +"\n\n")
	
		result.append( "LookupTableFrame 1\n")
		result.append( "\tLookupTableGroup 0\n")
		result.append( "\t\tLookupTableNPath 2\n")
		result.append( "\tLookupTableGroup 1\n")
		result.append( "\t\tLookupTableNPath 1\n")
		result.append( "DrawingOrderEnd\n")


	def _outputFromObjFile(self):
		"""
		Builds the group of axis nodes from the obj file,
		if one was specified during init.
		"""
		
		if not self.objfile:
			return
		
		data = open(self.objfile).readlines()
		if not data or data[0] != '## OBJ file generated by Nuke ##\n':
			raise Exception("%s is not a nuke-generated obj" % self.objfile)
		
		filtered = [line.strip() for line in data if line.startswith('v ')]
		
		pointData = []
		for line in filtered:
			try:
				x,y,z = line.split()[1:]
			except:
				continue
			pointData.append((x,y,z))
		
		total = len(pointData)
		if not total:
			return
		
		nodeNum = 2
		childrenIds = range(nodeNum+1, nodeNum+1+total)
		
		pointCloud = self._getAxisString('PointCloudAxis', nodeNum, childs=childrenIds)
		self.__result.append(pointCloud+'\n')
		nodeNum += 1
		
		xVals = deque( (-212, -106, 0, 106, 212) )
		yVal  = -86
		firstX = xVals[0]
		firstY = yVal
		
		for x,y,z in pointData:
			x = float(x) * self.scale
			y = float(y) * self.scale
			z = float(z) * self.scale
			axis = self._getAxisString('point%iAxis' % (nodeNum-2), nodeNum, 
										x=x, y=y, z=z,
										xPos=xVals[0], yPos=yVal)
		
			self.__result.append(axis+'\n')
			nodeNum += 1
			
			xVals.rotate(-1)
			if xVals[0] == firstX:
				yVal += firstY
		

	def _getAxisString(self, name, id, x=0, y=0, z=0, xPos=0, yPos=0, childs=[]):
		"""
		Builds the individual axis block info from given values.
		"""		
		vals = {'name' : name, 'id' : id, 
				'x' : x, 'y' : y, 'z' : z, 
				'xPos' : xPos, 'yPos' : yPos}
		
		childStrs = []
		for child in childs:
			childStrs.append('\tChild %s' % child)
		
		vals['childStr'] = ''
		if childStrs:
			vals['childStr'] = "\n%s" % ('\n'.join(childStrs))
		
		axisTemplate = """
		Node Axis
			Name %(name)s
			Number %(id)s%(childStr)s
			MotionPath no
			PosX %(xPos)s
			PosY %(yPos)s
			Specifics
			{
				Channel position/x
					Extrapolation constant
					Value %(x)s
					End
				Channel position/y
					Extrapolation constant
					Value %(y)s
					End
				Channel position/z
					Extrapolation constant
					Value %(z)s
					End
				Channel speed
					Extrapolation constant
					Value 0
					End
				Channel rotation/x
					Extrapolation constant
					Value 0
					End
				Channel rotation/y
					Extrapolation constant
					Value 0
					End
				Channel rotation/z
					Extrapolation constant
					Value 0
					End
				Channel scaling/x
					Extrapolation constant
					Value 100
					End
				Channel scaling/y
					Extrapolation constant
					Value 100
					End
				Channel scaling/z
					Extrapolation constant
					Value 100
					End
				Channel shearing/x
					Extrapolation constant
					Value 0
					End
				Channel shearing/y
					Extrapolation constant
					Value 0
					End
				Channel shearing/z
					Extrapolation constant
					Value 0
					End
				Channel centre/x
					Extrapolation constant
					Value 0
					End
				Channel centre/y
					Extrapolation constant
					Value 0
					End
				Channel centre/z
					Extrapolation constant
					Value 0
					End
				ChannelEnd
				Path position
					Dimension 3
					Closed no
					Size 0
					End
		
				MBlur yes
				Global no
			}
		End
		""".strip().replace('\n\t\t', '\n')
		
		return axisTemplate % vals
		
		
		
		
		
		
		
	
	
	
		
