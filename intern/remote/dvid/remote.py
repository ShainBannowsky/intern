"""
# Copyright 2017 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
from intern.remote import Remote
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import json
import math

LATEST_VERSION = 'v0'
HOST = 'host'


class DVIDRemote(Remote):

	def __init__(self, cfg_file_or_dict=None, version=None):
		Remote.__init__(self,cfg_file_or_dict)
		if version is None:
			version = LATEST_VERSION

	def get_cutout(IP, IDrepos, xpix, ypix, zpix, xo, yo, zo):
	    #ID MUST BE STRING ""
	    #SCALE MUST BE STRING "" - "GRAYSCALE"
	    #TYPEV MUST BE STRING "" - "RAW"
	    #SHAPE MUST BE STRING "" - 'XY'
	    #self.resource = resource
	    # self.resolution = resolution
	    # self.x_range = x_range
	    # self.y_range = y_range
	    # self.z_range = z_range
	    #shape = "xy"
	    #xpix = "x" how many pixels traveled in x
	    #ypix = "y" how many pixels traveled in y
      	#zpix = "z" how many pixels traveled in z
	    #xo, yo, zo (x,y,z offsets)
	    #type = "raw"
	    #scale = "grayscale"
	    size = str(xpix) + "_" + str(ypix) + "_" +str(zpix)
	    offset = str(xo) + "_" + str(yo) + "_" + str(zo)
	    ID, repos = IDrepos

	    #User entered IP address with added octet-stream line to obtain data from api in octet-stream form
	    #0_1_2 specifies a 3 dimensional octet-stream "xy" "xz" "yz"
	    address = IP + "/" + ID + "/" + repos + "/raw" + "/0_1_2/" + size + "/" + offset + "/octet-stream" 
	    r = requests.get(address)
	    octet_stream = r.content

	    #Converts obtained octet-stream into a numpy array of specified type uint8
	    entire_space = np.fromstring(octet_stream,dtype=np.uint8)

	    #Specifies the 3 dimensional shape of the numpy array of the size given by the user
	    entire_space2 = entire_space.reshape(zpix,ypix,xpix)
	    #Returns a 3-dimensional numpy array to the user
	    return entire_space2


	def create_project(api, typename,dataname,version=0):
		#Creates a repository for the data to be placed in.
		#Returns randomly generated 32 character long UUID
		p = requests.post(api + "/api/repos")
		UUID = p.content
		return (api,UUID)

	def create_cutout(api,UUID,typename,dataname,version=0):
		#Creates an instance which works as a sub-folder where the data is stored
		#Must specify:
		#typename(required) = "uint8blk", "labelblk", "labelvol", "imagetile"
		#dataname(required) = "example1"
		#version(required) = "1"
		#The size of the space reserved must be a cube with sides of multiples of 32

		dat1 = requests.post(api + "/api/repo/" + UUID + "/instance", 
			json = ({"typename" : typename,
				"dataname" : dataname,
				"versioned" : version
		}))
		res = requests.post(
			"http://34.200.231.1/api/node/" + UUID + "/Luis3/raw/0_1_2/{}_{}_{}/{}_{}_{}/".format(
				x,y,z,32,32,32
				),
			data=octet_streams
			)
		return("Your data has been uploaded to the cutout in " + dataname)

	def get_info(UUID):
		#Returns JSON for just the repository with given root UUID.  The UUID string can be
		#shortened as long as it is uniquely identifiable across the managed repositories.
		availability = requests.get("http://34.200.231.1/api/repo/" + UUID + "/info")
		avalM = availability.content
		return(avalM)

	def get_log(UUID):
		#The log is a list of strings that will be appended to the repo's log.  They should be
		#descriptions for the entire repo and not just one node.  For particular versions, use
		#node-level logging (below).
		log = requests.get("http://34.200.231.1/api/node/" + UUID + "/log")
		logM = log.content
		return(logM)

	def post_log(UUID,log1):
		#Allows the user to write a short description of the content in the repository
		#{ "log": [ "provenance data...", "provenance data...", ...] }
		log = requests.post("http://34.200.231.1/api/node/" + UUID + "/log",
			json = {"log" : [log1] })
		return("The log has been updated.")