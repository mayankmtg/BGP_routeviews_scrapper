import requests
import os
import sys
import threading
from Queue import Queue
import urllib


class DownloadThread(threading.Thread):
	def __init__(self, queue, destfolder):
		super(DownloadThread, self).__init__()
		self.queue = queue
		self.destfolder = destfolder
		self.daemon = True
	def run(self):
		while True:
			url = self.queue.get()
			try:
				self.download_url(url)
			except Exception,e:
				print "   Error: %s"%e
			self.queue.task_done()

	def download_url(self,url):
		vantage_folder=str(url.split('/')[3])
		name=str(url.split('/')[-1])
		destination="./"+vantage_folder+"/"+name
		print(destination)
		r=requests.get(url, allow_redirects=True)
		open(destination, 'wb').write(r.content)
		print(name)

#	def download_url(self, url):
#		# change it to a different way if you require
#		name = url.split('/')[-1]
#		dest = os.path.join(self.destfolder, name)
#		print "[%s] Downloading %s -> %s"%(self.ident, url, dest)
#		urllib.urlretrieve(url, dest)

def download(urls, destfolder, numthreads=30):
	queue = Queue()
	for url in urls:
		queue.put(url)
	for i in range(numthreads):
		t = DownloadThread(queue, destfolder)
		t.start()
	queue.join()




RibUrls=[]
routeViews="http://archive.routeviews.org"
vantagePoints=[
"/bgpdata",
"/route-views3/bgpdata",
"/route-views4/bgpdata",
"/route-views6/bgpdata",
"/route-views.eqix/bgpdata",
"/route-views.isc/bgpdata",
"/route-views.kixp/bgpdata",
"/route-views.jinx/bgpdata",
"/route-views.linx/bgpdata",
#"/route-views.napafrica/bgpdata",
#"/route-views.nwax/bgpdata",
"/route-views.telxatl/bgpdata",
"/route-views.wide/bgpdata",
"/route-views.sydney/bgpdata",
"/route-views.saopaulo/bgpdata",
"/route-views.sg/bgpdata",
"/route-views.perth/bgpdata",
"/route-views.sfmix/bgpdata",
"/route-views.soxrs/bgpdata"
]

ribDate=["/2013.12/RIBS/rib.20131231.0000.bz2","/2014.12/RIBS/rib.20141231.0000.bz2","/2015.12/RIBS/rib.20151231.0000.bz2","/2016.12/RIBS/rib.20161231.0000.bz2","/2017.12/RIBS/rib.20171231.0000.bz2"]



for point in vantagePoints:
	try:
		os.stat(point.split('/')[1])
	except:
		os.mkdir(point.split('/')[1])
	for yr in ribDate:
		finalurl=routeViews+point+yr
		RibUrls.append(finalurl)

download(RibUrls, "/ribs_from_script")
