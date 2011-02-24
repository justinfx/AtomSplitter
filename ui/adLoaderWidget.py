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
from collections import deque, defaultdict
import tempfile, time, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QHttp

from PIL import Image


class AdLoader(QWidget):
	"""
	AdLoader(QWidget)
	
	Banner-style display widget.
	Rotates through a series of remote or local image
	and displays them for a certain amount of time.
	Sets a clickable link for each one that opens in
	a webbrowser.
	
	Ad data being passed in via setAdData must be of
	the following format:

	myAdData = [
				 {u'image': u'/path/to/local/image.jpg',
				  u'link': u'http://somesite.com/',
				  u'name': u'my ad #1'},
				
				 {u'image': u'http://www.coolimages.com/anotherImage.png',
				  u'link': u'http://www.anotherSite.com',
				  u'name': u'my ad #2'},

				]
				  
	"""
	
	AD_SIZE = (728, 90)
	AD_INTERVAL = 10 # seconds
	AD_BGCOLOR = "rgb(41, 41, 41)"
	
	
	def __init__(self, parent=None):
		super(AdLoader, self).__init__(parent)
		
		#
		# Setup
		#
		self._adBgColor = self.AD_BGCOLOR
		self._adSize = self.AD_SIZE
		self._adInterval = self.AD_INTERVAL
		
		self._link = None
		self._data = deque([])
		self._imageCache = {}
		self._loadFailed = defaultdict(int)
		self.__http = QHttp()
		self.__lastReqId = -1
		
		
		self._timer = QTimer(self)
		self._timer.setInterval(self._adInterval * 1000)
		
		self.setObjectName("AdLoader")
		self.resize(*self._adSize)
		self.mainLayout = QHBoxLayout(self)
		self.mainLayout.setMargin(0)
		self.adDisplay = QLabel(self)
		self.adDisplay.setObjectName("AdDisplay")
		self.adDisplay.setText("")
		self.adDisplay.setScaledContents(False)
		self.adDisplay.setTextInteractionFlags(Qt.NoTextInteraction)
		self.mainLayout.addWidget(self.adDisplay)
		
		self.setStyleSheet("#AdDisplay {background-color: %s}" % self._adBgColor)
		
#		self._page = QWebPage()
#		self._page.mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
#		self._page.mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
#		self._lastNetworkReply = None	
#		self._nam = self._page.networkAccessManager()
		
		self.adDisplay.mousePressEvent = lambda event: self.adDisplay.emit(SIGNAL("clicked"))
		
#		self.connect(self._page, SIGNAL("loadFinished(bool)"), self._loadFinished) 
#		self.connect(self._nam, SIGNAL("finished (QNetworkReply *)"), self._networkReply)

		self.connect(self.__http, SIGNAL("requestFinished (int,bool)"), self._loadFinished) 
		self.connect(self.adDisplay, SIGNAL("clicked"), self.linkClicked)
		self.connect(self._timer, SIGNAL("timeout()"), self.rotateAd)
		
	
		
	def linkClicked(self):
		""" Launch the currently set URL """
		if not self._link:
			return
		
		QDesktopServices.openUrl(self._link)
	
	def loadCurrentAd(self):
		""" Load the current Ad in the rotation """
		self.loadUrl(self._data[0]['image'])
		
	def loadUrl(self, url):
		""" 
		loadUrl(str url)
		
		Load the given ad image url into the display
		"""
		pixmap = self._imageCache.get(url, None)
		
		if pixmap:
			self.adDisplay.setPixmap(pixmap)
			link = self._data[0].get('link', None)
			self._link = QUrl(link) if link else None
		
		else:
			self._loadUrl(url)
		
	def rotateAd(self):
		""" Rotate to the next Ad in the list and display it """
		if not self._data:
			return
		
		self._data.rotate(-1)
		self.loadCurrentAd()

	def setBgColor(self, colorStr):
		""" 
		setBgColor(str colorStr)
		
		Sets the background color of the display to the given
		CSS-style color string. Can be hex, name, or rgb(r,g,b)
		format.
		"""
		self._adBgColor = colorStr
		self.setStyleSheet("#AdDisplay {background-color: %s}" % self._adBgColor)
		
	def setAdSize(self, size):
		""" 
		setAdSize(tuple size)
		
		Set the Ad display size in (width, height) pixels
		"""
		self._adSize = size

	def setAdData(self, data):
		""" 
		setAdData(list data)
		
		Set the Ad data to rotate through

		Format:
			myAdData = [
						 {u'image': u'/path/to/local/image.jpg',
						  u'link': u'http://somesite.com/',
						  u'name': u'my ad #1'},
						
						 {u'image': u'http://www.coolimages.com/anotherImage.png',
						  u'link': u'http://www.anotherSite.com',
						  u'name': u'my ad #2'},
		
						]		
		"""
		active = self._timer.isActive()
		if active:
			self._timer.stop()

		self._data = deque(data)
		
		if active:
			self._timer.start()
	
	def setAdInterval(self, seconds):
		""" 
		setAdInterval(float seconds)
		
		Set how many seconds each ad should display, before
		rotating to the next.
		"""
		self._adInterval = seconds*1000
		self._timer.setInterval(self._adInterval)
		
	def start(self):
		""" Starts the rotator and loads the first image"""
		self.loadCurrentAd()
		self._timer.start()
	
	def stop(self):
		""" Stops the rotator """
		self._timer.stop()
		
	def _renderUrl(self, buffer):
		""" 
		Private slot
		Slot called when url has been loaded and is ready for rendering
		into the display as an image
		"""
		adSize = QSize(*self._adSize)
		
		if not buffer.isOpen():
			buffer.open(QIODevice.ReadOnly)
			
		img  = Image.open(buffer)
		temp = os.path.join(tempfile.gettempdir(), "ad_tmp_%s_%s.png" % (os.getpid(), int(time.time())))
		img.save(temp)

		pixmap = QPixmap(temp)
		pixmap = pixmap.scaled(adSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.adDisplay.setPixmap(pixmap)
		
		link = self._data[0].get('link', None)
		self._link = QUrl(link) if link else None
		
		self._imageCache[self._data[0]['image']] = pixmap 
		
		os.remove(temp)
		
					
	def _loadFinished(self, reqid, error):
		""" 
		Private slot
		Called when the url has finished loading and is 
		ready to be validated, before then starting the
		display render.
		Filters out images that have excessive loading
		errors.
		"""
		
		if reqid != self.__lastReqId:
			return
		
		errorCode  = self.__http.error()
		statusCode = self.__http.lastResponse().statusCode()
		
		if errorCode == 0 and not error:
			buffer = QBuffer()
			buffer.setData(self.__http.readAll())
			if buffer.size() > 0:
				self._renderUrl(buffer)
				self._timer.start()
				return
		
		self.stop()
		
		url = self._data[0]['image']
		print "Failed to load", url, self._loadFailed[url]

		self._loadFailed[url] += 1
		
		if self._loadFailed[url] >= 3:
			del self._data[0]
			self._loadFailed[url] = 0
			if self._data:
				self.start()
				return
		else:
			self.rotateAd()
			self._timer.start()
			return
		
		
	def _loadUrl(self, url):
		""" 
		_loadUrl(str url)
		
		Loads the given image url into the display
		"""
		self._timer.stop()
		self._link = None

#		self._page.mainFrame().load(QUrl(url))

		qurl = QUrl(url)
		self.__http.setHost(qurl.host())
		self.__lastReqId = self.__http.get(qurl.path())
		
		

#	def _networkReply(self, reply):
#		""" 
#		_networkReply(QNetworkReply reply)
#		Slot called when a url finishes loading
#		Logs the last network reply so we can check it
#		for errors later.
#		"""
#		self._lastNetworkReply = reply


if __name__ == "__main__":
	
	import sys, random, pprint, os
	
	try:
		import json
	except:
		import simplejson as json
	
	fh = open('/homes/justin/Downloads/adSource.txt', 'r')
	data = json.load(fh)
	fh.close()
	
	adData = data['config']['ads']
	random.shuffle(adData)
	app  = QApplication([])
	
	gui = AdLoader()
	gui.setAdData(adData)
	gui.setAdInterval(data['config']['interval'])
	gui.start()
	gui.show()
	gui.activateWindow()
	
	sys.exit(app.exec_())	
				
