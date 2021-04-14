from flask import request

data = [
	{ "position": 1, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 1 },
	{ "position": 2, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 2 },
	{ "position": 3, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 3 },
	{ "position": 4, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 4 },
	{ "position": 5, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 5 },
	{ "position": 6, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 6 },
	{ "position": 7, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 7 },
	{ "position": 8, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 8 },
	{ "position": 8, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 9 },
	{ "position": 10, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 10 },
	]

def get_data():
	headers = [
		{ "value": "id", "text": "ID" },
		{ "value": "position", "text": "Position"},
			{ "value": "name", "text": 'Name'},
			{ "value": "weight", "text": "Weight"},
		{ "value": "symbol", "text": 'Symbol'},
		{ "value": "address", "text": 'Address'}
	]

	resp = {
		"items": data,
		"headers": headers
	}

	return resp

def get_for_edit(id):
	return { "position": 10, "name": 'Hydrogen', "weight": 1.0079, "symbol": 'H', "id": 10 }