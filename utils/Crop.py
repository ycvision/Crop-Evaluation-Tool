class Crop:
    def __init__(self, image_paths):
        self.likes = []
        self.imagePaths = image_paths
        self.length = len(self.imagePaths)

    def __getitem__(self, idx):
        if idx < 0 or idx >= self.length:
            raise IndexError
        return self.imagePaths[idx]

    def __str__(self):
        return "Number of likes: {}".format(sum(self.likes))