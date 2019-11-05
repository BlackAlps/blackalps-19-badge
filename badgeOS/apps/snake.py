import random

class App():
    """
    Simple snake game to show the badge capabilities
    """

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Snake"

    def run(self):
        self.badge.screen.oled.fill(0)
        self.badge.screen.oled.rect(0,0,128,64,1)

        sh, sw = 64, 128

        snk_x = sw/4
        snk_y = sh/2
        snake = [
            [snk_y, snk_x],
            [snk_y, snk_x-1],
            [snk_y, snk_x-2]
        ]

        food = [sh/2, sw/2]
        self.badge.screen.oled.pixel(int(food[1]), int(food[0]), 1)

        key = 'RIGHT'

        while True:
            next_key = self.badge.buttons.get_button()
            key = key if next_key is None else next_key

            if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
                return len(snake)

            new_head = [snake[0][0], snake[0][1]]

            if key == 'DOWN':
                new_head[0] += 1
            if key == 'UP':
                new_head[0] -= 1
            if key == 'LEFT':
                new_head[1] -= 1
            if key == 'RIGHT':
                new_head[1] += 1

            snake.insert(0, new_head)

            if snake[0] == food:
                food = None
                while food is None:
                    nf = [
                        random.randint(4, sh-4),
                        random.randint(4, sw-4)
                    ]
                    food = nf if nf not in snake else None
                self.badge.screen.oled.pixel(food[1], food[0], 1)
            else:
                tail = snake.pop()
                self.badge.screen.oled.pixel(int(tail[1]), int(tail[0]), 0)

            self.badge.screen.oled.pixel(int(snake[0][1]), int(snake[0][0]), 1)

            self.badge.screen.oled.show()

