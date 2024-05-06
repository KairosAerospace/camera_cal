from camera import Camera, Cmos
import math


if __name__ == "__main__":
    SonyILx = Cmos(3.8 / 1000, 9504, 6336, name="SonyILx")
    IMX540 = Cmos(2.74 / 1000, 5320, 4600, name="IMX540")
    # cam = Camera(SonyILx, 35)
    cam = Camera(IMX540, 16)
    fov_h = cam.get_fov_h()
    fov_v = cam.get_fov_v()
    print(math.degrees(fov_h), math.degrees(fov_v))