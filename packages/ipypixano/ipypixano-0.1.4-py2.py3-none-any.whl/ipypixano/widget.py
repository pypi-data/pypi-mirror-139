#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nicolas allezard.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""


from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Bool, validate, TraitError,Int,List,Dict,Bytes,Any
from ipywidgets.widgets.trait_types import (
    bytes_serialization,
    _color_names,
    _color_hex_re,
    _color_hexa_re,
    _color_rgbhsl_re,
)
from ._frontend import module_name, module_version


import numpy as np
import base64
import cv2
import copy


from pathlib import Path
from urllib.request import urlopen
from PIL import Image
import io

def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return img

def writeb64(img):
    """Encode matrix to base64 image string"""
    retval, buffer = cv2.imencode('.png', img)
    pic_str = base64.b64encode(buffer)
    pic_str = pic_str.decode()
    return pic_str

@register
class Pixano(DOMWidget, ValueWidget):
    _model_name = Unicode('PixanoModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('PixanoView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    element=Unicode('').tag(sync=True)

    image= Any().tag(sync=True) 

    mode=Unicode('none').tag(sync=True)

    shapes_in=List([]).tag(sync=True)
    shapes=List([]).tag(sync=True)
    selectedShapeIds=List([]).tag(sync=True)
    current_category=Unicode('').tag(sync=True)
    categories_colors=Dict().tag(sync=True)

    
    mask=Unicode('').tag(sync=True)
    targetClass=Int(1).tag(sync=True)
    clsMap=Dict().tag(sync=True)
    maskVisuMode=Unicode('INSTANCE').tag(sync=True)



    @validate('element')
    def _valid_element(self, proposal):
        valid_elem=["pxn-rectangle","pxn-segmentation","pxn-smart-rectangle","pxn-smart-segmentation","pxn-polygon",'pxn-graph']
        #print("element",proposal["value"])
        # if not proposal['value'] in valid_elem:
        #     raise TraitError('Invalid element: must be one of '+",".join(valid_elem))
        return proposal["value"]


    @validate('image')
    def _valid_image(self, proposal):
        #print(type(proposal['value']))
        if isinstance(proposal['value'], str):
            #print("string")
            filename=proposal['value']
            if 'https' in filename:
                data=urlopen(filename).read()
                data = base64.b64encode(data).decode()
            else:
                abs_filename=Path(filename).absolute().as_posix()
                #print(abs_filename)

                data=urlopen("file://"+abs_filename).read()
                data = base64.b64encode(data).decode()
            return data
        elif str(type(proposal['value']))== "<class 'numpy.ndarray'>" :
            #print("array")
            img_b64=writeb64(proposal['value'])
            return img_b64
            
        elif isinstance(proposal['value'],Image.Image):
            #print("pil image")
            img_byte_arr = io.BytesIO()
            proposal['value'].save(img_byte_arr, format='PNG')
            return base64.b64encode(img_byte_arr.getvalue()).decode()
        else:
            raise TraitError('Invalid type: must be a string, a numpy ndarray or a PIL image, but receive '+str(type(proposal['value'])))
        return None

    def getMask(self):
        if self.mask!='':
            img=readb64(self.mask)
            return img
        else:
            return None

    # def setImage(self,img):
    #     print("setImage")

    #     img_b64=writeb64(img)
    #     print(img_b64)
        
    #     #self.image_data=img_b64

    def clearShapes(self):
        #print("python in",self.shapes_in)
        self.shapes_in=copy.deepcopy([])

    def setShapes(self,new_shape=[]):
        self.shapes_in=copy.deepcopy(new_shape)