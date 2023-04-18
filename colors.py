class Color():
    R: int
    G: int
    B: int
    def __init__(self, R, G, B) -> None:
        self.R = R
        self.G = G
        self.B = B
    def bash_str(self):
        # return f"\x1b[48;2;{self.R};{self.G};{self.B}m \x1b[0m"
        return f"\x1b[48;2;{self.R};{self.G};{self.B}m "
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Color):
            return False
        return self.R == __value.R and self.G == __value.G and self.B == __value.B

invalid_color = Color(-1, -1, -1)
