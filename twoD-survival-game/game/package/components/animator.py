import pygame

from game.package.core.component import Component


class AnimationData:

    def __init__(
            self,
            name: str,
            frames: list[pygame.Surface],
            fps: float,
            is_loop: bool
        ):
        self.name: str = name
        self.frames: list[pygame.Surface] = frames
        self.fps: float = fps
        self.is_loop: bool = is_loop

        self._scaled_cache: dict[tuple[float, float], list[pygame.Surface]] = {}

    def get_frames(self) -> list[pygame.Surface]:
        return self.frames

    def get_scaled_frames(self, scale: tuple[float, float]) -> list[pygame.Surface]:
        if scale not in self._scaled_cache:
            self._scaled_cache[scale] = self._build_scaled_frames(scale)
        return self._scaled_cache[scale]

    def _build_scaled_frames(self, scale: tuple[float, float]) -> list[pygame.Surface]:
        sx, sy = scale
        return [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * sx), int(frame.get_height() * sy))
            )
            for frame in self.frames
        ]


class AnimationPlayer:

    def __init__(self):
        self.animation_data: AnimationData | None = None
        self.is_playing: bool = False
        self.frame_index: int = 0
        self.elapsed: float = 0.0


    def update(self, dt: float) -> None:
        if self.is_playing:

            if self.animation_data is None:
                return

            frame_duration = 1.0 / self.animation_data.fps
            self.elapsed += dt

            if self.elapsed >= frame_duration:
                self.elapsed -= frame_duration
                next_index = self.frame_index + 1

                if next_index >= len(self.animation_data.frames):
                    if self.animation_data.is_loop:
                        self.frame_index = 0
                    else:
                        self.frame_index = len(self.animation_data.frames) - 1
                        self.is_playing = False
                else:
                    self.frame_index = next_index

    def get_current_frame(self):
        return self.animation_data.get_frames()[self.frame_index]

    def play(self) -> None:
        self.is_playing = True

    def stop(self) -> None:
        self.is_playing = False

    def reset(self) -> None:
        self.frame_index = 0
        self.elapsed = 0.0


class Animator(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)
        
        self.animations: list[AnimationData] = []
        self.animation_player: AnimationPlayer = AnimationPlayer()

        self.transform = self.parent.get_component("Transform")
        self.sprite_renderer = self.parent.get_component("SpriteRenderer")
    
        if len(self.animations) >= 1:
            self.animation_player.animation_data = self.animations[0]

    def update(self):
        self.animation_player.update(self.engine.delta_time)

        frames: list[pygame.Surface] = self.animation_player.animation_data.get_scaled_frames(tuple(self.transform.scale.xy))
        frame_index: int = self.animation_player.frame_index

        self.sprite_renderer.render_data.surface = frames[frame_index]

        return super().update()

    def add_animation(
        self,
        name: str,
        frames: list[pygame.Surface],
        fps: float,
        is_loop: bool
    ) -> None:
        self.animations.append(AnimationData(name, frames, fps, is_loop))

    def remove_animation(self, name: str) -> None:
        self.animations = [a for a in self.animations if a.name != name]


    def change_animation(self, name: str, autoplay: bool = False, force_restart: bool = False) -> None:

        animation = self.animation_player.animation_data
        if animation is not None:
            if animation.is_loop == True and animation.name == name:
                return
            
        animation = self._find_animation(name)
        if animation is None:
            return
        
        self.animation_player.animation_data = animation

        if autoplay:
            self.animation_player.play()
        else:
            self.animation_player.stop()

        if force_restart:
            self.animation_player.reset()

    def _find_animation(self, name: str) -> AnimationData | None:
        for animation in self.animations:
            if animation.name == name:
                return animation
        print(
            f"{self.parent_gameobject}, {self.__class__.__name__}: "
            f"アニメーション '{name}' が見つかりませんでした。"
        )
        return None
    
