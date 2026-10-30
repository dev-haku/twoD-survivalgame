from __future__ import annotations
import pygame
import asyncio
import json
import time

from game import paths, definition


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.package.core.scene import Scene


class Engine:  

    def __init__(self):

        self.running: bool = False
        self.delta_time: float = 0
        self.global_values: dict = definition.global_values
        self.input_status: InputStatus = InputStatus()
        self.scheduler:  Scheduler = Scheduler()
        self.debug_settings = definition.debug
    
        pygame.init()

        with open(paths.GAME_CONFIG, "r") as f:
            game_config = json.load(f)

        self.window = pygame.display.set_mode(
            game_config["window_size"], 
            pygame.RESIZABLE
        )

        pygame.display.set_caption(game_config["name"])
        pygame.display.set_icon(pygame.image.load(paths.ROOT / game_config["icon_image_path"]))

        self.scenes: list = definition.scenes

        init_scene_index = definition.initial_scene_index
        self.current_scene: Scene = self.scenes[init_scene_index](engine= self)

        self.max_tps: int = game_config["max_tps"]
        self.max_fps: int = game_config["max_fps"]

    async def start(self):
        self.running = True
        await self._loop()

    def current_time(self):
        return time.time()

    def change_scene(self, index: int):
        self.current_scene = self.scenes[index](engine=self)

    def shutdown(self):
        self.running = False

    async def _loop(self):
        clock = pygame.time.Clock()
        accumulator = 0.0
        fixed_dt = 1.0 / self.max_tps

        tps_timer = 0
        tps_count = 0
        fps_timer = 0
        fps_count = 0
        tps = 0

        while self.running:
            dt = clock.tick(self.max_fps) / 1000
            await asyncio.sleep(0)  
            accumulator += min(dt, fixed_dt * 5)

            fps_timer += dt

            while accumulator >= fixed_dt:
                self.delta_time = fixed_dt
                self._update()

                accumulator -= fixed_dt
                
                tps_timer += fixed_dt
                tps_count += 1
            
            self._draw()
            fps_count += 1

            if tps_timer >= 1:     
                tps = tps_count
                tps_timer = 0
                tps_count = 0

            if fps_timer >= 1:
                print(f"{tps} ticks, {fps_count} fps")

                fps_timer = 0
                fps_count = 0

    def _update(self):
        self._process_events()
        self.scheduler.update(self.delta_time)

        scene = self.current_scene
        if scene.active:
            scene.update()

    def _process_events(self):

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.shutdown()

            elif event.type == pygame.KEYDOWN:
                self.input_status.keys[pygame.key.name(event.key)] = True

                if self.debug_settings["print_key_events"]:
                    print(pygame.key.name(event.key))

            elif event.type == pygame.KEYUP:
                self.input_status.keys[pygame.key.name(event.key)] = False

            elif event.type == pygame.MOUSEMOTION:
                self.input_status.mouse_position = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input_status.mouse_buttons = [False] * 5
                self.input_status.mouse_buttons[event.button - 1] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.input_status.mouse_buttons = [False] * 5
                                 
    def _draw(self):
        if self.current_scene.active:

            scaled_screen = pygame.transform.scale(
                self.current_scene.render(), 
                self.window.get_size()
            )

            self.window.blit(
                scaled_screen, 
                (0,0)
            )

        pygame.display.flip()


class InputStatus:
    def __init__(self):
        self.keys = {}
        self.mouse_position = (0,0)
        self.mouse_buttons = [False] * 5

class Scheduler:
    def __init__(self):
        self.events = []

    def schedule_event(self, delay, callback, *args, **kwargs):
        self.events.append({
            "time": delay,
            "callback": callback,
            "args" : args,
            "kwargs" : kwargs
        })

    def update(self, delta_time):
        for event in self.events[:]:
            event["time"] -= delta_time

            if event["time"] <= 0:
                event["callback"](
                    *event["args"],
                    **event["kwargs"]
                )
                self.events.remove(event)