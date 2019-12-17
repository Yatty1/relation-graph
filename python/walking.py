'''
	0. parse all the data into accessible data structure
	1. find all combination of all subjects
	2. proceed one by one
	3. take data and transform into data structure below
	4. calculate numerator and denominator by formula specified
	5. calculate dcalc with span specified, which is 60 in this assignment
	6. create data to store all points on all combination calculated
'''
'''
	data: {
		a: [10,0,20,40],
		b: [0,39,50,20],
	}
'''
'''
	DATA STRUCTURE FOR COMBINATION
	combinations: [
		[a,b],
		[a,c],
		[a,d]
	]
'''
'''
DATA STRUCTURE CREATED at No.4 TO BE USED TO PROCEED No.5
	rows: [
		{
			numerator: 1,
			denominator: 1,
			dcalc: 0.02,
		}
	]
'''
'''
DATA STRUCTURE TO BE CREATED No.6
	points: {
		'a,b': 10,
		'a,c': 15,
	}
'''

'''
output file format
{
	"nodes": [
		{
			"id": "data_A_1",
			"group": "A",
			"relations": {
				"data_A_2": 20,
				"data_A_3": 120,
				"data_A_4": 0,
				"data_A_5": 420,
			}
		},
		...
	]
	"links": [
		{
			"source": "data_A_1",
			"target: "data_A_2"
		},
		{
			"source": "data_A_1",
			"target: "data_A_3"
		},
		...
	]
}
'''

import itertools as itt
import sys
import json

def parseFiles(filepaths):
	data = {}
	subjects = []
	for filepath in filepaths:
		filepathArr = filepath.split("/")
		filename = filepathArr[len(filepathArr) - 1]
		subject = filename.split(".")[0]
		subjects.append(subject)
		file = open(filepath, "r")
		data[subject] = []
		for i, line in enumerate(file):
			if i == 0:
				continue
			step = line.split(",")[2].replace("\n", "")
			data[subject].append(step)
		file.close()
	return subjects, data


def findAllCombinations(iteratable, length):
	return list(itt.combinations(iteratable, length))


def calculateNumDen(firstSubject, secondSubject):
	ddata = []
	length = len(firstSubject) if len(firstSubject) < len(secondSubject) else len(secondSubject)

	for j in range(length):
		numerator = (int(firstSubject[j]) - int(secondSubject[j])) ** 2
		denominator = (int(firstSubject[j]) ** 2) + (int(secondSubject[j]) ** 2)
		ddata.append({ 'numerator': numerator, 'denominator': denominator })
	return ddata


def dcalc(rows, span, threshold):
	for i in range(len(rows)):
		sumNum = 0
		sumDen = 0
		if (i + 1) < span:
			continue
		offset = (i + 1) - span
		for j in range(len(rows)):
			sumNum += rows[j + offset]['numerator']
			sumDen += rows[j + offset]['denominator']
			if (j + 1) == (span): # calc until where it is at
				rows[j + offset]['dcalc'] = 0 if sumNum == 0 else sumNum / sumDen
				rows[j + offset]['dcalc'] = -1 if sumDen < threshold else rows[j + offset]['dcalc']
				sumNum = 0
				sumDen = 0
				break
	return rows


def calcPoint(resultRow, w, threshold):
	point = 0
	for i in range(len(resultRow)):
		for j in range(len(resultRow)):
			if not j + i < len(resultRow):
				break
			if 'dcalc' not in resultRow[i + j] or resultRow[i+j]['dcalc'] == -1 or resultRow[i + j]['dcalc'] > threshold:
				break
			if (j + 1) == w:
				point += 1
				break
	return point

# <params>
# data: { id: "", group: "", relations: { "{id}": 12, "{anotherID}": 23 }}
# source: string
# target: string
# point: number
def formOutputNode(data, source, target, point):
	if data != None:
		data["relations"][target] = point
		return data
	else:
		newData = {}
		newData["id"] = source
		newData["group"] = source.split("_")[1]
		newData["relations"] = {}
		newData["relations"][target] = point
		return newData


'''
	Parameters to be modified
'''
SPAN = 60
THRESHOLD = 0.05
VALID_SPAN = 40
BORDER = 5500


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print(f"ERROR: More than one file should be specified. number of files specified: {len(sys.argv)}")
		exit(-1)

	outputData = { "nodes": [], "links": [] }
	outputNodeDict = {}

	subjects, data = parseFiles(sys.argv[1:])
	combinations = findAllCombinations(subjects, 2)

	print(f"LEN: {len(combinations)}")
	for i, comb in enumerate(combinations, start = 0):
		ddata = calculateNumDen(data[comb[0]], data[comb[1]])
		result = dcalc(ddata, SPAN, BORDER)
		point = calcPoint(result, VALID_SPAN, THRESHOLD)

		print(f"INDEX: {i} COMB: {comb[0]},{comb[1]}, POINT: {point}")

		if point != 0:
			outputData["links"].append({ "source": comb[0], "target": comb[1]})

		outputNodeDict[comb[0]] = formOutputNode(outputNodeDict.get(comb[0]), comb[0], comb[1], point)

		# add last element to nodes
		if i + 1 == len(combinations):
			outputNodeDict[comb[1]] = {}
			outputNodeDict[comb[1]]["id"] = comb[1]
			outputNodeDict[comb[1]]["group"] = comb[1].split("_")[1]
			outputNodeDict[comb[1]]["relations"] = {}

	for key, value in outputNodeDict.items():
		outputData["nodes"].append(value)

	with open(f"a-{SPAN}-{BORDER}-{VALID_SPAN}.json", "w+") as file:
		json.dump(outputData, file)
