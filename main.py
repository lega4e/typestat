#!/usr/bin/python3

import argparse
import datetime as dt
import re
import sys

from nvxsct import sct





# objects
date_re = re.compile(
	'(\d{4})\.(\d{2})\.(\d{2}), (\d{2}):(\d{2}):(\d{2}) — '
	'(\d+(\.\d+)?) сек., (\d+) зн/мин, (\d+) \w+ \((\d+(\.\d+)?)\%\)'
)

target = None





# functions
def parse(line):
	'Парсит строку записи и формирует структуру'
	match = re.search(date_re, line)
	g = match.groups()
	return sct(
		year   = int(g[0]),
		month  = int(g[1]),
		day    = int(g[2]),
		hour   = int(g[3]),
		minute = int(g[4]),
		second = int(g[5]),
		time   = float(g[6]),
		symc   = int(g[8]),
		errc   = int(g[9]),
		errp   = float(g[10])
	)



def read():
	'Считывает строку из указанного файла или stdin'
	if target is None:
		return input()
	line = target.readline()
	if len(line) == 0:
		raise EOFError('EOF')
	return line[:-1]



def write_stat():
	'''
	Считывает четыре значения: общее время набора
	текста, скорость (знаков в минуту), количество
	ошибок и процент ошибок. Такие странные поля
	обусловлены тем, что на том сайте, где я
	занимаюсь, выдаётся только эта информация :)
	'''
	try:
		while True:
			try:
				t, a, b, c = map(lambda x: float(x), input().split(' '))
				date = dt.datetime.now().strftime('%Y.%m.%d, %X')
				print(
					'%s — %.3g сек., %i зн/мин, %i ошибок (%.3g%%)' %
					(date, t, int(a), int(b), c),
					file = target or sys.stdout
				)
			except Exception as e:
				if isinstance(e, EOFError):
					raise e
				print(e, file=sys.stderr)
	except EOFError:
		pass
	return



def print_stat():
	'Печать всей статистики'
	try:
		while True:
			line = read()
			print(line)
	except EOFError:
		pass





# main
parser = argparse.ArgumentParser(description=
	'Здравствуй, пользователь! Это программа, которая'
	'предназначена для записи статистики по набору текста'
	'и последующего её отображения. Пользуйся, и да'
	'возрадуется твой разум!'
)

parser.add_argument('action', choices=['write', 'list'])
parser.add_argument('-f', dest='file', help='Файл статистики')

args = parser.parse_args()

if args.action == 'write':
	if args.file is not None:
		target = open(args.file, 'a')
	write_stat()
else:
	if args.file is not None:
		target = open(args.file, 'r')
	print_stat()





# END
