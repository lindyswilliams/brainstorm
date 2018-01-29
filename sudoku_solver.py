import numpy as np

# given one matrix, will return row, column, and grid matricies in list of lists
def get_col_row_grid_matrix(original_matrix):
	grid_rows = list(original_matrix)
	grid_cols = zip(*grid_rows)
	grid_cols = [list(x) for x in grid_cols]

	idxs = range(0,len(original_matrix[0]))
	grid_index = len(original_matrix[0])
	grid_sub_index = grid_index/3

	idx1 = idxs[0:grid_sub_index]
	idx2 = idxs[grid_sub_index:grid_sub_index*2]
	idx3 = idxs[grid_sub_index*2:grid_sub_index*3]

	all_idxs = []
	all_idxs.extend([idx1])
	all_idxs.extend([idx2])
	all_idxs.extend([idx3])


	grid_grids = []
	for the_idx in all_idxs:
		for the_sec_idx in all_idxs:
			tmp_result = []
			for one_idx in range(0, 3):
				tmp_result_2 = []
				for two_idx in range(0, 3):
					tmp_result_2 = tmp_result_2 + [original_matrix[the_idx[one_idx]][the_sec_idx[two_idx]]]
				tmp_result = tmp_result + tmp_result_2
			grid_grids.extend([tmp_result])
	return grid_rows, grid_cols, grid_grids

# given one matrix, possible array of 1-9 in place- returns a list of lists of lists
def get_one_thru_nine_possible(one_matrix):
	possible_matrix =[]
	tmp_matrix = []
	for i in range(0,9): 
		for j in range(0,9):
			if one_matrix[i][j] != '0':
				tmp_matrix.extend([list(one_matrix[i][j])])
			else:
				tmp_matrix.extend([[str(x) for x in range(1,10)]])
	possible_matrix = list([tmp_matrix[0+x:9+x] for x in range(0,81,9)])
	return possible_matrix


# check for 1-9 on row, cols, and grid matrix - returns a list of lists of lists of possible elems
def check_one_thru_nine(the_matrix, matrix_row, matrix_col, matrix_grid, matrix_code):
	one_nine_matrix = []
	for i in range(0,9):
		for j in range(0,9):
			if len(new_possible2[i][j]) > 1:
				new_elem_list = list(set(the_matrix[i][j]) - (set(matrix_row[i]).union(set(matrix_col[j])).union(set(matrix_grid[int(matrix_code[i][j][0])]))))
				#print new_elem_list, set(the_matrix[i][j]), (set(matrix_row[i]).union(set(matrix_col[j])).union(set(matrix_grid[int(matrix_code[i][j][0])])))
				if len(new_elem_list) == 0:
					one_nine_matrix.extend([the_matrix[i][j]])
				else:
					one_nine_matrix.extend([new_elem_list])
			else:
				one_nine_matrix.extend([the_matrix[i][j]])
	one_nine_matrix = list([one_nine_matrix[0+x:9+x] for x in range(0,81,9)])
	return one_nine_matrix

# check for any must be elements in a matrix gievn the possible matrix
def check_matrix_for_must(one_matrix):
	one_matrix_result=[]
	for index, elem in enumerate(one_matrix):
		for index2, item in enumerate(elem):
			flat_list = []
			if len(item) > 1:
				for index3, num in enumerate(one_matrix[index]):
					if (index2 != index3):
						for number in num:
							flat_list.append(number)
			result = list(set(one_matrix[index][index2]) - set(flat_list))
			if (len(result) == 1):
				one_matrix_result.extend(result)
			else:
				one_matrix_result.extend('0')
	one_matrix_result = list([one_matrix_result[0+x:9+x] for x in range(0,81,9)])
	return one_matrix_result

# given the matrix without possibilities, column, row and grid matrix, add them all together
def sum_all_matricies(matrix_def, matrix_row):
	result = []
	for i in range(0,9):
		for j in range(0,9):
			#matrix_col = zip(*matrix_col)
			#matrix_col = [list(x) for x in matrix_col]
			elem = int(matrix_def[i][j]) + int(matrix_row[i][j]) #+ matrix_col[i][j] #+ matrix_row[i][j]# + matrix_grid[i][j]
			if int(matrix_def[i][j]) == int(matrix_row[i][j]):
				result.extend(matrix_row[i][j])
			else:
				result.extend(str(elem))
	result = list([result[0+x:9+x] for x in range(0,81,9)])
	return result

# array of arrays > 0 write 0 in place
def flatten_matrix(the_matrix):
	flat_matrix = []
	for i in range(0,9):
		flat_list = []
		for j in range(0,9):
			if len(the_matrix[i][j])>1:
				flat_list.extend('0')
			else: 
				flat_list.extend(the_matrix[i][j])
		flat_matrix.extend([flat_list])
	return flat_matrix

# runs through one iteration
def one_iteration(the_full_grid):
	row, col, grid = get_col_row_grid_matrix(the_full_grid)
	possible = get_one_thru_nine_possible(the_full_grid)
	possible_narrow = check_one_thru_nine(possible, row, col, grid, matrix_code)
	possible_row, possible_col, possible_grid = get_col_row_grid_matrix(possible_narrow)
	new_row = check_matrix_for_must(possible_row)
	new_matrix = flatten_matrix(possible_narrow)
	new_matrix_summed = sum_all_matricies(new_matrix, new_row)
	return new_matrix_summed


#sudoku.txt

file = open('/Users/lindywilliams/Documents/Data/Euler/sudoku.txt', 'r')
nums = file.readlines()

# creating the code grid
first = [['0'], ['0'], ['0'], ['1'], ['1'], ['1'], ['2'], ['2'], ['2']]
second = [['3'], ['3'], ['3'], ['4'], ['4'], ['4'], ['5'], ['5'], ['5']]
third = [['6'], ['6'], ['6'], ['7'], ['7'], ['7'], ['8'], ['8'], ['8']]

matrix_code = [first]*3 + [second]*3 + [third]*3

for grid in range(1, 5):
	the_list = []
	for row in range(1, 10):
		the_list.extend([str(grid) + str(row)])

grid = []
for idx in the_list:
	grid.extend([(nums[int(idx)].split('\n')[0])])

full_grid = []
for elem in grid:
	full_grid.extend([list(elem)])

first_iter = one_iteration(full_grid)
sec_iter = one_iteration(first_iter)
third_iter = one_iteration(sec_iter)
fourth_iter = one_iteration(third_iter)



# clean code

# in the future, want to encorporate checking the cols and grids, 
# but if they find the same number, don't want to add them

#row, col, grid = get_col_row_grid_matrix(full_grid)
#possible = get_one_thru_nine_possible(full_grid)
#possible_narrow = check_one_thru_nine(possible, row, col, grid, matrix_code)
#possible_row, possible_col, possible_grid = get_col_row_grid_matrix(possible_narrow)
#new_row = check_matrix_for_must(possible_row)
##new_col = check_matrix_for_must(possible_col)
##new_grid = check_matrix_for_must(possible_grid)
##matrix without possibilities
#new_matrix = flatten_matrix(possible_narrow)
#new_matrix_summed = sum_all_matricies(new_matrix, new_row)









