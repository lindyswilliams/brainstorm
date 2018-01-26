def check_it(y, factors, k=1):
	if((y > 1) & (k < y)):
		if(y%(k+1) == 0):
			factors.extend([k+1])
			y = y/(k+1)
			check_it(y, factors, 1)
		else:
			check_it(y, factors, k+1)
	return factors