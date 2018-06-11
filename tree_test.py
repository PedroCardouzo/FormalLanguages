class TreeNode:
	"""value of the node and an arbitrary number of children"""
	def __init__(self, value, *children):
		self.children = [x for x in children if x is not None]
		self.value = value


# extract_all :: TreeNode -> [String]
# if is a leaf, returns a list containing only the node value of the leaf.
# else appends itself in front of every element in the list returned by calling this function recursively on its children
def extract_all(node):
	if node.children == []:
		return [node.value]
	else:
		acc = []
		for child in node.children:
			acc += [node.value+x for x in extract_all(child)]

		return acc

def main():
	# just some example code to show a group buddy how to get every possible path through a TreeNode
	t = TreeNode(
			'A',
			TreeNode(
				'B',
				TreeNode(
					'1'
				),
				TreeNode(
					'2'
				)
			),
			TreeNode(
				'C',
				TreeNode(
					'+'
				),
				TreeNode(
					'-'
				),
				TreeNode(
					'*',
					TreeNode('#')
				)
			)
		)
	print(extract_all(t))  # expected output is ['AB1', 'AB2', 'AC+', 'AC-', 'AC*#']


if __name__ == '__main__':
	main()