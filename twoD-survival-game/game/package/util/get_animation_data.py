import json, pygame


def get_animation_data(aniamtions_data_json_path, animation_name) -> list[dict[str,list]]:

    with open(aniamtions_data_json_path, "r") as f:
        animations_data = json.load(f)

    anim_data = animations_data[animation_name]
        
    spritesheet_surface = pygame.image.load(anim_data["spritesheet_image_path"])

    frames_data = anim_data["frames"]
    cut_frames = []
    for i in range(len(frames_data)):
        x, y, w, h = frames_data[i]
        frame_rect = pygame.Rect(x * w, y * h, w, h)
        cut_surface = spritesheet_surface.subsurface(frame_rect).copy()
        cut_frames.append(cut_surface)

    return {
        "name": animation_name,
        "autoplay" : anim_data["autoplay"],
        "is_loop" : anim_data["is_loop"],
        "fps" : anim_data["fps"],
        "frames" : cut_frames
        }