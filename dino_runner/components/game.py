import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, GAME_OVER, HAMMER, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        self.running =  False
        self.score = 0
        self.lives = 3
        self.death_count = 0
        self.scores = []
        self.historical_scores = []

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
         
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw    
        if self.death_count == self.lives:
            self.lives = 3
            self.death_count = 0
            self.historical_scores.append(sum(self.scores))
            self.scores = []
        self.score = 0
        self.player = Dinosaur()
        self.game_speed = 30
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.scores.append(self.score)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.playing = False 
                self.running = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player, self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5 

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) 
        self.draw_background() 
        self.draw_score()
        self.draw_lives()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width() 
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) 
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    def draw_lives(self):
        self.print_text(22,f"Lives: {self.lives - self.death_count}", 1000, 70)

    def draw_score(self):
        self.print_text(22, f"Score: {self.score}", 1000, 50)
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.font_size = 18
                self.message = f"{self.player.type.capitalize()} enabled for {time_to_show} seconds."
                self.to_write_x = 500
                self.to_write_y = 40              
                self.print_text(self.font_size, self.message, self.to_write_x, self.to_write_y)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH //2
        if self.death_count == 0:
            self.print_text(30, "Press any key to start",  half_screen_width, half_screen_height)
            if len(self.historical_scores) > 0:
                self.print_text(30, f"Highest score: {max(self.historical_scores)}",  half_screen_width , half_screen_height - 250)
            self.screen.blit(SHIELD,(half_screen_width - 200, half_screen_height + 50))
            self.print_text(20, "Shield: you become invulnerable but ",  half_screen_width - 200, half_screen_height + 150)
            self.print_text(20, "your score will decrese by 50 ",  half_screen_width - 200, half_screen_height + 200)
            self.print_text(20, "for collition with any obstacle ",  half_screen_width - 200, half_screen_height + 250)
            self.screen.blit(HAMMER,(half_screen_width + 200, half_screen_height + 50))
            self.print_text(20, "Hammer: you can kill birds,",  half_screen_width + 200, half_screen_height + 150)
            self.print_text(20, "cactus can still kill you",  half_screen_width + 200, half_screen_height + 200)
        elif self.death_count < self.lives and self.death_count > 0:
            self.print_text(30, "Press any key to start",  half_screen_width, half_screen_height)
            self.print_text(30, f"Last score: {self.score}",  half_screen_width, half_screen_height + 100)
            self.print_text(30, f"Max score: {max(self.scores)}",  half_screen_width, half_screen_height + 150)                
            self.print_text(30, f"Number of deaths: {self.death_count}",  half_screen_width, half_screen_height + 200)
        else:
            self.screen.blit(GAME_OVER,(half_screen_width - 160 , half_screen_height ))
            self.print_text(30, "Press any key to play again",  half_screen_width, half_screen_height + 100)
            self.print_text(30, f"Max score: {max(self.scores)}",  half_screen_width, half_screen_height + 150)
            self.print_text(30, f"Total Achieved: {sum(self.scores)}",  half_screen_width, half_screen_height + 200)
            if len(self.historical_scores) > 0:
                self.print_text(30, f"Highest score: {max(self.historical_scores)}",  half_screen_width , half_screen_height - 250)

        self.screen.blit(ICON,(half_screen_width - 20, half_screen_height - 140))

        pygame.display.update() 
        self.handle_events_on_menu()
    
    def print_text(self, font_size, print_string, rect_x, rect_y, color_text = (0, 0, 0)):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(print_string , True, color_text)

        text_rect = text.get_rect()
        text_rect.center = (rect_x, rect_y)
        self.screen.blit(text, text_rect)
    

