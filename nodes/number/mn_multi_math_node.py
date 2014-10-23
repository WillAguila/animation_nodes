import bpy, random
from bpy.types import Node
from mn_cache import getUniformRandom
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling
from mn_utils import *

class mn_MultiMathNode(Node, AnimationNode):
	bl_idname = "mn_MultiMathNode"
	bl_label = "Multi Math"
	node_category = "Math"
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_FloatSocket", "1.")
		self.inputs.new("mn_FloatSocket", "2.")
		self.inputs.new("mn_EmptySocket", "...")
		self.outputs.new("mn_FloatSocket", "Result")
		allowCompiling()
		
	def draw_buttons(self, context, layout):
		row = layout.row(align = True)
	
		newSocket = row.operator("mn.add_multi_math_socket", text = "New", icon = "PLUS")
		newSocket.nodeTreeName = self.id_data.name
		newSocket.nodeName = self.name
		
		removeSocket = row.operator("mn.remove_multi_math_socket", text = "Remove", icon = "X")
		removeSocket.nodeTreeName = self.id_data.name
		removeSocket.nodeName = self.name
		
	def update(self):
		forbidCompiling()
		socket = self.inputs.get("...")
		if socket is not None:
			links = socket.links
			if len(links) == 1:
				link = links[0]
				fromSocket = link.from_socket
				originSocket = getOriginSocket(socket)
				self.id_data.links.remove(link)
				if originSocket is not None:
					if originSocket.dataType in ["Float", "Integer"]:
						self.inputs.remove(socket)
						newSocketName = str(len(self.inputs) + 1) + "."
						newSocket = self.inputs.new("mn_FloatSocket", newSocketName)
						self.inputs.new("mn_EmptySocket", "...")
						self.id_data.links.new(newSocket, fromSocket)
				
		allowCompiling()
		
	def execute(self, inputs):
		output = {}
		result = 0
		for identifier, value in inputs.items():
			if identifier != "...":
				result += value
				
		output["Result"] = result
		return output
		
	def newInputSocket(self):
		forbidCompiling()
		newSocketName = newSocketName = str(len(self.inputs)) + "."
		newSocket = self.inputs.new("mn_FloatSocket", newSocketName)
		self.inputs.move(len(self.inputs) - 1, len(self.inputs) - 2)
		allowCompiling()
		
	def removeInputSocket(self):
		forbidCompiling()
		if len(self.inputs) > 2:
			self.inputs.remove(self.inputs[len(self.inputs) - 2])
		allowCompiling()
		

class AddMultiMathSocket(bpy.types.Operator):
	bl_idname = "mn.add_multi_math_socket"
	bl_label = "Add Multi Math Socket"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	
	def execute(self, context):
		node = getNode(self.nodeTreeName, self.nodeName)
		node.newInputSocket()
		return {'FINISHED'}
		
class RemoveMultiMathSocket(bpy.types.Operator):
	bl_idname = "mn.remove_multi_math_socket"
	bl_label = "Remove Multi Math Socket"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	
	def execute(self, context):
		node = getNode(self.nodeTreeName, self.nodeName)
		node.removeInputSocket()
		return {'FINISHED'}