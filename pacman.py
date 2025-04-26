import pygame
import random
import time

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman 2.0")

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
BLUE = (0, 0, 255)  # Labirent duvarları için
GHOST_COLORS = [
    (255, 0, 0),    # Kırmızı hayalet
    (255, 182, 255),  # Pembe hayalet
    (0, 255, 255),   # Turkuaz hayalet
    (255, 182, 85)   # Turuncu hayalet
]

# Labirent oluşturma
CELL_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Labirent haritası (0: yol, 1: duvar)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Pacman özellikleri
PACMAN_SIZE = 30
pacman_x = CELL_SIZE + CELL_SIZE//2
pacman_y = CELL_SIZE + CELL_SIZE//2
pacman_speed = 5

# Hayalet özellikleri
GHOST_SIZE = 30
ghosts = []
for i in range(4):
    ghost = {
        'x': SCREEN_WIDTH - 2 * CELL_SIZE,
        'y': SCREEN_HEIGHT - 2 * CELL_SIZE,
        'speed_x': 3,
        'speed_y': 3,
        'color': GHOST_COLORS[i],
        'direction': random.choice(['left', 'right', 'up', 'down'])
    }
    ghosts.append(ghost)

# Yem noktaları
dots = []
DOT_SIZE = 6
for y in range(len(maze)):
    for x in range(len(maze[0])):
        if maze[y][x] == 0:
            dots.append({
                'x': x * CELL_SIZE + CELL_SIZE//2,
                'y': y * CELL_SIZE + CELL_SIZE//2,
                'visible': True
            })

# Çilek özellikleri
STRAWBERRY_SIZE = 20
strawberry = {
    'x': -100,
    'y': -100,
    'visible': False,
    'last_spawn': time.time()
}

# Oyun değişkenleri
power_mode = False
power_mode_timer = 0
score = 0

def is_wall_collision(x, y, size):
    # Karakterin dört köşesini kontrol et
    points = [
        (x, y),
        (x + size, y),
        (x, y + size),
        (x + size, y + size)
    ]
    
    for point_x, point_y in points:
        grid_x = point_x // CELL_SIZE
        grid_y = point_y // CELL_SIZE
        if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
            return True
        if maze[grid_y][grid_x] == 1:
            return True
    return False

# Ana oyun döngüsü
running = True
clock = pygame.time.Clock()

while running:
    current_time = time.time()
    
    # Event kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pacman hareketi
    new_x = pacman_x
    new_y = pacman_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        new_x += pacman_speed
    if keys[pygame.K_UP]:
        new_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        new_y += pacman_speed

    # Duvar çarpışma kontrolü
    if not is_wall_collision(new_x, new_y, PACMAN_SIZE):
        pacman_x = new_x
        pacman_y = new_y

    # Çilek spawn kontrolü
    if not strawberry['visible'] and current_time - strawberry['last_spawn'] >= 10:
        valid_positions = []
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 0:
                    valid_positions.append((x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2))
        if valid_positions:
            pos = random.choice(valid_positions)
            strawberry['x'] = pos[0]
            strawberry['y'] = pos[1]
            strawberry['visible'] = True
            strawberry['last_spawn'] = current_time

    # Hayalet hareketi
    for ghost in ghosts:
        # Hayaletin yeni pozisyonunu hesapla
        new_x = ghost['x']
        new_y = ghost['y']
        
        if ghost['direction'] == 'left':
            new_x -= ghost['speed_x']
        elif ghost['direction'] == 'right':
            new_x += ghost['speed_x']
        elif ghost['direction'] == 'up':
            new_y -= ghost['speed_y']
        elif ghost['direction'] == 'down':
            new_y += ghost['speed_y']

        # Eğer duvarla karşılaşırsa yön değiştir
        if is_wall_collision(new_x, new_y, GHOST_SIZE):
            ghost['direction'] = random.choice(['left', 'right', 'up', 'down'])
        else:
            ghost['x'] = new_x
            ghost['y'] = new_y

        # Rastgele yön değiştirme
        if random.random() < 0.02:  # %2 ihtimalle
            ghost['direction'] = random.choice(['left', 'right', 'up', 'down'])

    # Çarpışma kontrolleri
    pacman_rect = pygame.Rect(pacman_x, pacman_y, PACMAN_SIZE, PACMAN_SIZE)

    # Çilek çarpışması
    if strawberry['visible']:
        strawberry_rect = pygame.Rect(strawberry['x'] - STRAWBERRY_SIZE//2,
                                    strawberry['y'] - STRAWBERRY_SIZE//2,
                                    STRAWBERRY_SIZE, STRAWBERRY_SIZE)
        if pacman_rect.colliderect(strawberry_rect):
            power_mode = True
            power_mode_timer = current_time
            strawberry['visible'] = False
            score += 50

    # Güç modu kontrolü
    if power_mode and current_time - power_mode_timer >= 10:
        power_mode = False

    # Hayalet çarpışması
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost['x'] - GHOST_SIZE//2,
                               ghost['y'] - GHOST_SIZE//2,
                               GHOST_SIZE, GHOST_SIZE)
        if pacman_rect.colliderect(ghost_rect):
            if power_mode:
                # Hayaleti başlangıç pozisyonuna gönder
                ghost['x'] = SCREEN_WIDTH - 2 * CELL_SIZE
                ghost['y'] = SCREEN_HEIGHT - 2 * CELL_SIZE
                score += 200
            else:
                running = False

    # Yem toplama
    for dot in dots:
        if dot['visible']:
            dot_rect = pygame.Rect(dot['x'] - DOT_SIZE//2,
                                 dot['y'] - DOT_SIZE//2,
                                 DOT_SIZE, DOT_SIZE)
            if pacman_rect.colliderect(dot_rect):
                dot['visible'] = False
                score += 10

    # Ekranı temizle
    screen.fill(BLACK)

    # Labirenti çiz
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE,
                               (x * CELL_SIZE, y * CELL_SIZE,
                                CELL_SIZE, CELL_SIZE))

    # Yemleri çiz
    for dot in dots:
        if dot['visible']:
            pygame.draw.circle(screen, WHITE,
                             (dot['x'], dot['y']), DOT_SIZE // 2)

    # Çileği çiz
    if strawberry['visible']:
        pygame.draw.circle(screen, (255, 0, 0),
                         (int(strawberry['x']), int(strawberry['y'])),
                         STRAWBERRY_SIZE//2)

    # Pacman'i çiz
    pygame.draw.circle(screen, NEON_GREEN,
                      (int(pacman_x + PACMAN_SIZE//2), int(pacman_y + PACMAN_SIZE//2)),
                      PACMAN_SIZE//2)

    # Hayaletleri çiz
    for ghost in ghosts:
        pygame.draw.circle(screen, ghost['color'],
                         (int(ghost['x']), int(ghost['y'])),
                         GHOST_SIZE//2)

    # Skoru göster
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Skor: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Ekranı güncelle
    pygame.display.flip()
    clock.tick(60)

pygame.quit()