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
		name=str(url.split('/')[-1])
		destination=os.path.join(self.destfolder, name)
		r=requests.get(url, allow_redirects=True)
		open(name, 'wb').write(r.content)
		print(name)

#	def download_url(self, url):
#		# change it to a different way if you require
#		name = url.split('/')[-1]
#		dest = os.path.join(self.destfolder, name)
#		print "[%s] Downloading %s -> %s"%(self.ident, url, dest)
#		urllib.urlretrieve(url, dest)

def download(urls, destfolder, numthreads=16):
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
"/route-views.napafrica/bgpdata",
"/route-views.nwax/bgpdata",
"/route-views.telxatl/bgpdata",
"/route-views.wide/bgpdata",
"/route-views.sydney/bgpdata",
"/route-views.saopaulo/bgpdata",
"/route-views.sg/bgpdata",
"/route-views.perth/bgpdata",
"/route-views.sfmix/bgpdata",
"/route-views.soxrs/bgpdata"
]

ribDate="/2017.12/RIBS/rib.201712"
# day
# time
ribExtension="00.bz2"



for point in vantagePoints:
	for day in range(1,30):
		for time in range(0,23,2):
			finalurl=routeViews+point+ribDate+str(day).zfill(2) + "."+str(time).zfill(2)+ribExtension
			RibUrls.append(finalurl)

download(RibUrls, "/ribs_from_script")
