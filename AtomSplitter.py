#!/usr/bin/env python

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

import time, random
from os import path
from datetime import datetime
from math import tan, radians
from collections import defaultdict
from functools import partial


try:
	import json
except:
	import simplejson as json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QHttp

from templates import fbx_template, chan2terragen, chan2action

from ui.chanToFbxUI import Ui_MainWindow
from ui.adLoaderWidget import AdLoader

############################################################# 
#############################################################
######## ChanConvert
############################################################# 
############################################################# 
class ChanConvert(object):
	"""
	Given a .chan file, class will perform the conversion
	to FBX format. Defaults assume 24 fps at 2k Full aperature
	resolution, and can be overridden during init.
	Also supports optional .obj file, which should be exported
	from a nuke pointCloud.
	"""
	
	DEFAULT_FPS = 24
	DEFAULT_WIDTH = 2048
	DEFAULT_HEIGHT = 1556
	DEFAULT_FILMWIDTH = 24.576
	DEFAULT_FILMHEIGHT = 18.672
	DEFAULT_SCALEVALUE = 1.0
	
	VERSION = "1.6.2"
	
	def __init__(self, chanFile, objFile=None, **kwargs):
		""" 
		__init__(str chanFile, objFile=None, **kwargs)
			
			str chanFile - path to .chan file
			str objFile - path to nuke exported pointcloud .obj file
			
		Default values can be set with the following keywords:
			int fps		  - frames per second (default 24)
			int width		- frame resolution width (default 2048)
			int height	   - frame resolution height (default 1556)
			float filmWidth  - horizontal aperature in millimeters (default 24.576)
			float filmHeight - vertical aperature in millimenters (default 18.672)
			bool doAction  -  If True, export a Flame .action file instead
			float scaleValue - scales translate by given amount (default 1.0)
			
		"""
		self.__chanFile = ChanFile(chanFile)
		self.__objFile  = objFile
		
		self.__fps = kwargs.get('fps', self.DEFAULT_FPS)
		self.__width = kwargs.get('width', self.DEFAULT_WIDTH)
		self.__height = kwargs.get('height', self.DEFAULT_HEIGHT)
		self.__filmWidth = kwargs.get('filmWidth', self.DEFAULT_FILMWIDTH)
		self.__filmHeight = kwargs.get('filmHeight', self.DEFAULT_FILMHEIGHT)
		self.__scaleValue = kwargs.get('scaleValue', self.DEFAULT_SCALEVALUE)
		
		
		self.__outFormat = kwargs.get('format', 'fbx')
		if self.__outFormat.lower() == 'tgd':
			self.__outFormat = 'terragen'
			
	
	def getTemplate(self, data={}):
		""" 
		getTemplate(dict data={}) -> str
		
		Returns the fbx template string, optional rendered
		using given dictionary values.
		
		"""
		
		dataType = self.__chanFile.getType()
		
		if data:
			
			if self.__objFile:
				pointData = self._objToFbxData()
				data['totalObjCount']   += len(pointData)
				data['totalModelCount'] += len(pointData)	
				
				template = fbx_template.getTemplate(objectType=dataType, 
													objectData=pointData)
			else:
				template = fbx_template.getTemplate(objectType=dataType)
			
			return template % data
		
		return fbx_template.getTemplate(dataType)


	def keyDataToString(self):
		""" 
		keyDataToString() -> str
		
		Returns the 'Models animation' section of the FBX format.
		Keys from chan file are parsed and converted ot the string format.
		"""
		
		if self.__chanFile.getType() == 'camera':
			objectName = 'camera1'
		else:
			objectName = 'null1'

		keyCount = self.__chanFile.totalFrames()
		keyData  = self.__chanFile.getKeyData()
		start, finish = self.__chanFile.getFrameRange()
		
		dataList = []
		dataList.append('\t\tModel: "Model::%s" {\n\t\t\tVersion: 1.1' % objectName)
		
		dataList.append('\t\t\tChannel: "Transform" {')
		
		for i, c1 in enumerate('tr'):
			
			dataList.append('\t\t\t\tChannel: "%s" {' % c1.upper())
	
			for c2 in 'xyz':
				key = '%s%s' % (c1, c2)
				dataList.append('\t\t\t\t\tChannel: "%s" {' % c2.upper())
				dataList.append('\t\t\t\t\t\tDefault: 0\n\t\t\t\t\t\tKeyVer: 4005\n\t\t\t\t\t\tKeyCount: %s' % keyCount)
				dataList.append('\t\t\t\t\t\tKey:')
				
				# keys loop
				for k in xrange(start, finish+1):
				
					val	 = keyData[k][key]
					if c1 == 't':
						val *= self.__scaleValue
					
					fbxTime = self.getFbxTime(k, self.__fps)
					
					if k == finish:
						lineterm = ''
					else:
						lineterm = ','
					
					dataList.append('\t\t\t\t\t\t\t%s,%s,L%s' % (fbxTime, val, lineterm))
				
				dataList.append('\t\t\t\t\t\tColor: 1,1,1')
				dataList.append('\t\t\t\t\t}')
				
			dataList.append('\t\t\t\t\tLayerType: %s' % str(i+1))
			dataList.append('\t\t\t\t}')
		
		dataList.append('\t\t\t}')
		
		# camera only
		if self.__chanFile.getType() == 'camera':
			default = self.getFovToFocalLength(self.__filmHeight, keyData[start]['fov'])
			dataList.append('\t\t\tChannel: "FocalLength" {')
			dataList.append('\t\t\t\tDefault: %s\n\t\t\t\tKeyVer: 4005\n\t\t\t\tKeyCount: %s' % (default, keyCount))
			
			# keys loop
			dataList.append('\t\t\t\tKey:')
			for k in xrange(start, finish+1):
			
				val	 = self.getFovToFocalLength(self.__filmHeight, keyData[k]['fov'])
				fbxTime = self.getFbxTime(k, self.__fps)

				if k == finish:
					lineterm = ''
				else:
					lineterm = ','
						
				dataList.append('\t\t\t\t\t%s,%s,L%s' % (fbxTime, val, lineterm))			
			
			dataList.append('\t\t\t\tColor: 1,1,1')
			dataList.append('\t\t\t}')
		
		dataList.append('\t\t}')
		
		return '\n'.join(dataList)
			
			
	def setFps(self, fps):
		""" 
		setFps(int fps) -> void
		
		Set the fps used in the output FBX
		"""
		self.__fps = fps

	def writeFbx(self, outfile=''):
		""" 
		writeFbx(str outfile) -> str fileWritten
		
		Main method which processes the chan file and writes out
		the FBX file to the given filename. If no filename is
		given, FBX is written with the same name in the same
		directory as source.
		Returns the filename that was actually written out, in-case
		the file existed already and had to be renamed.
		
			str outfile - full .fbx filepath to write out
		"""

		if self.__outFormat != 'fbx' and self.__chanFile.getType() != 'camera':
			raise Exception("Non-camera .chan files are only supported by the FBX output format.")
			
					
		# setup
		keyData = self.__chanFile.getKeyData()

		now = datetime.now()		
		start, finish = self.__chanFile.getFrameRange()
		width, height = (self.__width, self.__height)
		
		fov = filmWidth = filmHeight = 0
		if self.__chanFile.getType() == 'camera':
			filmWidth, filmHeight = (self.__filmWidth, self.__filmHeight)
			fov = keyData[start]['fov']
						
		data = dict( date_timestamp = now.strftime('%Y-%m-%d %H:%M:%S:000'),
					 date_ctime	 = now.ctime(),
					 date_year		= now.year,
					 date_month		= now.month,
					 date_day		= now.day,
					 date_hour		= now.hour,
					 date_minute	= now.minute,
					 date_second	= now.second,
					 aspect			= float(width) / height,
					 fps			= self.__fps,
					 width		  = width,
					 height		 = height,
					 start		  = start,
					 finish		 = finish,
					 
					filmWidth	= filmWidth,
					filmHeight	= filmHeight,
					fov			= fov,
					focalLength	= self.getFovToFocalLength(filmHeight, fov),
					 )

		data['totalObjCount'] = 2
		data['totalModelCount'] = 1
		
		
		safeData = defaultdict(str)
		safeData.update(data)
		data = safeData
		

			
		#
		# action
		#
		if self.__outFormat == 'action':
			converter = chan2action.ChanToAction(self.__chanFile.getFileName(), 
												 objfile = self.__objFile,
												 **data)
			rendered = converter.convert()
			ext = 'action'
	
	
		#
		# terragen
		#
		elif self.__outFormat == 'terragen':
			converter = chan2terragen.ChanToTerragen(self.__chanFile, data, scale=self.__scaleValue)
			rendered = converter.convert()
			ext = 'tgd'
	
	
		#
		# fbx
		#
		else:

			# format
			animData = self.keyDataToString()
			
			data.update( dict( fbxTime_start  = self.getFbxTime(start, self.__fps),
							   fbxTime_end	  = self.getFbxTime(finish, self.__fps),
							   animationData  = animData,
							) )

			if self.__chanFile.getType() == 'camera':
				
				data.update( dict(
								filmWidth	= filmWidth / 25.4,
								filmHeight	= filmHeight / 25.4,
								rotationOrder = 4, #ZXY, nuke default
								) )		
						
			rendered = self.getTemplate(data)
			ext = 'fbx'
		
		# write
		if not outfile:
			outfile = self._getOutFile(self.__chanFile.getFileName(), ext=ext)
			
		fh = open(outfile, 'w')
		fh.write(rendered)
		fh.write('\n')
		fh.close()
		
		return outfile


	def _getOutFile(self, infile, ext='fbx'):
		"""
		
		"""
		outfile = '%s.%s' % (path.splitext(infile)[0], ext)
		
		if path.isfile(outfile):
			base, ext = path.splitext(outfile)
			i = 1
			newFile = '%s_%s%s' % (base, i, ext)
			
			while path.isfile(newFile):
				i += 1
				newFile = '%s_%s%s' % (base, i, ext)
			
			outfile = newFile
	
		return outfile


	def _objToFbxData(self):
		"""
		
		"""
		if not self.__objFile:
			return ""
		
		data = open(self.__objFile).readlines()
		if not data or data[0] != '## OBJ file generated by Nuke ##\n':
			raise Exception("%s is not a nuke-generated obj" % self.__objFile)
		
		filtered = [line.strip() for line in data if line.startswith('v ')]
		
		pointData = []
		for line in filtered:
			try:
				x,y,z = line.split()[1:]
			except:
				continue
			pointData.append((x,y,z))	
		
		outData = []
		template = fbx_template.nullType()

		vals = {'name' : 'PointCloud', 'x' : 0, 'y' : 0, 'z' : 0}
		nullString = template % vals
		outData.append({'name' : 'PointCloud', 'parent' : 'Scene', 'data' : nullString})

		for i, point in enumerate(pointData):
			name = 'locator%d' % (i+1)
			x,y,z = point
			vals = {'name' : name, 
					'x' : float(x) * self.__scaleValue, 
					'y' : float(y) * self.__scaleValue, 
					'z' : float(z) * self.__scaleValue}
			nullString = template % vals
			outData.append({'name' : name, 'parent' : 'PointCloud', 'data' : nullString})
		
		return outData

		
			
	@staticmethod
	def getFbxTime(t, fps):
		""" 
		getFbxTime(float t, int fps) -> int 
		
		Gets the FBX time from a given frame and fps,
		per FBX SDK specifications
		
			float t - frame time
			int fps - frames per second
		"""
		frame = float(t)
		val = int(0.5 + ((frame/fps) * 46186158000))
		return val
	
	@staticmethod
	def getFovToFocalLength(aperature, fov):
		"""
		getFovToFocalLength(float aperature, float fov) -> float
		
		Given an aperature in millimeters, and a field of view in degress,
		returns the focal length in millimeters
		
			float aperature - film aperature in millimeters
			float fov	   - field of view in degrees
		"""
		focalLength = aperature / (2 * tan( radians(fov / 2) ) )
		return focalLength
	
	
############################################################# 
#############################################################
######## ChanFile
############################################################# 
############################################################# 
class ChanFile(object):
	"""
	Class represnting a .chan file.
	Can parse file into usable data.
	
	Supports two 'types' of detected chan files: null or camera
	A null only has Transform XYZ and Rotate XYZ, while a 
	camera has a 7th column for FOV.
	"""
	
	def __init__(self, chanFile):
		""" 
		__init__(str chanFile)
		
			str chanFile - path to .chan file
		"""
		self.__chanFile = chanFile
		
		self.__keyData	  = None
		self.__frameRange = None
		self.__totalKeys  = None
		
		self.type = ""
		
		if not path.isfile(chanFile):
			raise IOError("Given .chan file does not exist: %s" % chanFile)
		
	def getFileName(self):
		""" Return the name of .chan file """
		return self.__chanFile
	
	def getFrameRange(self):
		""" Return the frame range parsed from file as (int start, int end) """
		if self.__frameRange == None:
			self.parse()
			
		return self.__frameRange
	
	def getKeyData(self, redundant=True):
		""" Return the keys parsed from file as a structured dictionary """
		if not self.__keyData:
			self.parse()
			
		return self.__keyData

	def getType(self):
		""" Get the type of chan file data. Can either be 'null' or 'camera' """
		if not self.type:
			self.parse()
		
		return self.type
	
	def parse(self):
		""" Parses the chan file. Run automatically if needed by other methods """
		try:
			fh = open(self.__chanFile, 'r')
		except:
			raise IOError("Failed to read .chan file: %s" % self.__chanFile)
		
		self.__keyData = {}
		
		while True:
			line = fh.readline()
			if not line: break
			if not line.strip(): continue
			
			columns = line.strip().split()
			if len(columns) == 7:
				self.type = 'null'
				frame, tx, ty, tz, rx, ry, rz = columns
			else:
				self.type = 'camera'
				frame, tx, ty, tz, rx, ry, rz, fov = columns
			
			self.__keyData[int(frame)] = dict( frame = int(frame),
											   tx	= float(tx),
											   ty	= float(ty),
											   tz	= float(tz),
											   rx	= float(rx),
											   ry	= float(ry),
											   rz	= float(rz),
											   )
			if self.type == 'camera':
				self.__keyData[int(frame)]['fov'] = float(fov)
			
		fh.close()
	
		keys = sorted(self.__keyData.keys())
		self.__totalKeys = len(keys)
		
		if keys:
			self.__frameRange = (keys[0], keys[-1])

		
	def totalFrames(self):
		""" Return the total number of frames parsed from chan file as int """
		if not self.__totalKeys:
			self.parse()
			
		return self.__totalKeys

		
############################################################# 
#############################################################
######## ChanConverGUI
############################################################# 
############################################################# 
class ChanConverGUI(QMainWindow, Ui_MainWindow):
	"""

	"""
	
	AD_DATA_SOURCE = "http://cmivfx.com/AtomSplitter/banners/adSource.txt"
	AD_DATA_HOST = 'www.cmivfx.com'
	
	
	
	def __init__(self, parent=None, **kwargs):
		super(ChanConverGUI, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("AtomSplitter v%s" % ChanConvert.VERSION)
		
		self.__prevDir = None
		self.__chatLoaded = False
		
		self.setStatusBar(None)
		
		self.toolButtons = QButtonGroup(self)
		self.toolButtons.addButton(self.settingsBtn)
		self.toolButtons.addButton(self.chatBtn)
		self.toolButtons.addButton(self.aboutBtn)

		self.fileTypeButtons = QButtonGroup(self)
		self.fileTypeButtons.addButton(self.radioFbx, 0)
		self.fileTypeButtons.addButton(self.radioAction, 1)
		self.fileTypeButtons.addButton(self.radioTerragen, 2)
		
		numValidator   = QRegExpValidator(QRegExp(r'\d+'), self)
		floatValidator = QRegExpValidator(QRegExp(r'\d+\.?\d*'), self)
		self.widthField.setValidator(numValidator)
		self.heightField.setValidator(numValidator)
		self.hfaField.setValidator(floatValidator)
		self.vfaField.setValidator(floatValidator)
		self.fpsField.setValidator(floatValidator)
	
		def focusEvent(event):
			self._objFieldClicked()
			QLineEdit.focusInEvent(self.objFileField, event)
			
		self.objFileField.focusInEvent = focusEvent

		websettings = self.chatView.settings()
		websettings.setAttribute(websettings.PluginsEnabled,True)
				
		# tool tips
		self.__toolTips = {}
		self.__toolTips['chan'] = "In Nuke, select your desired Camera node and press its 'export chan file' " \
								  "button. Save this camera data as a .chan file"
		self.__toolTips['obj'] = "In Nuke, create a WriteGeo node and connect it to the output of your pointCloud " \
								 "node. From this node, export the pointCloud geometry to an .obj file"
		self.__toolTips['out'] = ".fbx or .action file to be exported after conversion"
		self.__toolTips['fbx'] = "Output filetype is FBX format"
		self.__toolTips['action'] = "Output filetype is .action format for Flame"
		self.__toolTips['tgd'] = "Output filetype is TGD format for Terragen"
		self.__toolTips['scale'] = "Translation values are scaled by this number (multiplied)"

		self.objFileField.mouseMoveEvent = partial(self._setInfoLine, 'obj')
		self.objFileButton.mouseMoveEvent = partial(self._setInfoLine, 'obj')
		self.sourceFileField.mouseMoveEvent = partial(self._setInfoLine, 'chan')
		self.sourceFileButton.mouseMoveEvent = partial(self._setInfoLine, 'chan')
		self.outFileField.mouseMoveEvent = partial(self._setInfoLine, 'out')
		self.outFileButton.mouseMoveEvent = partial(self._setInfoLine, 'out')
		
		self.radioFbx.mouseMoveEvent = partial(self._setInfoLine, 'fbx')
		self.radioAction.mouseMoveEvent = partial(self._setInfoLine, 'action')
		self.radioTerragen.mouseMoveEvent = partial(self._setInfoLine, 'tgd')
		
		self.scaleField.mouseMoveEvent = partial(self._setInfoLine, 'scale')
		
		self.groupBox.mouseMoveEvent = partial(self._setInfoLine, '')

		
		# ad widget
		self.adWidget = AdLoader(self)
		self.adFrameLayout.addWidget(self.adWidget)
	
		# form values
		self.sourceFileField.setText(kwargs.get('chan', ""))
		self.widthField.setText(str(kwargs.get('width', ChanConvert.DEFAULT_WIDTH)))
		self.heightField.setText(str(kwargs.get('height', ChanConvert.DEFAULT_HEIGHT)))
		self.hfaField.setText(str(kwargs.get('filmWidth', ChanConvert.DEFAULT_FILMWIDTH)))
		self.vfaField.setText(str(kwargs.get('filmHeight', ChanConvert.DEFAULT_FILMHEIGHT)))
		self.fpsField.setText(str(kwargs.get('fps', ChanConvert.DEFAULT_FPS)))
		self.scaleField.setText(str(kwargs.get('scaleValue', ChanConvert.DEFAULT_SCALEVALUE)))
		
		if kwargs.get('doAction', False):
			self.radioAction.setChecked(True)
		
		# connections
		self.connect(self.quitButton, SIGNAL("clicked()"), self.close)
		self.connect(self.convertButton, SIGNAL("clicked()"), self.convert)
		self.connect(self.sourceFileButton, SIGNAL("clicked()"), self.setSourceFile)
		self.connect(self.objFileButton, SIGNAL("clicked()"), self.setObjFile)
		self.connect(self.outFileButton, SIGNAL("clicked()"), self.setOutFile)
		self.connect(self.sourceFileField, SIGNAL("textChanged(const QString&)"), self._syncOutFile)
		self.connect(self.fileTypeButtons, SIGNAL("buttonClicked(int)"), self.fileTypeChanged)
		self.connect(self.cmiSmallButton, SIGNAL("clicked()"), self._linkToCMI)
		self.connect(self.cmiLogoButton, SIGNAL("clicked()"), self._linkToCMI)
		
		cbk = partial(self.stack.setCurrentIndex, 0)
		self.connect(self.settingsBtn, SIGNAL("clicked()"), cbk)
		cbk = partial(self.stack.setCurrentIndex, 1)
		self.connect(self.aboutBtn, SIGNAL("clicked()"), cbk)	
#		cbk = partial(self.stack.setCurrentIndex, 2)
		self.connect(self.chatBtn, SIGNAL("clicked()"), self._chatButton_Clicked)
		
		QTimer.singleShot(1, self._initDelayed)
	
	
	def closeEvent(self, event):
		self.adWidget.stop()	
		super(ChanConverGUI, self).closeEvent(event)
			
	def _initDelayed(self):
		""" """
		#
		# Ads
		#
		self.__http = QHttp()
		self.__http.setHost(self.AD_DATA_HOST)
		self.__httpID = None
		
		self.connect(self.__http, SIGNAL("requestFinished(int,bool)"), self._initAdWidget)
		self.__httpID = self.__http.get(self.AD_DATA_SOURCE)
		

	def _initAdWidget(self, id, error):
		""" """
		if id != self.__httpID:
			return
		
		resp = self.__http.lastResponse()
		if resp.statusCode() != 200:
			return
		
		strData = str(self.__http.readAll())
		data = json.loads(strData)
		adData = data['config']['ads']
		random.shuffle(adData)
		
		self.adWidget.setAdData(adData)
		self.adWidget.setAdInterval(data['config']['interval'])
		self.adWidget.start()	

	def _chatButton_Clicked(self, *args, **kwargs):
		""" """
		self.stack.setCurrentIndex(2)
		
		if not self.__chatLoaded:
			self._initChatWidget()
			self.__chatLoaded = True
		
		
	def _initChatWidget(self):
		""" """
		#
		# Chat
		#
		chatSize = self.stack.size()
		chatCode = """ 
		<iframe src="http://cdn.livestream.com/embed/cmivfx?layout=3&autoPlay=false" 
				width="%(width)s" height="%(height)s" style="border:0;outline:0" 
				frameborder="0" scrolling="no" marginheight="0" marginwidth="0">
		Requires Mozilla Flash Player version 10
		</iframe>
		""" % {'width' : chatSize.width()-25, 'height' : chatSize.height()-25}
		
		self.chatView.setHtml(chatCode)
				
	def convert(self):
		""" """
		error = ""
		for field in (self.widthField, self.heightField, 
						self.hfaField, self.vfaField, 
						self.fpsField, self.sourceFileField, self.outFileField,
						self.scaleField):
			
			if not str(field.text()).strip():
				error = "All fields must be filled in!"
				break
		
		if not error and not path.isfile(str(self.sourceFileField.text())):
			error = "Source .chan file does not exist!"

		if error:
			msg = QMessageBox(self)
			msg.setText(error)
			msg.exec_()
			return
		
		if self.objFileField.text() == '[Optional]':
			self.objFileField.clear()
		
		format = 'fbx'
		formatID = self.fileTypeButtons.checkedId()
		if formatID == 1:
			format = 'action'
		elif formatID == 2:
			format = 'tgd'
			
		# do the convert
		converter = ChanConvert(str(self.sourceFileField.text()),
								objFile = str(self.objFileField.text()),
								fps = float(str(self.fpsField.text())),
								width = int(str(self.widthField.text())),
								height = int(str(self.heightField.text())),
								filmWidth = float(str(self.hfaField.text())),
								filmHeight = float(str(self.vfaField.text())),
								format = format,
								scaleValue = float(str(self.scaleField.text())))
		
		try:
			written = converter.writeFbx(str(self.outFileField.text()))	
		except Exception, e:
			doneMsg = "Failed with the following:\n\n%s" % str(e)
		else:
			doneMsg = "Wrote out:\n\n%s" % written
		
		msg = QMessageBox(self)
		msg.setText(doneMsg)
		msg.exec_()
					
		
	def fileTypeChanged(self, id):
		""" """
		val = str(self.outFileField.text())

		self.objFileField.setEnabled(True)
		self.objFileButton.setEnabled(True)
			
		if id == 0:
			out = "%s.fbx" % path.splitext(val)[0]
		elif id == 1:
			out = "%s.action" % path.splitext(val)[0]	
		else:
			self.objFileField.setEnabled(False)
			self.objFileButton.setEnabled(False)
			out = "%s.tgd" % path.splitext(val)[0]		
		
		if val:
			self.outFileField.setText(out)
		
	def setSourceFile(self):
		""" """
		
		if self.__prevDir:
			homedir = self.__prevDir
		else:
			homedir = QDir.toNativeSeparators( QDir.homePath() )
			
		filename = QFileDialog.getOpenFileName(self, "Source .chan file",
												homedir, "Chan File (*.chan)")
		
		self.__prevDir = path.dirname(str(filename))
		
		if filename:
			self.sourceFileField.setText(filename)

	def setObjFile(self):
		""" """
		
		if self.__prevDir:
			homedir = self.__prevDir
		else:
			homedir = QDir.toNativeSeparators( QDir.homePath() )
			
		filename = QFileDialog.getOpenFileName(self, "Source PointCloud .obj file",
												homedir, "Nuke Obj File (*.obj)")
		
		self.__prevDir = path.dirname(str(filename))
		
		if filename:
			self.objFileField.setText(filename)
					
	def setOutFile(self):
		""" """
		filterStr = "FBX (*.fbx)"
		if self.radioAction.isChecked():
			filterStr = "Action (*.action)"
		elif self.radioTerragen.isChecked():
			filterStr = "Terragen (*.tgd)"
					
		if self.__prevDir:
			homedir = self.__prevDir
		else:
			homedir = ""
				
		filename = QFileDialog.getSaveFileName(self, "Output file",
												homedir, filterStr)
		
		self.outFileField.setText(filename)

	def _objFieldClicked(self):
		""" """
		if self.objFileField.text() == '[Optional]':
			self.objFileField.clear()

	def _linkToCMI(self):
		""" """
		
		service = QDesktopServices()
		service.openUrl(QUrl("http://cmivfx.com/"))
			
	def _syncOutFile(self):
		""" """
		val = str(self.sourceFileField.text())
		
		if self.radioAction.isChecked():
			out = "%s.action" % path.splitext(val)[0]
		elif self.radioTerragen.isChecked():
			out = "%s.tgd" % path.splitext(val)[0]
		else:
			out = "%s.fbx" % path.splitext(val)[0]
			
		self.outFileField.setText(out)

	def _setInfoLine(self, typeName, *args, **kwargs):
		""" """
		self.infoLine.setText(self.__toolTips.get(typeName, ''))
		

		
	
if __name__ == "__main__":
	
	import sys, optparse


	class OptParser(optparse.OptionParser):
		def error(self, msg):
			raise Exception("Parsing error: %s" % msg)		
	
		
	usage = "%prog <chan file> [out fbx file]"
	parser = OptParser(usage=usage)

	parser.add_option("-o", "--obj", default='', 
						help="Optional nuke-exported pointCloud .obj file")
	
	parser.add_option("-f", "--fps", type='int', default=24, 
						help="Set FPS rate (default 24)")
	parser.add_option("-x", "--width", type='int', default=2048, 
						help="Set frame width (default 2048)")
	parser.add_option("-y", "--height", type='int', default=1556, 
						help="Set frame height (default 1556)")				
	parser.add_option("--filmwidth", type='float', default=24.576, 
						help="Set film aperature width in mm (default 24.576)")	
	parser.add_option("--filmheight", type='float', default=18.672, 
						help="Set film aperature height in mm (default 18.672)")	
	parser.add_option("-s", "--scale", type='float', default=1.0, 
						help="Scale the translation values by this amount")	
	parser.add_option("-F", "--format", action='store', default='fbx', 
						help="Output format (fbx, action, terragen)")	
	
	parser.add_option("-a", "--action", action='store_true', default=False, 
						help="Export a Flame .action file instead of FBX (DEPRECATED)")	
	
	forceGui = False	
	runOptions = {}
	
	try:
		(options, args) = parser.parse_args()
	except Exception, e:
		forceGui = True
	
	# TODO: Deprecated support for -a flag. Remove in next version
	if options.action:
		options.format = 'action'
	
	if not forceGui:
		runOptions = dict(  objFile = options.obj, 
							fps = options.fps,
							width = options.width,
							height = options.height,
							filmWidth = options.filmwidth,
							filmHeight = options.filmheight,
							format = options.format,
							scaleValue = options.scale
							)
	
	if forceGui or not len(args):
		app  = QApplication(sys.argv)
		cGui = ChanConverGUI(**runOptions)
		cGui.show()
		cGui.activateWindow()
		sys.exit(app.exec_())
		
	
	chan = args[0]
	converter = ChanConvert(chan, **runOptions)
	
	if len(args) > 1:
		out = args[1]
	else:
		out = ''
		
	try:
		converter.writeFbx(out)	
	except Exception, e:
		raise
		parser.error(str(e))
	
	
	