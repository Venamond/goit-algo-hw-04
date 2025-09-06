#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import math


def parse_args() -> int:
    parser = argparse.ArgumentParser(
        description="Visualization of the Koch snowflake fractal with adjustable recursion level."
    )
    parser.add_argument(
        "-l", "--level", type=int,default=3, help="Recursion level (non-negative integer, e.g., 0..10). Default: 3"
    )
    args = parser.parse_args()
    if args.level < 0 or args.level > 10:
        parser.error("Recursion level must be in the range 0..10.")
    return args.level


def koch_segment(p1: tuple[float, float], p2: tuple[float, float], level: int) -> list[tuple[float, float]]:
    """Recursively generates a Koch curve segment between points p1 and p2."""
    if level == 0:
        return [p1, p2]

    x1, y1 = p1
    x2, y2 = p2
    dx = (x2 - x1) / 3
    dy = (y2 - y1) / 3

    # Points dividing the segment into 3 parts
    A = (x1, y1)
    B = (x1 + dx, y1 + dy)
    D = (x1 + 2 * dx, y1 + 2 * dy)
    E = (x2, y2)

    # Point C (top vertex of the "triangle")
    angle = math.radians(60)
    Cx = B[0] + dx * math.cos(angle) - dy * math.sin(angle)
    Cy = B[1] + dx * math.sin(angle) + dy * math.cos(angle)
    C = (Cx, Cy)

    # Recursively process the four segments
    return (
        koch_segment(A, B, level - 1)[:-1]
        + koch_segment(B, C, level - 1)[:-1]
        + koch_segment(C, D, level - 1)[:-1]
        + koch_segment(D, E, level - 1)
    )


def koch_snowflake(level):
    """Generates coordinates for the Koch snowflake."""
    # Initial equilateral triangle
    size = 1.0
    p1 = (0, 0)
    p2 = (size, 0)
    p3 = (size / 2, math.sin(math.radians(60)) * size)

    # Generate three sides
    side1 = koch_segment(p1, p2, level)[:-1]
    side2 = koch_segment(p2, p3, level)[:-1]
    side3 = koch_segment(p3, p1, level)

    return side1 + side2 + side3


def main():
    level = parse_args()
    coords = koch_snowflake(level)
    xs, ys = zip(*coords)

    plt.figure(figsize=(8, 8))
    plt.axis("equal")
    plt.axis("off")
    plt.plot(xs, ys, color="blue")
    plt.title(f"Koch Snowflake (level {level})")
    plt.show()


if __name__ == "__main__":
    main()