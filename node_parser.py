import sys
import json
import os
from zipfile import ZipFile
from os import path as pat
from shutil import copy

def not_empty(a_list):
    return len(a_list) != 0
def get_file_extension(path):
    return pat.splitext(path)[-1]
class node:
    nodes = {}
    counter = 0
    def get(path):
        if node.nodes.get(path,None):
            return node.nodes[path]
        return None
                     
    def __init__(self,path,node_name):
        self.id = node.counter
        self.child = [None,None]
        self.src = []
        self.path = path
        self.node_name = node_name
        node.nodes[pat.join(path,node_name)] = self
        node.counter += 1
        
    def set_childL(self,child):
        self.child[0] = child
    def set_childR(self,child):
        self.child[1] = child
        
    def add_src(self,src):
        self.src.append(src)
        
    def get_json(self):
        default_dict = {
                "nodeid":self.id,
                "video":"0x00",
                "audio":"0x00",
                "pic":"0x00",
                "childNodeL":'',
                "childNodeR":'',
                }
        video_candiate = list(filter(lambda x: x.find('.mp4') != -1,self.src))
        audio_candiate = list(filter(lambda x: x.find('.mp3') != -1,self.src))
        picture_candiate = list(filter(lambda x: x.find('.jpg') != -1,self.src))
        if not_empty(video_candiate): default_dict['video'] = str(node.id).zfill(5)+'.mp4'
        if not_empty(audio_candiate): default_dict['audio'] = str(node.id).zfill(5)+'.mp3'
        if not_empty(picture_candiate): default_dict['pic'] = str(node.id).zfill(5)+'.jpg'
        if self.child[0]: default_dict['childNodeL'] = self.child[0].id
        if self.child[1]: default_dict['childNodeR'] = self.child[1].id
        # print(json.dumps(default_dict))
        return default_dict

def unzip_file(file_name,output):
    with ZipFile(file_name, 'r') as zip:
        zip.extractall(output)

root_path: str = './unzipped'
file_to_unzip = sys.argv[1]
unzip_file(file_to_unzip,root_path)
output_folder = './output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for path, dirs, files in os.walk(root_path,topdown=True):
    if not node.get(path):
        _ = node(*pat.split(path))

    visiting_node = node.nodes[path]
    for dir in dirs:
        if not visiting_node.child[0]:
            visiting_node.set_childL( node(path,dir) )
        elif not visiting_node.child[1]: 
            visiting_node.set_childR( node(path,dir) )
        # print(pat.join(root,dir))
    for file in files:
        if file.find('.') == 0:
            continue
        node.nodes[path].add_src(pat.join(path,file))

if True:
    output_path = pat.realpath(pat.join(root_path,'..',output_folder))
    json_info = {"Product":"StoryBook",
                 "DataStructure":"BinaryTree",
                 "node_nums":len(node.nodes),
                 "root_nodeid":"0000",
                "node":[]
            }
    for path,node in node.nodes.items():
        print(path,node.id)
        for src in node.src:
            src_extension = get_file_extension(src)
            src_path_output = pat.join( output_path\
                                           ,str(node.id).zfill(5)+src_extension)
            copy(src,src_path_output)
        json_info['node'].append(node.get_json())


print(json.dumps(json_info))
