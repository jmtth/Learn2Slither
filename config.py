from dataclasses import dataclass, field
import const as c


@dataclass
class GameConfig:
    nb_cells: int = 10
    initial_size: int = 3
    nb_apples: int = 3


@dataclass
class RenderConfig:
    screen_width: int = 600
    screen_height: int = 750
    game_height: int = 600
    show_grid: bool = True
    show_vision: bool = False
    fps: int = c.FPS
    ms: int = c.MS_OPTIONS[0]
    step_by_step: bool = False


@dataclass
class AiConfig:
    sessions: int = 10
    save_name: str = "q_table"
    visual: bool = False
    load_name: str | None = None
    learn: bool = True
    step_by_step: bool = False


@dataclass
class AppConfig:
    game: GameConfig = field(default_factory=GameConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    ai: AiConfig = field(default_factory=AiConfig)

    @property
    def cell_size(self):
        return self.render.screen_width // self.game.nb_cells

    @property
    def snake_pos(self):
        return self.game.nb_cells // 2, self.game.nb_cells // 2
