



class Boss(GameObject):
    def __init__(self,
        position: "Vector2D",
        speed: number_types,
        player_sprite: "pygame.Surface",
        width: number_types = 64,
        height: number_types = 64) -> "None":
        """Initialisation of Player object."""

        super().__init__(position)
        self.speed = speed
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(player_sprite, (self.width, self.height))
        self.movement = Vector2D(0,0)
        self.rotation = 0