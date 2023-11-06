import numpy as np
import random
import sys
import datetime
import pya

recommend_unit_nm = 50000 # 50um
cell_name_maze = "MAZE"
maze_origin_xy = (0,0)
METAL5_LABEL_TEXT = None
METAL5_PAD_LABEL_TEXT = None


# please don't touch.
base_unit_nm = 180 # GF180.
base_unit_num = 8 # 1 mezu block unit of num
metal_width_unit_num = 2 # meze wall(metal) width size by unit
metal5_layer_num1 = 81
metal5_layer_num2 = 0
metal5_label_layer_num1 = 81
metal5_label_layer_num2 = 10
pad_layer_num1 = 37
pad_layer_num2 = 0
pad_label_layer_num1 = 37
pad_label_layer_num2 = 10


start_goal_position = {
	'left_above' : 0, 
	'right_above' : 1,
	'right_below' : 2,
	'left_below' : 3
}
maze_obj_list = {
	'wall' : 0,
	'road' : 1,
	'out' : 2,
	'start' : 3,
	'goal' : 4,
	'empty' : 99,
}

class MazeCreater():
	def __init__(self, size_w, size_h):
		self.size_w = int(size_w / 2)
		self.size_h = int(size_h / 2)

		self.roadfiller =RoadFiller()
		self.GDS_generater = GDS_Generater()
	
	def generate_maze(self):
		n_w = 2 * self.size_w + 1
		n_h = 2 * self.size_h + 1

		field = np.zeros((n_h, n_w), dtype=np.uint8)

		x = 2* np.random.randint(0, self.size_w) + 1
		y = 2* np.random.randint(0, self.size_h) + 1

		field = self.roadfiller.fill_with_road(
			field, x, y
			)
		
		field_out = field.copy()

		return field_out

class RoadFiller:
	def __init__(self):
		self.reach_goal = False

	def fill_with_road(
		self, field, x, y
		):

		if self.reach_goal is True:
			return field

		self.field = field.copy()
		
		if self.field[y, x] == 0:
			self.field[y, x] = maze_obj_list["road"]

		xy_history = [(x, y)]

		while True:
			res, x, y, self.field = self.extend_road(
				self.field, x, y
				)

			if res == 'stretched':
				xy_history.append((x, y))
				continue

			if res == 'deadend':
				break
		
		xy_history.pop(-1)
		xy_history.reverse()
		for xy in xy_history:
			x = xy[0]
			y = xy[1]
			self.fill_with_road(
				self.field, x, y
				)
		
		return self.field

	def extend_road(
		self, field, x, y
		):
		dd = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1),
		]

		n_h, n_w = field.shape[:2]
		next_field = field.copy()
		id_brank = 0

		dd_res = [''] * 4
		for id_dir in range(4):
			x1 = x + dd[id_dir][0] * 2
			y1 = y + dd[id_dir][1] * 2
			x0 = x + dd[id_dir][0]
			y0 = y + dd[id_dir][1]

			if x1 < 0 or n_w <= x1:
				dd_res[id_dir] = 'out'
				continue

			if y1 < 0 or n_h <= y1:
				dd_res[id_dir] = 'out'
				continue

		   
			if (field[y1, x1] == id_brank):
				dd_res[id_dir] = 'brank'
				continue
				

			dd_res[id_dir] = 'no'

		ids_dir = [i for i, x in enumerate(dd_res) if x == 'brank']
		if len(ids_dir) > 0:
			res = 'stretched'
			id_dir = random.sample(ids_dir, 1)[0]

			x1 = x + dd[id_dir][0] * 2
			y1 = y + dd[id_dir][1] * 2
			x0 = x + dd[id_dir][0]
			y0 = y + dd[id_dir][1]
			next_field[y1, x1] = maze_obj_list["road"]
			next_field[y0, x0] = maze_obj_list["road"]
			next_x = x1
			next_y = y1

			return res, next_x, next_y, next_field

		res = 'deadend'
		next_x = None
		next_y = None
		return res, next_x, next_y, next_field


class GDS_Generater():

	debug_ary = []

	def generate(
		self,
		field,
		unit,
		start_position,
		goal_position,
		layout,
		cell
		):

		h, w = field.shape
		SG_position = []
		SG_position.append((1, 1))
		SG_position.append((w - 2, 1))
		SG_position.append((w - 2, h - 2))
		SG_position.append((1, h - 2))

		start_xy = SG_position[start_position]
		goal_xy = SG_position[goal_position]

		for i in range(h):
			for j in range(w):
				if field[i][j] == maze_obj_list["road"]:
					self.debug_ary.append("R")
					continue
				
				dir_obj = {
					'above' : maze_obj_list["empty"],
					'below' : maze_obj_list["empty"],
					'right' : maze_obj_list["empty"],
					'left' : maze_obj_list["empty"]
				}

				above_xy = (j, i-1)
				below_xy = (j, i+1)
				right_xy = (j+1, i)
				left_xy = (j-1, i)
				loc_xy = (j, i)

				# start & goal
				if start_position == start_goal_position['left_above']:
					if loc_xy[0] == start_xy[0] - 1 and loc_xy[1] == start_xy[1]:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] and loc_xy[1] == start_xy[1] - 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] - 1 and loc_xy[1] == start_xy[1] - 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif start_position == start_goal_position['right_above']:
					if loc_xy[0] == start_xy[0] and loc_xy[1] == start_xy[1] - 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] +1 and loc_xy[1] == start_xy[1]:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] +1 and loc_xy[1] == start_xy[1] - 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif start_position == start_goal_position['right_below']:
					if loc_xy[0] == start_xy[0] + 1 and loc_xy[1] == start_xy[1]:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] and loc_xy[1] == start_xy[1] + 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] + 1 and loc_xy[1] == start_xy[1] + 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif start_position == start_goal_position['left_below']:
					if loc_xy[0] == start_xy[0] - 1 and loc_xy[1] == start_xy[1]:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] and loc_xy[1] == start_xy[1] + 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == start_xy[0] - 1 and loc_xy[1] == start_xy[1] + 1:
						self.generate_start_side_block(start_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue

				if goal_position == start_goal_position['left_above']:
					if loc_xy[0] == goal_xy[0] - 1 and loc_xy[1] == goal_xy[1]:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] and loc_xy[1] == goal_xy[1] - 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] - 1 and loc_xy[1] == goal_xy[1] - 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif goal_position == start_goal_position['right_above']:
					if loc_xy[0] == goal_xy[0] and loc_xy[1] == goal_xy[1] - 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] + 1 and loc_xy[1] == goal_xy[1]:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] + 1 and loc_xy[1] == goal_xy[1] - 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif goal_position == start_goal_position['right_below']:
					if loc_xy[0] == goal_xy[0] + 1 and loc_xy[1] == goal_xy[1]:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] and loc_xy[1] == goal_xy[1] + 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] + 1 and loc_xy[1] == goal_xy[1] + 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
				elif goal_position == start_goal_position['left_below']:
					if loc_xy[0] == goal_xy[0] - 1 and loc_xy[1] == goal_xy[1]:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] and loc_xy[1] == goal_xy[1] + 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue
					if loc_xy[0] == goal_xy[0] - 1 and loc_xy[1] == goal_xy[1] + 1:
						self.generate_goal_side_block(goal_position, loc_xy[0], loc_xy[1], unit, layout, cell)
						continue


				# above
				if above_xy[1] < 0:
					dir_obj["above"] = maze_obj_list["out"]
				elif field[above_xy[1]][above_xy[0]] == maze_obj_list["wall"]:
					dir_obj["above"] = maze_obj_list["wall"]
				elif field[above_xy[1]][above_xy[0]] == maze_obj_list["road"]:
					dir_obj["above"] = maze_obj_list["road"]
				else:
					print("above not match!!!")

				# below
				if below_xy[1] >= h:
					dir_obj["below"] = maze_obj_list["out"]
				elif field[below_xy[1]][below_xy[0]] == maze_obj_list["wall"]:
					dir_obj["below"] = maze_obj_list["wall"]
				elif field[below_xy[1]][below_xy[0]] == maze_obj_list["road"]:
					dir_obj["below"] = maze_obj_list["road"]
				else:
					print("below not match!!!")

				# right
				if right_xy[0] >= w:
					dir_obj["right"] = maze_obj_list["out"]
				elif field[right_xy[1]][right_xy[0]] == maze_obj_list["wall"]:
					dir_obj["right"] = maze_obj_list["wall"]
				elif field[right_xy[1]][right_xy[0]] == maze_obj_list["road"]:
					dir_obj["right"] = maze_obj_list["road"]
				else:
					print("right not match!!!")

				# left
				if left_xy[0] < 0:
					dir_obj["left"] = maze_obj_list["out"]
				elif field[left_xy[1]][left_xy[0]] == maze_obj_list["wall"]:
					dir_obj["left"] = maze_obj_list["wall"]
				elif field[left_xy[1]][left_xy[0]] == maze_obj_list["road"]:
					dir_obj["left"] = maze_obj_list["road"]
				else:
					print("left not match!!!")

				# outer corner
				if (dir_obj["above"] == maze_obj_list["out"] and 
				    dir_obj["below"] == maze_obj_list["wall"] and 
				    dir_obj["right"] == maze_obj_list["out"] and 
				    dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["out"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["out"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["out"] and 
				      dir_obj["right"] == maze_obj_list["out"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["out"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["out"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				# outer wall
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["out"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["out"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["out"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["out"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["out"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_outer_road_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["out"]):
					self.generate_outer_road_right_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["out"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_outer_road_below_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["out"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_outer_road_above_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				# inter all
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_empty_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_all_road_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				# inter 3way road
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_above_below_right_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_above_below_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_above_right_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_below_right_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				# inter 2way road
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_above_below_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_above_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_right_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_below_right_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_above_right_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_below_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				# inter 1way road
				elif (dir_obj["above"] == maze_obj_list["road"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_above_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["road"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_below_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["road"] and 
				      dir_obj["left"]  == maze_obj_list["wall"]):
					self.generate_inter_road_right_block(loc_xy[0], loc_xy[1], unit, layout, cell)
				elif (dir_obj["above"] == maze_obj_list["wall"] and 
				      dir_obj["below"] == maze_obj_list["wall"] and 
				      dir_obj["right"] == maze_obj_list["wall"] and 
				      dir_obj["left"]  == maze_obj_list["road"]):
					self.generate_inter_road_left_block(loc_xy[0], loc_xy[1], unit, layout, cell)

				else:
					debug_ary.append("E")
					print("generator not match!!!")

		self.generate_start_object(start_xy[0], start_xy[1], unit, layout, cell)
		self.generate_goal_object(goal_xy[0], goal_xy[1], unit, layout, cell)

		return self.debug_ary




	def cal_stripe_size(
			self,
			unit):
				return int(unit / base_unit_num)

	def cal_center_xy(
			self, 
			start_xy, 
			end_xy):

				center_x = 0
				center_y = 0
				if end_xy[0] - start_xy[0] > 0:
					center_x = start_xy[0] + int((end_xy[0] - start_xy[0]) / 2)
				else:
					center_x = start_xy[0] - int((start_xy[0] - end_xy[0]) / 2)

				if end_xy[1] - start_xy[1] > 0:
					center_y = start_xy[1] + int((end_xy[1] - start_xy[1]) / 2)
				else:
					center_y = start_xy[1] - int((start_xy[1] - end_xy[1]) / 2)

				center_xy = (center_x, center_y)
				return center_xy


	def create_circle_polygon(
				self,
				radius):
					nr_points = 32
					angles = np.linspace(0,2*np.pi,nr_points+1)[0:-1]
					points = []
					for ind,angle in enumerate(angles):
						points.append(pya.Point(radius*np.cos(angle),radius*np.sin(angle)))
					return pya.SimplePolygon(points)


	def generate_Metal5_cells(
				self, 
				start_xy, 
				end_xy, 
				layout,
				cell):
					center_xy = self.cal_center_xy(start_xy, end_xy)
					text_size = int(end_xy[0] - start_xy[0] / 10)

					m5 = layout.layer(metal5_layer_num1, metal5_layer_num2)
					cell.shapes(m5).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
					if METAL5_LABEL_TEXT != None:
						m5_L = layout.layer(metal5_label_layer_num1, metal5_label_layer_num2)
						cell.shapes(m5_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
						text_obj = pya.Text(METAL5_LABEL_TEXT, center_xy[0], center_xy[1])
						cell.shapes(m5_L).insert(text_obj)

					pad = layout.layer(pad_layer_num1, pad_layer_num2)
					cell.shapes(pad).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
					if METAL5_PAD_LABEL_TEXT != None:
						pad_L = layout.layer(pad_label_layer_num1, pad_label_layer_num2)
						cell.shapes(pad_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
						text_obj = pya.Text(METAL5_PAD_LABEL_TEXT, center_xy[0], center_xy[1])
						cell.shapes(pad_L).insert(text_obj)


	def cal_real_position_xy(
				self, 
				loc_x, 
				loc_y, 
				unit):

					start_xy = (maze_origin_xy[0] + (loc_x * unit), maze_origin_xy[1] + (-1 * (loc_y * unit)))
					end_xy = (maze_origin_xy[0] + ((loc_x+1) * unit), maze_origin_xy[1] + (-1 * (loc_y+1) * unit))

					return start_xy, end_xy


	def generate_above_side_Metal5(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)
					strip_size = self.cal_stripe_size(unit)
					metal_size = strip_size * metal_width_unit_num

					metal_start_xy = real_start_xy
					metal_end_xy = (real_end_xy[0], real_start_xy[1] - metal_size)

					self.generate_Metal5_cells(metal_start_xy, metal_end_xy, layout, cell)


	def generate_below_side_Metal5(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)
					strip_size = self.cal_stripe_size(unit)
					metal_size = strip_size * metal_width_unit_num

					metal_start_xy = (real_start_xy[0], real_end_xy[1] + metal_size)
					metal_end_xy = real_end_xy

					self.generate_Metal5_cells(metal_start_xy, metal_end_xy, layout, cell)


	def generate_right_side_Metal5(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)
					strip_size = self.cal_stripe_size(unit)
					metal_size = strip_size * metal_width_unit_num

					metal_start_xy = (real_end_xy[0] - metal_size, real_start_xy[1])
					metal_end_xy = real_end_xy

					self.generate_Metal5_cells(metal_start_xy, metal_end_xy, layout, cell)


	def generate_left_side_Metal5(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)
					strip_size = self.cal_stripe_size(unit)
					metal_size = strip_size * metal_width_unit_num

					metal_start_xy = real_start_xy
					metal_end_xy = (real_start_xy[0] + metal_size, real_end_xy[1])

					self.generate_Metal5_cells(metal_start_xy, metal_end_xy, layout, cell)

	def generate_block_Metal5(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)

					metal_start_xy = real_start_xy
					metal_end_xy = real_end_xy

					self.generate_Metal5_cells(metal_start_xy, metal_end_xy, layout, cell)


	def generate_empty_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("0")
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_start_side_block(
				self,
				start_position,
				loc_x,
				loc_y,
				unit,
				layout,
				cell):
					self.debug_ary.append("Y")


	def generate_goal_side_block(
				self,
				start_position,
				loc_x,
				loc_y,
				unit,
				layout,
				cell):
					self.debug_ary.append("Z")


	def generate_outer_road_right_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("1")
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_outer_road_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("2")
#					self.generate_left_side_Metal5( loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_outer_road_below_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("3")
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_outer_road_above_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("4")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_all_road_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("5")
#					self.generate_above_side_Metal5( loc_x, loc_y, unit, layout, cell)
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_below_right_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("6")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_below_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("7")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_right_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("8")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_below_right_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("9")
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_below_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("A")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("B")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_right_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("C")
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_below_right_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("D")
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_right_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("F")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)


	def generate_inter_road_below_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("G")
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_above_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("H")
#					self.generate_above_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_below_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("I")
#					self.generate_below_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_right_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("J")
#					self.generate_right_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)

	def generate_inter_road_left_block(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					self.debug_ary.append("K")
#					self.generate_left_side_Metal5(loc_x, loc_y, unit, layout, cell)
					self.generate_block_Metal5(loc_x, loc_y, unit, layout, cell)



	def generate_start_object(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)
					center_xy = self.cal_center_xy(real_start_xy, real_end_xy)

					radius = int( (real_end_xy[0] - real_start_xy[0]) * 0.8 / 2 ) 
					circle = self.create_circle_polygon(radius)
					circle.move(center_xy[0], center_xy[1])

					m5 = layout.layer(metal5_layer_num1, metal5_layer_num2)
					cell.shapes(m5).insert(circle)
#					m5_L = layout.layer(metal5_label_layer_num1, metal5_label_layer_num2)
#					cell.shapes(m5_L).insert(circle)

					pad = layout.layer(pad_layer_num1, pad_layer_num2)
					cell.shapes(pad).insert(circle)
#					pad_L = layout.layer(pad_label_layer_num1, pad_label_layer_num2)
#					cell.shapes(pad_L).insert(circle)


	def generate_goal_object(
				self, 
				loc_x, 
				loc_y, 
				unit,
				layout,
				cell):
					real_start_xy, real_end_xy = self.cal_real_position_xy(loc_x, loc_y, unit)

					longside_len = int( (real_end_xy[0] - real_start_xy[0]) * 0.4)
					shortside_len = int( (real_end_xy[0] - real_start_xy[0]) * 0.2)

					start_xy = (real_start_xy[0] + longside_len, real_start_xy[1] - shortside_len)
					end_xy = (real_end_xy[0] - longside_len, real_end_xy[1] + shortside_len)

					m5 = layout.layer(metal5_layer_num1, metal5_layer_num2)
					cell.shapes(m5).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
#					m5_L = layout.layer(metal5_label_layer_num1, metal5_label_layer_num2)
#					cell.shapes(m5_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))

					pad = layout.layer(pad_layer_num1, pad_layer_num2)
					cell.shapes(pad).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
#					pad_L = layout.layer(pad_label_layer_num1, pad_label_layer_num2)
#					cell.shapes(pad_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))


					start_xy = (real_start_xy[0] + shortside_len, real_start_xy[1] - longside_len)
					end_xy = (real_end_xy[0] - shortside_len, real_end_xy[1] + longside_len)

					m5 = layout.layer(metal5_layer_num1, metal5_layer_num2)
					cell.shapes(m5).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
#					m5_L = layout.layer(metal5_label_layer_num1, metal5_label_layer_num2)
#					cell.shapes(m5_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))

					pad = layout.layer(pad_layer_num1, pad_layer_num2)
					cell.shapes(pad).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))
#					pad_L = layout.layer(pad_label_layer_num1, pad_label_layer_num2)
#					cell.shapes(pad_L).insert(pya.Box(start_xy[0], start_xy[1], end_xy[0], end_xy[1]))


if __name__ == '__main__':

	w = 20 # maze width size of block
	h = 10 # maze hight size of block

	u = recommend_unit_nm # 1 block(road) size(nm)

	METAL5_LABEL_TEXT = None
	METAL5_PAD_LABEL_TEXT = None
#	METAL5_LABEL_TEXT = "VDD"
#	METAL5_PAD_LABEL_TEXT = "VDD"

	file_dir = None


	layout = pya.Layout()
	cell = layout.create_cell(cell_name_maze)

	maze = MazeCreater(size_w=w, size_h=h)

	field = maze.generate_maze()

	ary = maze.GDS_generater.generate(
		field, unit=u,
		start_position=start_goal_position['left_below'], goal_position=start_goal_position['right_above'],
		layout=layout, cell=cell)


	dt_now = datetime.datetime.now()
	file_name = ("maze_" + 
		str(dt_now.year) + 
		str(dt_now.month) + 
		str(dt_now.day) + 
		str(dt_now.hour) + 
		str(dt_now.minute) + 
		str(dt_now.second) + 
		".gds")
	if file_dir == None:
		layout.write(file_name)
	else:
		layout.write(file_dir + file_name)

	# debug out(ASCII art of maze)
	for i in range(h+1):
		print_str = ""
		for j in range(w+1):
			print_str = print_str + str(ary[i*(w+1) + j])
		print(print_str)

