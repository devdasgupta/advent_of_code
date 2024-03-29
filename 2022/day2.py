from utils import read_input_file
from pathlib import Path


file_path = Path(__file__).parent.absolute()
INPUT_DATA_FILE = f'{file_path}/day2_input'

OPPONENT_MAP = {
	'A': 'Rock',
	'B': 'Paper',
	'C': 'Scissor'
}

PLAY_MAP = {
	'X': 'Rock',
	'Y': 'Paper',
	'Z': 'Scissor'
}

SCORE_MAP = {
	'Rock': 1,
	"Paper": 2,
	"Scissor": 3,
	"Win": 6,
	"Draw": 3,
	"Loss": 0
}

OUT_MAP = {
	'X': 'Loss',
	'Y': 'Draw',
	'Z': 'Win'
}


def puzzle1(input_items):
	"""
	Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

	The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

	The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

	Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

	For example, suppose you were given the following strategy guide:

	A Y
	B X
	C Z
	This strategy guide predicts and recommends the following:

	In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
	In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
	The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
	In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

	What would your total score be if everything goes exactly according to your strategy guide?
	"""
	def calc_score(moves: tuple):
		oppo, player = moves

		oppo = OPPONENT_MAP[oppo]
		player = PLAY_MAP[player]
		score = SCORE_MAP[player]

		# When both opted choices are same, i.e. both Rock or both Paper etc.
		if oppo == player:
			score += SCORE_MAP["Draw"]
		# When you win
		elif (oppo == "Rock" and player == "Paper") or (oppo == "Paper" and player == "Scissor") or (oppo == "Scissor" and player == "Rock"):
			score += SCORE_MAP["Win"]
		# When you loose
		else:
			score += SCORE_MAP["Loss"]

		return score

	return sum(map(calc_score, input_items))


def puzzle2(input_items):
	"""
	The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

	The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

	In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
	In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
	In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
	Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

	Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
	"""
	def calc_score(moves: tuple):
		oppo, result = moves
		oppo = OPPONENT_MAP[oppo]
		result = OUT_MAP[result]
		score = SCORE_MAP[result]

		if result == "Draw":
			score += SCORE_MAP[oppo]
		elif result == "Win":
			if oppo == "Rock":
				score += SCORE_MAP["Paper"]
			elif oppo == "Paper":
				score += SCORE_MAP["Scissor"]
			else:
				score += SCORE_MAP["Rock"]
		else:
			if oppo == "Rock":
				score += SCORE_MAP["Scissor"]
			elif oppo == "Paper":
				score += SCORE_MAP["Rock"]
			else:
				score += SCORE_MAP["Paper"]

		return score

	return sum(map(calc_score, input_items))



if __name__ == "__main__":
    input_items = read_input_file(filepath=INPUT_DATA_FILE)
    input_items = [tuple(x.split()) for x in input_items]

    print(puzzle1(input_items))
    print(puzzle2(input_items))
