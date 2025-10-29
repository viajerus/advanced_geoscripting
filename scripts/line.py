import math


class Line:
    def __init__(self, coordinates, name=None):
        """
        Initialize the Line with a list of 3D points [(x, y, z), ...]
        """
        if len(coordinates) < 2:
            raise ValueError("Line must contain at least two points.")
        self.coordinates = coordinates
        self.name = name

    def get_segment_slopes(self) -> list:
        """
        Returns a list of slopes for each segment of the line.
        If a segment is vertical in x/y (i.e. dx and dy are 0), returns float('inf').
        """
        slopes = []
        for i in range(len(self.coordinates) - 1):
            x1, y1, z1 = self.coordinates[i]
            x2, y2, z2 = self.coordinates[i + 1]

            dx = x2 - x1
            dy = y2 - y1
            horizontal_distance = math.hypot(dx, dy)

            if horizontal_distance == 0:
                slopes.append(float("inf"))  # vertical in x/y, undefined slope
            else:
                dz = z2 - z1
                slopes.append(dz / horizontal_distance)
        return slopes

    def length(self) -> float:
        """
        Returns the length of the line.
        """
        total = 0.0
        for i in range(len(self.coordinates) - 1):
            x1, y1, z1 = self.coordinates[i]
            x2, y2, z2 = self.coordinates[i + 1]
            segment = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
            total += segment
        return total

    def coordinates(self) -> list:
        """
        Returns the coordinates of the line.
        """
        return self.coordinates.copy()

    def move(self, dx, dy, dz):
        """
        Moves the line by dx, dy and dz.
        :param dx: value by which to move the line in x direction
        :param dy: value by which to move the line in y direction
        :param dz: value by which to move the line in z direction
        """
        self.coordinates = [(x + dx, y + dy, z + dz) for (x, y, z) in self.coordinates]
