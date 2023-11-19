from utils import read_input_file
from pathlib import Path
from dataclasses import dataclass
import re

"""
This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover their energy. Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km. On the 12th second, both reindeer are resting. They continue to rest until the 138th second, when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the winning reindeer traveled?
"""
race_time = 2503
# race_time = 1000

@dataclass
class Race:
    name: str
    speed: int
    duration: int
    rest: int

    def __post_init__(self):
        if not isinstance(self.speed, int):
            self.speed = int(self.speed)
        if not isinstance(self.duration, int):
            self.duration = int(self.duration)
        if not isinstance(self.rest, int):
            self.rest = int(self.rest)

    def __repr__(self) -> str:
        return f"{self.name}, {self.speed} km/s for {self.duration} resting {self.rest}"

    def calculate_distance(self, race_time):
        tot_time = self.duration + self.rest
        freq = race_time // tot_time
        remaining = race_time % tot_time

        if remaining >= self.duration:
            freq += 1
            total_dist = freq * self.speed * self.duration
        else:
            total_dist = freq * self.speed * self.duration
            total_dist += remaining * self.speed

        return total_dist


def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day14_input"
    return read_input_file(filepath=file_path)

def _split(s: str) -> tuple:
    regex = r" can fly | km/s for | seconds, but then must rest for | seconds."
    return re.split(regex, s)

def part1():
    data = test_data()
    # data = [
    #     "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
    #     "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."
    # ]
    res = [Race(name, speed, duration, rest) for name, speed, duration, rest, _ in map(_split, data)]
    res = [x.calculate_distance(race_time) for x in res]

    return max(res)


"""
--- Part Two ---

Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second, he awards one point to the reindeer currently in the lead. (If there are multiple reindeer tied for the lead, they each get one point.) He keeps the traditional 2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point. He stays in the lead until several seconds into Comet's second burst: after the 140th second, Comet pulls into the lead and gets his first point. Of course, since Dancer had been in the lead for the 139 seconds before that, he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated 689 points, while poor Comet, our old champion, only has 312. So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, how many points does the winning reindeer have?
"""

def part2():
    data = test_data()
    # data = [
    #     "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
    #     "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."
    # ]

    res = [Race(name, speed, duration, rest) for name, speed, duration, rest, _ in map(_split, data)]

    winner = [0] * len(res)

    for t in range(1, race_time + 1):
        interim_points = [(x.calculate_distance(t), i) for i, x in enumerate(res)]
        # print(interim_points)
        winning_point = max(interim_points)[0]
        # print(winning_point)

        interim_winner = [x for x in interim_points if x[0] == winning_point]

        for wins in interim_winner:
            winner[wins[1]] += 1
    print(winner)
    final_winner = max(winner)
    return final_winner



if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)