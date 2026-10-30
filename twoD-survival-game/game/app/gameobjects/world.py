import pygame

from game.assets.data.thing_defs import ThingIDs, THING_DEFS,  TILE_SIZE
from game.package import Gameobject
from game.app.utils import noise, hash2d
from game.app.gameobjects.player import Player
from game.app.gameobjects.tile import Tile

    
class World(Gameobject):

    CHUNK_SIZE: int = 4
    
    TILE_SCALED_SIZE = TILE_SIZE * Tile.SCALE

    def __init__(self, engine, scene, args):
        super().__init__(engine, scene, args)
        
        self.cached_player_position: tuple[float,float] = (0,0)

        self.load_range = 3

        self.seed=12345678

        self.existing_chunks = {}

        self.scene.add_gameobject(
            gameobject_class= Player, 
            position= (0,0),
            layer= 1
        )
        
        player =self.scene.get_gameobject("Player1")
        self.player_transform = player.get_component("Transform")

        cp = self._get_current_player_chunk_position()

        surrounding_chunk_positions = [(cp[0], cp[1])]
        
        for r in range(1, self.load_range + 1):
            for x in range(1 - r, r + 1):
                surrounding_chunk_positions.append((cp[0] + x, cp[1] - r))
            for y in range(1 - r, r + 1):
                surrounding_chunk_positions.append((cp[0] + r, cp[1] + y))
            for x in range(r - 1, -r - 1, -1):
                surrounding_chunk_positions.append((cp[0] + x, cp[1] + r))
            for y in range(r - 1, -r - 1, -1):
                surrounding_chunk_positions.append((cp[0] - r, cp[1] + y))
                
        for required_chunk_pos in surrounding_chunk_positions:
            if not required_chunk_pos in self.existing_chunks:
                self._generate_chunk(1, required_chunk_pos)

    def update(self):
        player_pos: tuple = self.player_transform.position.xy

        if self.cached_player_position != player_pos:
            
            cp = self._get_current_player_chunk_position()

            surrounding_chunk_positions = [(cp[0], cp[1])]

            for r in range(1, self.load_range + 1):
                for x in range(1 - r, r + 1):
                    surrounding_chunk_positions.append((cp[0] + x, cp[1] - r))
                for y in range(1 - r, r + 1):
                    surrounding_chunk_positions.append((cp[0] + r, cp[1] + y))
                for x in range(r - 1, -r - 1, -1):
                    surrounding_chunk_positions.append((cp[0] + x, cp[1] + r))
                for y in range(r - 1, -r - 1, -1):
                    surrounding_chunk_positions.append((cp[0] - r, cp[1] + y))

            for chunk_pos in set(surrounding_chunk_positions) - set(self.existing_chunks):
                self._generate_chunk(1, chunk_pos)
                break
                    
            for chunk_pos in set(self.existing_chunks) - set(surrounding_chunk_positions):
                self._destroy_chunk(chunk_pos)
                break
                
            self.cached_player_position = player_pos

        return super().update()

    def _get_current_player_chunk_position(self) -> tuple[int,int]:
        player_pos: tuple = self.player_transform.position.xy
        
        return(
            int(player_pos[0] // (self.CHUNK_SIZE * self.TILE_SCALED_SIZE)),
            int(player_pos[1] // (self.CHUNK_SIZE * self.TILE_SCALED_SIZE)),
        )

    def _generate_chunk(self,  floor, target_chunk_pos):

        generated_entities :list[Gameobject] = []

        for y in range(self.CHUNK_SIZE):
            for x in range(self.CHUNK_SIZE):

                pos = (
                    (target_chunk_pos[0] * (self.CHUNK_SIZE * self.TILE_SCALED_SIZE)) + x * self.TILE_SCALED_SIZE, 
                    (target_chunk_pos[1] * (self.CHUNK_SIZE * self.TILE_SCALED_SIZE)) + y * self.TILE_SCALED_SIZE
                )


                sea_scale = 0.0001
                temperature_scale = 0.00005
                humidity_scale = 0.0001
                forest_scale = 0.0005

                sea_value = noise(sea_scale * pos[0], sea_scale * pos[1], self.seed-1)
                temperature_value = noise(temperature_scale * pos[0], temperature_scale * pos[1], self.seed-3)
                humidity_value = noise(humidity_scale * pos[0], humidity_scale * pos[1], self.seed-2)
                forest_value = noise(pos[0] * forest_scale, pos[1] * forest_scale, self.seed-4)

                object_value = hash2d(pos[0], pos[1], self.seed)


                A = None
                B = None

                if sea_value < -0.2:
                   A = ThingIDs.WATER_TILE
                else:
                    if temperature_value < -0.4:
                        A = ThingIDs.TUNDRA_TILE

                    elif temperature_value < 0.3:
                        if humidity_value < -0.1:
                            A = ThingIDs.STEPPE_TILE
                        else:
                            A = ThingIDs.GRASS_TILE

                            if forest_value < -0.1:
                                if object_value < -0.9:
                                    B = ThingIDs.TREE
                            if object_value < -0.99:
                                B = ThingIDs.TREE
                    else:
                        if humidity_value < 0.2:
                            A = ThingIDs.SAND_TILE
                        else:
                            # トロピカル
                            print("トロピカルバイオーム")
                            A = ThingIDs.GRASS_TILE

                if A is not None:
                    generated_entities.append(self._generate_entity(A, pos, 0))
                if B is not None:
                    print("propせいせい")
                    generated_entities.append(self._generate_entity(B, pos, 1))

        self.existing_chunks[target_chunk_pos] = generated_entities

    def _generate_entity(self, thing_id, pos, layer) -> Gameobject:
        entity_def = THING_DEFS.get(thing_id).entity_def
        gameobject_class = entity_def.gameobject_class
        return self.scene.add_gameobject(
            gameobject_class= gameobject_class, 
            thing_id= thing_id, 
            position= pos, 
            layer= layer,
            entity_def= entity_def,
            surface= self.scene.get_surface(thing_id)
        )


    def _destroy_chunk(self, target_chunk_pos):
        for tile_gameobject in self.existing_chunks[target_chunk_pos]:
            tile_gameobject.destroy()
        self.existing_chunks.pop(target_chunk_pos)


