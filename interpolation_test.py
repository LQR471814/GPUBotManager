import math
from typing import List

# * Note: To interpolate with a longer duration, simply add more steps and have the same amount of delay between executing steps

def interpolate_deltas(start: float, end: float, steps: int) -> List[float]: #? Interpolation with sin
    deltas = [] #? Interpolated deltas
    t = -math.pi / 2 #? Time (time ranges between -pi/2 and pi/2)
    step_size = math.pi / steps #? It's pi / steps because the full range of the function is exactly pi long
    prev_value = 1

    for i in range(steps):
        value = (math.sin(t) + 1) * (end - start)/2 + start
        deltas.append(value - prev_value)
        prev_value = value
        t += step_size

    return deltas

def interpolate(start: float, end: float, steps: int) -> List[float]: #? Interpolation with sin
    interpolation = [] #? Interpolated values
    t = -math.pi / 2 #? Time (time ranges between -pi/2 and pi/2)
    step_size = math.pi / steps #? It's pi / steps because the full range of the function is exactly pi long

    for i in range(steps):
        x = (math.sin(t) + 1) * (end - start)/2 + start
        interpolation.append(x)
        t += step_size

    return interpolation

print(interpolate(1, 10, 10))
print(interpolate_deltas(1, 10, 10))
