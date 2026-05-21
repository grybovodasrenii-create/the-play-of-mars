import pygame 
import sys   
import random 
import math   


WIDTH, HEIGHT = 1024, 768 
FPS = 60                  
TILE_SIZE = 50            
MAP_COLS, MAP_ROWS = 100, 100 
MAP_WIDTH = MAP_COLS * TILE_SIZE   
MAP_HEIGHT = MAP_ROWS * TILE_SIZE 

# Цвета в формате RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
DARK_GREEN = (30, 150, 30)
BLUE = (50, 100, 200)
YELLOW = (200, 200, 50)
ORANGE = (200, 100, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)


DESERT = (210, 180, 140)   
CRATER = (160, 130, 100)   
ICE = (200, 240, 255)      
MOUNTAIN = (100, 100, 100)  


TRANSLATIONS = {
    "en": { # Английский
        "title": "MARS COLONIZATION",
        "start": "Press ENTER to Start",
        "settings": "Press S for Settings",
        "exit": "Press ESC to Exit",
        "lang_toggle": "Press L to change Language (EN)",
        "settings_title": "SETTINGS / HELP",
        "controls": [
            "WASD - Move Rover", "E - Gather Ore", "B - Toggle Build (1: Drill, 2: Solar)",
            "LMB - Place | RMB - Delete", "R - Repair (Metal)", "U - Upgrade (Metal+Elec)",
            "ESC - Pause", "", "Bring Ore to Base for storage.",
            "Drills cost ORE and produce METAL.", "Solar Panels cost METAL and produce ELEC."
        ],
        "base_ore": "Base Ore",
        "metal": "Metal",
        "electric": "Electric",
        "rover_hp": "Rover HP",
        "inv": "Inv",
        "inv_full": "INVENTORY FULL!",
        "colonization": "Colonization",
        "rad_hazard": "RADIATION HAZARD!",
        "build": "Build",
        "upgrade": "Upgrade",
        "drill": "Drill",
        "solar": "Solar",
        "rover": "Rover",
        "costs": "1:Drill 100 Ore, 2:Solar 30 Metal",
        "upgrade_msg": "Keys 1,2,3 | LMB on target",
        "upgrade_costs": {"Rover": "50 Metal, 50 Elec", "Drill": "40 Metal", "Solar": "40 Metal"},
        "win": "MARS TERRAFORMED!",
        "lose": "MISSION FAILED"
    },
    "ru": { 
        "title": "КОЛОНИЗАЦИЯ МАРСА",
        "start": "ENTER - Начать игру",
        "settings": "S - Настройки",
        "exit": "ESC - Выход",
        "lang_toggle": "L - Сменить язык (RU)",
        "settings_title": "НАСТРОЙКИ / ПОМОЩЬ",
        "controls": [
            "WASD - Движение", "E - Сбор руды", "B - Режим постройки (1: Бур, 2: Панель)",
            "ЛКМ - Поставить | ПКМ - Удалить", "R - Ремонт (Металл)", "U - Улучшение (Металл+Эл)",
            "ESC - Пауза", "", "Отвозите руду на базу для хранения.",
            "Буры стоят РУДУ и добывают МЕТАЛЛ.", "Солн. панели стоят МЕТАЛЛ и дают ЭЛЕКТРИКУ."
        ],
        "base_ore": "Руда базы",
        "metal": "Металл",
        "electric": "Электрика",
        "rover_hp": "HP Ровера",
        "inv": "Инв",
        "inv_full": "ИНВЕНТАРЬ ПОЛОН!",
        "colonization": "Колонизация",
        "rad_hazard": "РАДИАЦИОННАЯ ОПАСНОСТЬ!",
        "build": "Стройка",
        "upgrade": "Улучшение",
        "drill": "Бур",
        "solar": "Панель",
        "rover": "Ровер",
        "costs": "1:Бур 100 Руды, 2:Панель 30 Металла",
        "upgrade_msg": "Клавиши 1,2,3 | ЛКМ по цели",
        "upgrade_costs": {"Rover": "50 Металл, 50 Эл", "Drill": "40 Металл", "Solar": "40 Металл"},
        "win": "МАРС ТЕРАФОРМИРОВАН!",
        "lose": "МИССИЯ ПРОВАЛЕНА"
    }
}


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (100, 60, 30), (15, 30, 10, 30)) 
        pygame.draw.circle(self.image, GREEN, (20, 25), 20)         
        pygame.draw.circle(self.image, DARK_GREEN, (15, 20), 10)      
        self.rect = self.image.get_rect(center=(x, y))

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height) 
        self.width = width
        self.height = height

    def apply(self, entity): 
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply_pos(self, pos): 
        return (pos[0] + self.camera.x, pos[1] + self.camera.y)

    def reverse_pos(self, pos): 
        return (pos[0] - self.camera.x, pos[1] - self.camera.y)

    def update(self, target): 
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        x = min(0, x) 
        y = min(0, y) 
        x = max(-(MAP_WIDTH - WIDTH), x)
        y = max(-(MAP_HEIGHT - HEIGHT), y) 
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, life, vel_x=None, vel_y=None):
        super().__init__()
        size = random.randint(3, 6) 
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(
            vel_x if vel_x is not None else random.uniform(-40, 40),
            vel_y if vel_y is not None else random.uniform(-40, 40)
        )
        self.life = life 
        self.max_life = life

    def update(self, dt):
        self.pos += self.vel * dt 
        self.rect.center = self.pos
        self.life -= dt 
        if self.life <= 0:
            self.kill() 
        else:
            alpha = int((self.life / self.max_life) * 255)
            self.image.set_alpha(alpha)


class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Рисование многогранника руды разными цветами
        pygame.draw.polygon(self.image, (220, 120, 50), [(20, 5), (30, 20), (20, 35), (10, 20)])
        pygame.draw.polygon(self.image, ORANGE, [(10, 15), (20, 25), (10, 35), (0, 25)])
        pygame.draw.polygon(self.image, YELLOW, [(30, 10), (40, 20), (30, 30), (20, 20)])
        self.rect = self.image.get_rect(center=(x, y))
        self.amount = random.randint(50, 150) # Количество руды в кучке


class Meteor(pygame.sprite.Sprite):
    def __init__(self, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 50), (20, 20), 15)
        pygame.draw.circle(self.image, RED, (20, 20), 18, 2)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 6)
        self.rect = self.image.get_rect()
        # Появляется сверху со случайным смещением
        self.start_pos = pygame.math.Vector2(target_x + random.randint(-400, 400), target_y - 800)
        self.target_pos = pygame.math.Vector2(target_x, target_y) # Летит в сторону игрока
        self.pos = pygame.math.Vector2(self.start_pos)
        self.rect.center = self.pos
        self.speed = 500
        direction = self.target_pos - self.start_pos
        if direction.length() > 0: self.dir = direction.normalize() # Вектор направления
        else: self.dir = pygame.math.Vector2(0, 1)

    def update(self, dt):
        self.pos += self.dir * self.speed * dt
        self.rect.center = self.pos
        # Создание "хвоста" из частиц
        if random.random() < 0.6: game.spawn_particles(self.rect.centerx, self.rect.centery, ORANGE, 2)
        if self.pos.y >= self.target_pos.y: self.explode() # Взрыв при достижении цели

    def explode(self):
        game.spawn_particles(self.rect.centerx, self.rect.centery, RED, 40) # Много искр
       
        for b in game.buildings:
            if math.hypot(b.rect.centerx - self.rect.centerx, b.rect.centery - self.rect.centery) < 120: b.hp -= 40
       
        if math.hypot(game.player.pos.x - self.rect.centerx, game.player.pos.y - self.rect.centery) < 120: game.player.hp -= 30
        self.kill()


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, max_hp):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        if color:
            self.image.fill(color)
            pygame.draw.rect(self.image, DARK_GRAY, self.image.get_rect(), 3)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_hp = max_hp
        self.hp = max_hp
        self.level = 1 

    def draw_hp(self, surface, camera):
        pos = camera.apply_rect(self.rect)
        if self.hp < self.max_hp:
            pygame.draw.rect(surface, RED, (pos.x, pos.y - 10, pos.width, 5))
            pygame.draw.rect(surface, GREEN, (pos.x, pos.y - 10, pos.width * (self.hp / self.max_hp), 5))
        if self != game.base:
            lvl_txt = game.font.render(f"L{self.level}", True, WHITE)
            surface.blit(lvl_txt, (pos.x, pos.y + pos.height + 2))


class Base(Building):
    def __init__(self, x, y):
        super().__init__(x, y, (160, 160), None, 1000)
        self.rect.center = (x, y)
        pygame.draw.polygon(self.image, GRAY, [(40, 20), (120, 20), (150, 60), (150, 100), (120, 140), (40, 140), (10, 100), (10, 60)])
        pygame.draw.polygon(self.image, DARK_GRAY, [(40, 20), (120, 20), (150, 60), (150, 100), (120, 140), (40, 140), (10, 100), (10, 60)], 4)
        pygame.draw.circle(self.image, BLUE, (80, 80), 35) # Купол
        pygame.draw.circle(self.image, (100, 150, 255), (80, 80), 35, 3)
        pygame.draw.circle(self.image, WHITE, (70, 70), 10) # Блик на куполе
        for lx, ly in [(10, 20), (130, 20), (10, 120), (130, 120)]:
            pygame.draw.rect(self.image, DARK_GRAY, (lx, ly, 20, 20), border_radius=3)
        pygame.draw.circle(self.image, RED, (80, 20), 5) # Маячок
    def update(self, dt): pass


class Drill(Building):
    def __init__(self, x, y):
        super().__init__(x, y, (TILE_SIZE, TILE_SIZE), None, 150)
        self.redraw(); self.mine_timer = 0; self.mine_rate = 1.0
    def redraw(self): # Визуальное обновление при повышении уровня
        self.image.fill((0,0,0,0))
        color = YELLOW if self.level == 1 else (255, 215, 0) if self.level == 2 else (255, 255, 200)
        pygame.draw.rect(self.image, (100, 100, 110), (5, 20, 40, 30), border_radius=4)
        pygame.draw.polygon(self.image, color, [(15, 20), (35, 20), (25, 5)])
        pygame.draw.rect(self.image, DARK_GRAY, (22, 20, 6, 25))
        pygame.draw.circle(self.image, (200, 100, 50), (25, 25), 8)
        pygame.draw.rect(self.image, GRAY, (0, 0, 50, 50), 2, border_radius=4)
    def update(self, dt):
        if self.hp <= 0: (game.spawn_particles(self.rect.centerx, self.rect.centery, GRAY, 30), self.kill()); return
        if game.electricity >= 1: # Если есть свет
            self.mine_timer += dt
            if self.mine_timer >= self.mine_rate / self.level: # Чем выше уровень, тем быстрее добыча
                game.metal += 2 * self.level; game.electricity -= 1; self.mine_timer = 0
                game.spawn_particles(self.rect.centerx, self.rect.top, WHITE, 3) # Искры работы


class SolarPanel(Building):
    def __init__(self, x, y):
        super().__init__(x, y, (TILE_SIZE, TILE_SIZE), None, 100)
        self.redraw(); self.energy_timer = 0; self.energy_rate = 1.0
    def redraw(self):
        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, GRAY, (22, 30, 6, 15))
        p_color = (30, 50, 150) if self.level == 1 else (50, 80, 200) if self.level == 2 else (100, 130, 255)
        panel_rect = pygame.Rect(2, 5, 46, 25)
        pygame.draw.rect(self.image, p_color, panel_rect, border_radius=2)
        pygame.draw.rect(self.image, WHITE, panel_rect, 1, border_radius=2)
        for i in range(1, 4): pygame.draw.line(self.image, (100, 150, 255), (2 + i * 11, 5), (2 + i * 11, 30))
        pygame.draw.line(self.image, (100, 150, 255), (2, 17), (48, 17))
    def update(self, dt):
        if self.hp <= 0: (game.spawn_particles(self.rect.centerx, self.rect.centery, GRAY, 30), self.kill()); return
        self.energy_timer += dt
        if self.energy_timer >= self.energy_rate: game.electricity += 3 * self.level; self.energy_timer = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Отрисовка внешнего вида марсохода
        self.image_orig = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image_orig, WHITE, (5, 5, 40, 30), border_radius=6)
        pygame.draw.rect(self.image_orig, GRAY, (5, 5, 40, 30), 2, border_radius=6)
        pygame.draw.rect(self.image_orig, (50, 200, 255), (25, 10, 15, 20), border_radius=4) 
        for wx in [0, 19, 38]: # Колеса
            pygame.draw.rect(self.image_orig, (40, 40, 40), (wx, 2, 12, 6), border_radius=2)
            pygame.draw.rect(self.image_orig, (40, 40, 40), (wx, 32, 12, 6), border_radius=2)
        self.image = self.image_orig.copy(); self.rect = self.image.get_rect(center=(x, y))
        # Физика движения через векторы
        self.pos = pygame.math.Vector2(x, y); self.vel = pygame.math.Vector2(0, 0); self.acc = pygame.math.Vector2(0, 0); self.angle = 0
        self.max_speed, self.acc_val, self.friction = 300, 1500, -5.0
        # Характеристики игрока
        self.max_capacity, self.rad_protection, self.max_hp, self.hp, self.inventory_ore = 50, 0, 200, 200, 0
        self.level = 1

    def update(self, dt):
        self.acc = pygame.math.Vector2(0, 0); keys = pygame.key.get_pressed()
        # Управление WASD
        if keys[pygame.K_w]: self.acc.y = -self.acc_val
        if keys[pygame.K_s]: self.acc.y = self.acc_val
        if keys[pygame.K_a]: self.acc.x = -self.acc_val
        if keys[pygame.K_d]: self.acc.x = self.acc_val
       
        self.acc += self.vel * self.friction; self.vel += self.acc * dt
        if self.vel.length() > self.max_speed: self.vel.scale_to_length(self.max_speed)
       
        if self.vel.length() > 5:
            t_angle = math.degrees(math.atan2(-self.vel.y, self.vel.x))
            self.angle += ((t_angle - self.angle + 180) % 360 - 180) * 10 * dt
            self.image = pygame.transform.rotate(self.image_orig, self.angle); self.rect = self.image.get_rect(center=self.pos)
        if self.vel.length() < 10 and self.acc.length() == 0: self.vel = pygame.math.Vector2(0, 0)
      
        old_p = self.pos.copy(); self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2; self.rect.center = self.pos
        
        if self.rect.left < 0 or self.rect.right > MAP_WIDTH: self.pos.x = old_p.x; self.vel.x = 0
        if self.rect.top < 0 or self.rect.bottom > MAP_HEIGHT: self.pos.y = old_p.y; self.vel.y = 0
        if game.world.get_tile(int(self.pos.x//TILE_SIZE), int(self.pos.y//TILE_SIZE)) == MOUNTAIN: self.pos = old_p; self.vel *= -0.5
        if self.vel.length() > 50 and random.random() < 0.2: game.spawn_particles(self.rect.centerx, self.rect.bottom, CRATER, 1)
        if self.hp <= 0: (game.spawn_particles(self.rect.centerx, self.rect.centery, RED, 50), self.kill(), setattr(game, 'state', 'lose'))

    def draw_hp(self, surface, camera): 
        pos = camera.apply_rect(self.rect)
        if self.hp < self.max_hp:
            pygame.draw.rect(surface, RED, (pos.x, pos.y - 10, pos.width, 5))
            pygame.draw.rect(surface, GREEN, (pos.x, pos.y - 10, pos.width * (self.hp / self.max_hp), 5))
        lvl_t = game.font.render(f"L{self.level}", True, BLUE)
        surface.blit(lvl_t, (pos.x, pos.y + pos.height + 2))


class WorldGenerator:
    def __init__(self): 
        
        self.grid = [[DESERT for _ in range(MAP_ROWS)] for _ in range(MAP_COLS)]; self.generate()
    def generate(self):
      
        def add_b(biome, count, max_r):
            for _ in range(count):
                cx, cy, r = random.randint(0, MAP_COLS-1), random.randint(0, MAP_ROWS-1), random.randint(5, max_r)
                for x in range(cx-r, cx+r):
                    for y in range(cy-r, cy+r):
                        if 0 <= x < MAP_COLS and 0 <= y < MAP_ROWS and math.hypot(x-cx, y-cy) < r: self.grid[x][y] = biome
        add_b(CRATER, 20, 15); add_b(ICE, 15, 12); add_b(MOUNTAIN, 30, 8) # Генерация объектов
       
        bcx, bcy = MAP_COLS // 2, MAP_ROWS // 2
        for x in range(bcx-8, bcx+8):
            for y in range(bcy-8, bcy+8):
                if 0 <= x < MAP_COLS and 0 <= y < MAP_ROWS: self.grid[x][y] = DESERT
    def get_tile(self, x, y):
        return self.grid[x][y] if 0 <= x < MAP_COLS and 0 <= y < MAP_ROWS else DESERT


class UIManager:
    def __init__(self, font, big_font): self.font, self.big_font = font, big_font
    def draw_menu(self, screen):
        t_data = TRANSLATIONS[game.lang]
        screen.fill(BLACK); t = self.big_font.render(t_data["title"], True, ORANGE); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//4))
        menu_items = [t_data["start"], t_data["settings"], t_data["lang_toggle"], t_data["exit"]]
        for i, txt in enumerate(menu_items):
            t = self.font.render(txt, True, WHITE); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 + i*50))
    def draw_settings(self, screen): 
        t_data = TRANSLATIONS[game.lang]
        screen.fill(BLACK); t = self.big_font.render(t_data["settings_title"], True, WHITE); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//8))
        for i, line in enumerate(t_data["controls"]): t = self.font.render(line, True, GRAY); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//4 + i*30))
    def draw_hud(self, screen, game): 
        t_data = TRANSLATIONS[game.lang]
       
        pygame.draw.rect(screen, DARK_GRAY, (10, 10, 220, 100), border_radius=5)
        screen.blit(self.font.render(f"{t_data['base_ore']}: {int(game.ore)}", True, ORANGE), (20, 20))
        screen.blit(self.font.render(f"{t_data['metal']}: {int(game.metal)}", True, WHITE), (20, 45))
        screen.blit(self.font.render(f"{t_data['electric']}: {int(game.electricity)}", True, YELLOW), (20, 70))
       
        pygame.draw.rect(screen, DARK_GRAY, (WIDTH-240, 10, 230, 80), border_radius=5)
        hp_c = RED if game.player.hp < 50 else GREEN; screen.blit(self.font.render(f"{t_data['rover_hp']}: {int(game.player.hp)}", True, hp_c), (WIDTH-230, 20))
        inv_c = RED if game.player.inventory_ore >= game.player.max_capacity else WHITE
        screen.blit(self.font.render(f"{t_data['inv']}: {int(game.player.inventory_ore)}/{game.player.max_capacity}", True, inv_c), (WIDTH-230, 45))
        if game.player.inventory_ore >= game.player.max_capacity: screen.blit(self.font.render(t_data["inv_full"], True, RED), (WIDTH-230, 65))
       
        pygame.draw.rect(screen, DARK_GRAY, (WIDTH//2-200, 10, 400, 30), border_radius=5)
        pygame.draw.rect(screen, GREEN, (WIDTH//2-200, 10, 400*(game.colonization/100), 30), border_radius=5)
        col_t = self.font.render(f"{t_data['colonization']}: {game.colonization:.1f}%", True, WHITE); screen.blit(col_t, (WIDTH//2 - col_t.get_width()//2, 15))
       
        if game.rad_timer_active:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((255, 0, 0, 40)); screen.blit(overlay, (0,0))
            w_t = self.big_font.render(t_data["rad_hazard"], True, RED); screen.blit(w_t, (WIDTH//2 - w_t.get_width()//2, HEIGHT//2))
        
        if game.build_mode:
            b_name = t_data[game.build_selected.lower()]
            t = self.font.render(f"{t_data['build']}: {b_name} ({t_data['costs']})", True, WHITE)
            pygame.draw.rect(screen, BLUE, (WIDTH//2-250, HEIGHT-50, 500, 40), border_radius=5); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT-40))
        elif game.upgrade_mode:
            u_name = t_data[game.upgrade_selected.lower()]
            msg = f"{t_data['upgrade']}: {u_name} ({t_data['upgrade_costs'][game.upgrade_selected]}) - {t_data['upgrade_msg']}"
            t = self.font.render(msg, True, YELLOW)
            pygame.draw.rect(screen, (30, 80, 30), (WIDTH//2-350, HEIGHT-50, 700, 40), border_radius=5); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT-40))
    def draw_win(self, screen): 
        t_data = TRANSLATIONS[game.lang]
        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); surf.fill((50, 200, 50, 150)); screen.blit(surf, (0, 0))
        t = self.big_font.render(t_data["win"], True, WHITE); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//3))
    def draw_lose(self, screen): 
        t_data = TRANSLATIONS[game.lang]
        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); surf.fill((200, 50, 50, 150)); screen.blit(surf, (0, 0))
        t = self.big_font.render(t_data["lose"], True, WHITE); screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//3))


class Game:
    def __init__(self):
        pygame.init(); self.screen = pygame.display.set_mode((WIDTH, HEIGHT)); pygame.display.set_caption("Mars Colonization")
        self.clock = pygame.time.Clock(); self.font = pygame.font.SysFont("Consolas", 18, bold=True); self.big_font = pygame.font.SysFont("Consolas", 48, bold=True)
        self.ui = UIManager(self.font, self.big_font); self.state = "menu"; self.lang = "ru"; self.reset()
    def reset(self): 
        global game; game = self; self.world = WorldGenerator(); self.camera = Camera(WIDTH, HEIGHT)
        
        self.all_sprites, self.buildings, self.resources, self.particles, self.trees = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
        self.player = Player(MAP_WIDTH//2, MAP_HEIGHT//2); self.all_sprites.add(self.player)
        self.base = Base(MAP_WIDTH//2, MAP_HEIGHT//2 - 120); self.buildings.add(self.base); self.all_sprites.add(self.base)
        self.ore, self.metal, self.electricity, self.colonization = 200, 100, 0, 0.0
        self.build_mode, self.build_selected = False, "Drill"
        self.upgrade_mode, self.upgrade_selected = False, "Rover"
        self.meteor_timer, self.rad_timer, self.cutscene_timer, self.rad_timer_active = 0, 0, 0, False
        
        for _ in range(500):
            rx, ry = random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT)
            dist = math.hypot(rx - MAP_WIDTH//2, ry - MAP_HEIGHT//2)
            chance = 0.05 if dist < 600 else 0.4 if dist < 1200 else 0.9
            if random.random() < chance and self.world.get_tile(rx//TILE_SIZE, ry//TILE_SIZE) != MOUNTAIN:
                r = Resource(rx, ry); self.resources.add(r); self.all_sprites.add(r)
    def spawn_particles(self, x, y, color, count): # Удобный метод создания кучи частиц сразу
        for _ in range(count): p = Particle(x, y, color, random.uniform(0.5, 1.5)); self.particles.add(p); self.all_sprites.add(p)
    def run(self): 
        while True: dt = self.clock.tick(FPS) / 1000.0; self.events(); self.update(dt); self.draw()
    def events(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if self.state == "menu": # Логика в меню
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: self.state = "playing"
                    if event.key == pygame.K_s: self.state = "settings"
                    if event.key == pygame.K_l: self.lang = "ru" if self.lang == "en" else "en"
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            elif self.state == "settings" and event.type == pygame.KEYDOWN: # Логика в настройках
                if event.key == pygame.K_ESCAPE: self.state = "menu"
                if event.key == pygame.K_l: self.lang = "ru" if self.lang == "en" else "en"
            elif self.state == "playing": # Логика во время игры
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.state = "menu"
                    if event.key == pygame.K_b: self.build_mode = not self.build_mode; self.upgrade_mode = False
                    if event.key == pygame.K_u: self.upgrade_mode = not self.upgrade_mode; self.build_mode = False
                    if self.build_mode:
                        if event.key == pygame.K_1: self.build_selected = "Drill"
                        if event.key == pygame.K_2: self.build_selected = "Solar"
                    if self.upgrade_mode:
                        if event.key == pygame.K_1: self.upgrade_selected = "Rover"
                        if event.key == pygame.K_2: self.upgrade_selected = "Drill"
                        if event.key == pygame.K_3: self.upgrade_selected = "Solar"
                    if event.key == pygame.K_e: self.gather_resource()
                    if event.key == pygame.K_r: self.repair()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.build_mode:
                        if event.button == 1: self.place_building(pygame.mouse.get_pos())
                        if event.button == 3: self.delete_building(pygame.mouse.get_pos())
                    elif self.upgrade_mode and event.button == 1:
                        self.apply_upgrade(pygame.mouse.get_pos())
            elif self.state in ("win", "lose") and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.reset(); self.state = "menu"
    def gather_resource(self): # Логика сбора руды
        for r in self.resources:
            if math.hypot(self.player.pos.x - r.rect.centerx, self.player.pos.y - r.rect.centery) < 80:
                amount = min(25, r.amount, self.player.max_capacity - self.player.inventory_ore)
                if amount > 0:
                    self.player.inventory_ore += amount; r.amount -= amount; self.spawn_particles(r.rect.centerx, r.rect.centery, ORANGE, 8)
                    if r.amount <= 0: r.kill()
                break
    def repair(self): 
        if self.metal >= 15 and self.player.hp < self.player.max_hp: self.player.hp = min(self.player.max_hp, self.player.hp + 50); self.metal -= 15; self.spawn_particles(self.player.pos.x, self.player.pos.y, GREEN, 15)
        for b in self.buildings:
            if math.hypot(self.player.pos.x - b.rect.centerx, self.player.pos.y - b.rect.centery) < 100 and self.metal >= 10 and b.hp < b.max_hp:
                b.hp = min(b.max_hp, b.hp + 50); self.metal -= 10; self.spawn_particles(b.rect.centerx, b.rect.centery, GREEN, 10)
    def apply_upgrade(self, m_pos): 
        wp = self.camera.reverse_pos(m_pos)
        if self.upgrade_selected == "Rover":
            if self.player.rect.collidepoint(wp) and math.hypot(self.player.pos.x - self.base.rect.centerx, self.player.pos.y - self.base.rect.centery) < 150:
                if self.metal >= 50 and self.electricity >= 50:
                    self.metal -= 50; self.electricity -= 50; self.player.max_speed += 40; self.player.max_capacity += 30; self.player.rad_protection += 2; self.player.max_hp += 50; self.player.hp = self.player.max_hp; self.player.level += 1; self.spawn_particles(self.player.pos.x, self.player.pos.y, BLUE, 30)
        else:
            for b in self.buildings:
                if b.rect.collidepoint(wp) and math.hypot(self.player.pos.x - b.rect.centerx, self.player.pos.y - b.rect.centery) < 100:
                    if (self.upgrade_selected == "Drill" and isinstance(b, Drill)) or (self.upgrade_selected == "Solar" and isinstance(b, SolarPanel)):
                        cost = 40 * b.level
                        if self.metal >= cost and b.level < 3:
                            self.metal -= cost; b.level += 1; b.hp = b.max_hp; b.redraw(); self.spawn_particles(b.rect.centerx, b.rect.centery, BLUE, 20); break
    def place_building(self, m_pos): 
        wp = self.camera.reverse_pos(m_pos); gx, gy = int(wp[0]//TILE_SIZE)*TILE_SIZE, int(wp[1]//TILE_SIZE)*TILE_SIZE; tr = pygame.Rect(gx, gy, TILE_SIZE, TILE_SIZE)
        if any(b.rect.colliderect(tr) for b in self.buildings) or self.player.rect.colliderect(tr): return
        if not any(math.hypot(b.rect.centerx-(gx+25), b.rect.centery-(gy+25)) < 400 for b in self.buildings): return
        if self.build_selected == "Drill" and self.ore >= 100:
            b = Drill(gx, gy); self.buildings.add(b); self.all_sprites.add(b); self.ore -= 100; self.spawn_particles(gx+25, gy+25, YELLOW, 15)
        elif self.build_selected == "Solar" and self.metal >= 30:
            b = SolarPanel(gx, gy); self.buildings.add(b); self.all_sprites.add(b); self.metal -= 30; self.spawn_particles(gx+25, gy+25, WHITE, 15)
    def delete_building(self, m_pos): 
        wp = self.camera.reverse_pos(m_pos)
        for b in self.buildings:
            if b != self.base and b.rect.collidepoint(wp): 
                self.spawn_particles(b.rect.centerx, b.rect.centery, GRAY, 20); b.kill()
                if isinstance(b, Drill): self.ore += 50
                else: self.metal += 15
                break
    def update(self, dt): 
        if self.state not in ("playing", "win_cutscene"): return
        if self.state == "win_cutscene": 
            self.cutscene_timer += dt
            if self.cutscene_timer > 8.0: self.state = "win"
            if random.random() < 0.1:
                tx, ty = random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT)
                tree = Tree(tx, ty); self.trees.add(tree); self.all_sprites.add(tree)
            self.particles.update(dt); return
        self.all_sprites.update(dt); self.camera.update(self.player)
       
        if math.hypot(self.player.pos.x - self.base.rect.centerx, self.player.pos.y - self.base.rect.centery) < 120:
            if self.player.inventory_ore > 0: drop = min(self.player.inventory_ore, 100*dt); self.player.inventory_ore -= drop; self.ore += drop
       
        self.colonization += (len(self.buildings)-1)*0.05*dt
        if self.colonization >= 100.0: (setattr(self, 'colonization', 100.0), setattr(self, 'state', 'win_cutscene'))
      
        self.meteor_timer += dt
        if self.meteor_timer > random.uniform(20, 50): self.meteor_timer = 0; self.all_sprites.add(Meteor(self.player.pos.x, self.player.pos.y))
       
        self.rad_timer_active = math.hypot(self.player.pos.x - self.base.rect.centerx, self.player.pos.y - self.base.rect.centery) > 1200
        if self.rad_timer_active:
            self.rad_timer += dt
            if self.rad_timer > 1.0: self.player.hp -= max(0, 10-self.player.rad_protection); self.rad_timer = 0
    def draw(self): 
        if self.state == "menu": self.ui.draw_menu(self.screen)
        elif self.state == "settings": self.ui.draw_settings(self.screen)
        elif self.state in ("playing", "win_cutscene", "win", "lose"):
            self.screen.fill(BLACK)
            
            sc = max(0, -self.camera.camera.x//TILE_SIZE); ec = min(MAP_COLS, (-self.camera.camera.x+WIDTH)//TILE_SIZE+1)
            sr = max(0, -self.camera.camera.y//TILE_SIZE); er = min(MAP_ROWS, (-self.camera.camera.y+HEIGHT)//TILE_SIZE+1)
            for c in range(sc, ec):
                for r in range(sr, er):
                    tile = self.world.grid[c][r]
                    if self.state in ("win_cutscene", "win"): 
                        p = min(1.0, self.cutscene_timer/8.0) if self.state == "win_cutscene" else 1.0
                        color = [int(tile[i]*(1-p) + GREEN[i]*p) for i in range(3)]
                    else: color = tile
                    rx, ry = c*TILE_SIZE + self.camera.camera.x, r*TILE_SIZE + self.camera.camera.y
                    pygame.draw.rect(self.screen, color, (rx, ry, TILE_SIZE, TILE_SIZE))
                    if (c*13 + r*27)%10 < 2: pygame.draw.circle(self.screen, [max(0, color[i]-20) for i in range(3)], (rx+15, ry+15), 3) # Камушки
                    pygame.draw.rect(self.screen, (0,0,0,15), (rx, ry, TILE_SIZE, TILE_SIZE), 1) # Сетка
           
            for s in self.all_sprites:
                if self.state == "win_cutscene" and not isinstance(s, (Building, Player, Particle, Tree)): continue
                self.screen.blit(s.image, self.camera.apply(s))
                if isinstance(s, (Building, Player)): s.draw_hp(self.screen, self.camera)
            
            if self.build_mode and self.state == "playing":
                wp = self.camera.reverse_pos(pygame.mouse.get_pos()); sx, sy = self.camera.apply_pos((int(wp[0]//TILE_SIZE)*TILE_SIZE, int(wp[1]//TILE_SIZE)*TILE_SIZE))
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA); surf.fill((255, 255, 255, 100)); self.screen.blit(surf, (sx, sy))
           
            if self.state == "playing": self.ui.draw_hud(self.screen, self)
            elif self.state == "win": self.ui.draw_win(self.screen)
            elif self.state == "lose": self.ui.draw_lose(self.screen)
        pygame.display.flip() 
if __name__ == "__main__":
    game = Game()
    game.run() 
