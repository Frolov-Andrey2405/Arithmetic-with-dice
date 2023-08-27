import random
import time


class DiceMathGame:
    def __init__(self):
        self.DICE_WIDTH = 9
        self.DICE_HEIGHT = 5
        self.CANVAS_WIDTH = 79
        self.CANVAS_HEIGHT = 24 - 3

        self.QUIZ_DURATION = 30
        self.MIN_DICE = 2
        self.MAX_DICE = 6

        self.REWARD = 4
        self.PENALTY = 1

        self.ALL_DICE = [
            (['+-------+', '|       |', '|   O   |', '|       |', '+-------+'], 1),
            (['+-------+', '| O     |', '|       |', '|     O |', '+-------+'], 2),
            (['+-------+', '|     O |', '|       |', '| O     |', '+-------+'], 2),
            (['+-------+', '| O     |', '|   O   |', '|     O |', '+-------+'], 3),
            (['+-------+', '|     O |', '|   O   |', '| O     |', '+-------+'], 3),
            (['+-------+', '| O   O |', '|       |', '| O   O |', '+-------+'], 4),
            (['+-------+', '| O   O |', '|   O   |', '| O   O |', '+-------+'], 5),
            (['+-------+', '| O   O |', '| O   O |', '| O   O |', '+-------+'], 6),
            (['+-------+', '| O O O |', '|       |', '| O O O |', '+-------+'], 6),
        ]

    def main(self):
        print(f'''
Arithmetic with dice game

Add up the sides of all the dice displayed on the screen. You have
{self.QUIZ_DURATION} seconds to answer as many as possible. You get
{self.REWARD} points for each correct answer and lose {self.PENALTY} point
for each incorrect answer.
        ''')
        input('Press Enter to begin...')

        correct_answers = 0
        incorrect_answers = 0
        start_time = time.time()

        while time.time() < start_time + self.QUIZ_DURATION:
            sum_answer, dice_faces = self.prepare_dice()
            top_left_dice_corners = self.calculate_dice_positions(dice_faces)

            canvas = self.draw_dice_on_canvas(
                dice_faces, top_left_dice_corners)

            self.display_canvas(canvas)
            response = input('Enter the sum: ').strip()

            if response.isdecimal() and int(response) == sum_answer:
                correct_answers += 1
            else:
                print(f'Incorrect, the answer is {sum_answer}')
                time.sleep(2)
                incorrect_answers += 1

        self.display_final_score(correct_answers, incorrect_answers)

    def prepare_dice(self):
        sum_answer = 0
        dice_faces = []
        num_dice = random.randint(self.MIN_DICE, self.MAX_DICE)

        for _ in range(num_dice):
            die = random.choice(self.ALL_DICE)
            dice_faces.append(die[0])
            sum_answer += die[1]

        return sum_answer, dice_faces

    def calculate_dice_positions(self, dice_faces):
        top_left_dice_corners = []

        for die in dice_faces:
            while True:
                left = random.randint(
                    0, self.CANVAS_WIDTH - 1 - self.DICE_WIDTH)
                top = random.randint(
                    0, self.CANVAS_HEIGHT - 1 - self.DICE_HEIGHT)

                if not self.does_overlap(top_left_dice_corners, left, top):
                    top_left_dice_corners.append((left, top))
                    break

        return top_left_dice_corners

    def does_overlap(self, top_left_dice_corners, left, top):
        for prev_die_left, prev_die_top in top_left_dice_corners:
            prev_die_right = prev_die_left + self.DICE_WIDTH
            prev_die_bottom = prev_die_top + self.DICE_HEIGHT

            for corner_x, corner_y in (
                (left, top), (left + self.DICE_WIDTH, top),
                (left, top + self.DICE_HEIGHT),
                (left + self.DICE_WIDTH, top + self.DICE_HEIGHT)
            ):
                if prev_die_left <= corner_x < prev_die_right and prev_die_top <= corner_y < prev_die_bottom:
                    return True

        return False

    def draw_dice_on_canvas(self, dice_faces, top_left_dice_corners):
        canvas = {}

        for i, (die_left, die_top) in enumerate(top_left_dice_corners):
            die_face = dice_faces[i]
            for dx in range(self.DICE_WIDTH):
                for dy in range(self.DICE_HEIGHT):
                    canvas_x = die_left + dx
                    canvas_y = die_top + dy
                    canvas[(canvas_x, canvas_y)] = die_face[dy][dx]

        return canvas

    def display_canvas(self, canvas):
        for cy in range(self.CANVAS_HEIGHT):
            for cx in range(self.CANVAS_WIDTH):
                print(canvas.get((cx, cy), ' '), end='')
            print()

    def display_final_score(self, correct_answers, incorrect_answers):
        score = (correct_answers * self.REWARD) - \
            (incorrect_answers * self.PENALTY)
        print(f'Correct:   {correct_answers}')
        print(f'Incorrect: {incorrect_answers}')
        print(f'Score:     {score}')


if __name__ == '__main__':
    game = DiceMathGame()
    game.main()
