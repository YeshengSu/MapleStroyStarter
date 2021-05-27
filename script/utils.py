# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox

VERSION = 1.0

EXECUTION = 'MapleStory.exe'

HEAD_ICON_PATH = 'res/MapleStory.ico'
REFRESH_ICON_PATH = 'res/Refresh.png'
BACKGROUND_ICON_PATH = 'res/BackGround.jpg'
SERVER_LIST_URL = 'http://47.241.186.78/server.txt'
MAPLE_STORY_URL = 'http://www.baidu.com'

SERVER_NORMAL = 1
SERVER_BUSY = 2
SERVER_STOP = 3


def parse_cfg_str_to_list(cfg_str, is_num=False, default=None):
	"""
	将配置的字符串解析成一个列表
	Args:
		cfg_str (str): 格式：'val1,val2,val3,...'
		is_num (bool): 是否转转化为数字
		default : 没有解析数据时的默认返回项

	Returns:
		cfg_list (list): 解析完成的列表：['val1','val2','val3',...]

	"""
	if not cfg_str and default:
		return default

	if is_num:
		cfg_list = [int(s) for s in cfg_str.split(',') if s]
	else:
		cfg_list = [s for s in cfg_str.split(',') if s]
	return cfg_list


def parse_cfg_str_to_list_of_list(cfg_str, is_num=False, default=None):
	"""
	将配置的字符串解析成一个列表的列表
	Args:
		cfg_str (str): 格式：'val11,val12,val13,...;val21,val22,val23,...;...'
		is_num (bool): 是否转化成数字
		default : 没有解析数据时的默认返回项

	Returns:
		cfg_list (list): 解析完成的列表：[['val11','val12','val13',...],['val21','val22','val23',...],...]

	"""
	if not cfg_str and default:
		return default

	cfg_list = [s for s in cfg_str.split(';') if s]
	cfg_list_of_list = []

	if is_num:
		for l_str in cfg_list:
			cfg_list_of_list.append([int(s) for s in l_str.split(',') if s])
	else:
		for l_str in cfg_list:
			cfg_list_of_list.append([s for s in l_str.split(',') if s])

	return cfg_list_of_list


def parse_cfg_str_to_dict_of_list(cfg_str, is_num=False, is_force_list=False, default=None):
	"""
	将配置的字符串解析成一个列表的字典
	Args:
		cfg_str (str): 格式：'val11,val12,val13,...;val21,val22,val23,...;...'
		is_num (bool): 是否转化成数字
		is_force_list (bool): 是否强制转化为列表，开启后纵使字典value的长度不足2也会转成列表
		default : 没有解析数据时的默认返回项

	Returns:
		cfg_dict_of_list (dict):
			解析完成的列表：
				如果列表项多于两个:{'val11':['val12','val13',...],'val21':['val22','val23',...],...}
				如果列表项只有两个:{'val11':'val12','val21':'val22','val23',...}

	"""
	if not cfg_str and default:
		return default

	cfg_list = [s for s in cfg_str.split(';') if s]
	cfg_dict_of_list = {}

	for l_str in cfg_list:
		if is_num:
			lst = [int(s) for s in l_str.split(',') if s]
		else:
			lst = [s for s in l_str.split(',') if s]
		lst_len = len(lst)
		if lst_len > 2 or is_force_list:
			cfg_dict_of_list[lst[0]] = lst[1:]
		elif lst_len == 2:
			cfg_dict_of_list[lst[0]] = lst[1]

	return cfg_dict_of_list

def popup_warning(widget, title, content, callback=None):
	choice = QMessageBox.warning(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_critical(widget, title, content, callback=None):
	choice = QMessageBox.critical(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_infomation(widget, title, content, callback=None):
	choice = QMessageBox.information(widget, title, content, QMessageBox.Yes)

	if choice == QMessageBox.Yes:
		if callback:
			callback()


def popup_confirm(widget, title, content, callback=None):
	choice = QMessageBox.question(widget, title, content, QMessageBox.Yes | QMessageBox.Cancel)

	if choice == QMessageBox.Yes:
		if callback:
			callback()
