import yaml, stars

class Simulation:
    def __init__(self, settings_file='settings.yaml'):
        print('Loading settings from {}'.format(settings_file))
        with open(settings_file, 'r') as f:
            data = yaml.load(f)
            self.settings = data

        self.time = self.settings['sim']['time'].get('start', 0)

        self.generate_stars()

    def generate_stars(self):
        print('Generating stars')
        self.stars = stars.generate_stars(
            self.settings.get("space_size", (700, 500)),
            self.settings.get("avg_groups", 10),
            self.settings.get("groups_sigma", 3),
            self.settings.get("avg_group_size", 10),
            self.settings.get("group_size_sigma", 3),
            self.settings.get("position_sigma", 50)
            )

    def draw_stars(self, images, surface, offset=(0, 0)):
        for star in self.stars:
            if star.mass == 1:
                surface.blit(images['star0'],
                    (star.position[0] - offset[0], star.position[1] - offset[1]))
            if star.mass == 0:
                surface.blit(images['star0yellow'],
                    (star.position[0] - offset[0], star.position[1] - offset[1]))

    def tick(self):
        self.time += self.settings['sim']['time'].get('time_increment', 1)


if __name__=="__main__":
    sim = Simulation()
