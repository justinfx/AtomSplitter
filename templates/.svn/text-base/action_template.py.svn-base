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

def getTemplate(objectType = 'camera'):
	""" Returns the ACTION file template """
	
	# main template
	template = """
		Module Action
		Program flame
		Version 2010.1
		FileVersion 2
		CreationDate %(date_ctime)s
		
		FrameWidth %(width)s
		FrameHeight %(height)s
		FramePixelFormat 124
		FrameAspectRatio %(aspect)s
		FrameDominance 2
		
			MinFrame %(start)s
			CurrentFrame %(start)s
			MaxFrames %(finish)s
			ShadingMode no
			TextureMode yes
			WireframeMode no
			ZBufferMode yes
			LinetestMode no
			MultiSample no
			CurrentCamera 5
			GridMode 3
			Grid3DColour 0.3 0.3 0.3
			CameraPlaneType 0
			PlayLockMode no
			BackupMode yes
			BackupTime 30
			QuickResolution 12
			AntiAliasingLevel 0
			AntiAliasingSoftness 1
			MotionBlurEditor
				Channel 
					Extrapolation constant
					Value 1
					End
				ChannelEnd
			TopLevelChannel
				Channel scene
					Uncollapsed
					End
			ResultCamChannel
				Channel ResultCamera
					Extrapolation constant
					Value 0
					Uncollapsed
					End
				ChannelEnd
		MotionBlurPhaseChannel
				Channel phase
					Extrapolation constant
					Value 0
					Uncollapsed
					End
				ChannelEnd
			MotionBlurEnableChannel
				Channel enable
					Extrapolation constant
					Value 0
					Uncollapsed
					End
				ChannelEnd
			MotionBlurShutterChannel
				Channel shutter
					Extrapolation constant
					Value 1
					Uncollapsed
					End
				ChannelEnd
			MotionBlurSamplesChannel
				Channel samples
					Extrapolation constant
					Value 5
					Uncollapsed
					End
				ChannelEnd
				DofMode no
				DofSoftness 1
				FogMode Off
				FogColour 0 0 0
				FogStart 0
				FogEnd 1
				FogRange 1
				ProjectorMotionPathMode no
				CamMotionPathMode no
				AxisMotionPathMode no
				LightMotionPathMode no
				PropScalingMode yes
				SPropScalingMode yes
				YSnapMode no
				YGridSize 1
				AutoKeyMode yes
				UpdateMode yes
				AutoParentMode yes
				ForceProxyUpdate yes
				UndoLevels 10
				DrawIconsMode IconsOn
				IconTransparency 0
				SchematicTransparency 0
				ClipInfo 0
				SubMenu AXIS_MENU
				OutputView Result
				ColourClamping yes
				End
		
		#
		# node database
		#
		ConcreteFileVersion 1.4
		CreationDate %(date_ctime)s
		
		
		WorldScale 1
		
		Node Group
			Name scene
			Number 0
			Child 1
			Child 2
			MotionPath no
			PosX 0
			PosY 200
			Flags SCHEMATIC_HIDDEN
			Specifics
			{
			}
		End
		Node Camera
			Name camera
			Number 1
			MotionPath no
			PosX 0
			PosY 100
			Specifics
			{
				Type Free
				CamChannel
				{
				%(animPositionData)s
				Channel speed
					Extrapolation constant
					Value 0
					End
				Channel interest/x
					Extrapolation constant
					Value 0.000000000
					End
				Channel interest/y
					Extrapolation constant
					Value 0.000000000
					End
				Channel interest/z
					Extrapolation constant
					Value 0.000000000
					End
				Channel int_speed
					Extrapolation constant
					Value 0
					End
				%(animRotationData)s
				Channel roll
					Extrapolation constant
					Value 0.000000000
					End
				%(animFovData)s
				Channel near
					Extrapolation constant
					Value 1
					End
				Channel far
					Extrapolation constant
					Value 10000
					End
				Channel distance
					Extrapolation constant
					Value 1483.64
					End
				Channel lens_distortion/x
					Extrapolation constant
					Value 0
					End
				Channel lens_distortion/y
					Extrapolation constant
					Value 0
					End
				Channel lens_distortion/magnitude
					Extrapolation constant
					Value 0
					End
				Channel lens_distortion/adjustment
					Extrapolation constant
					Value 0
					End
				Channel lens_distortion/anamorph
					Extrapolation constant
					Value 1
					End
				ChannelEnd
				}
				CamLensFitRes 0
				CamLensFilter 1
				CamLensMode 0
				CamMotionPathMode no
				CamMotionPath
				{
				Path pos_path
					Dimension 3
					Closed no
					Size 0
					End
		
				Path poi_path
					Dimension 3
					Closed no
					Size 0
					End
		
				}
				CamIndex 0
				CamPhysicalParameters
				PhysicalCameraEnabled no
				FStop FStop_1
				Film_Type 35mm_Full_Frame
			}
		End
		Node Axis
			Name MasterAxis
			Number 2
			%(axisChildData)s
			MotionPath no
			PosX 0
			PosY 0
			Specifics
			{
				Channel position/x
					Extrapolation constant
					Value 0
					End
				Channel position/y
					Extrapolation constant
					Value 0
					End
				Channel position/z
					Extrapolation constant
					Value 0
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
		%(axisNodesData)s
		ConcreteEnd
		
		#
		# layers
		#
		ActionLayerFileVersion 1.4
		CreationDate %(date_ctime)s
		
		LayerCount 0
		ProxyMode PROXY_OFF
		ProcessAlpha PROCESS_NO_ALPHA
		
		LayerEnd
		
		#
		# multitracks
		#
		ActionMTFileVersion 1.4
		CreationDate %(date_ctime)s
		
		
		MultiTrackEnd
		
		#
		# drawing order
		#
		DrawingOrderFileVersion 1.0
		CreationDate %(date_ctime)s
		
		LookupTableFrame 1
			LookupTableGroup 0
				LookupTableNPath 6
			LookupTableGroup 1
				LookupTableNPath 5
			LookupTableGroup 2
				LookupTableNPath 4
			LookupTableGroup 3
				LookupTableNPath 3
			LookupTableGroup 4
				LookupTableNPath 2
			LookupTableGroup 5
				LookupTableNPath 1
			LookupTableGroup 6
				LookupTableNPath 0
			LookupTableGroup 7
				LookupTableNPath 7
		DrawingOrderEnd
	"""
	template = template.replace('\n\t\t', '\n').lstrip()
	
	return template


		
