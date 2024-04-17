import math


def cal_f(sensor_dia, fov):
    return sensor_dia / 2.0 / math.tan(fov / 2.0)


def cal_fov_ang(x, f):
    return 2.0 * math.atan(x / 2.0 / f)


def cal_rsl_w(swath, sensor_reslution):
    s = 2 * swath / sensor_reslution
    return s


def cal_fov_width(fov, h):
    return 2 * h * math.tan(fov / 2.0)


class Cmos:
    def __init__(self, ps, H, V, name=''):
        self.ps = ps
        self.H = H
        self.V = V
        self.name = name
        self.h, self.v, self.diag = self.get_size()

    def get_size(self):
        h = self.ps * self.H
        v = self.ps * self.V
        diag = math.sqrt(h ** 2 + v ** 2)
        return h, v, diag

    def get_resolution(self):
        return self.H * self.V

    def get_lens_f_h(self, fov):
        f = self.h / 2.0 / math.tan(fov / 2.0)
        return f

    def get_lens_f_v(self, fov):
        f = self.v / 2.0 / math.tan(fov / 2.0)
        return f

    def get_lens_f_diag(self, fov):
        f = self.diag / 2.0 / math.tan(fov / 2.0)
        return f


class Camera:
    def __init__(self, cmos, lens_f):
        self.cmos = cmos
        self.lens_f = lens_f

    def get_fov_h(self):
        h, _, _ = self.cmos.get_size()
        return 2.0 * math.atan(h / 2.0 / self.lens_f)

    def get_fov_v(self):
        _, v, _ = self.cmos.get_size()
        return 2.0 * math.atan(v / 2.0 / self.lens_f)

    def get_swath_h(self, agl):
        fov = self.get_fov_h()
        swath = 2 * agl * math.tan(fov / 2.0)
        return swath

    def get_swath_v(self, agl):
        fov = self.get_fov_v()
        swath = 2 * agl * math.tan(fov / 2.0)
        return swath

    def get_smallest_feature_h(self, agl):
        swath = self.get_swath_h(agl)
        smallest_feature = 2 * swath / self.cmos.H
        return smallest_feature

    def get_smallest_feature_v(self, agl):
        swath = self.get_swath_v(agl)
        smallest_feature = 2 * swath / self.cmos.V
        return smallest_feature


def cal_sensor(coms: Cmos, lens_f, agl):
    # h, v, diag = coms.get_size()
    # fov_ang = cal_fov_ang(h, lens_f)
    # swath = cal_fov_width(fov_ang, agl)
    # smallest_feature = cal_rsl_w(swath, coms.H)
    cam = Camera(coms, lens_f)
    swath = cam.get_swath_h(agl)
    fov_ang = cam.get_fov_h()
    smallest_feature = cam.get_smallest_feature_h(agl)
    return swath, fov_ang, smallest_feature


if __name__ == "__main__":
    IMX541 = Cmos(2.74 / 1000, 4504, 4504, name="IMX541")
    IMX540 = Cmos(2.74 / 1000, 5320, 4600, name="IMX540")
    IMX677 = Cmos(1.12 / 1000, 5700, 5160, name="IMX677")
    IMX366 = Cmos(4.40 / 1000, 8228, 5574, name="IMX366")
    IMX455 = Cmos(3.76 / 1000, 9602, 6498, name="IMX455")
    IMX571 = Cmos(3.76 / 1000, 6280, 4264, name="IMX571")
    SonyBSI = Cmos(2.48 / 1000, 9600, 6376, name="Sony BSI")
    IMX264 = Cmos(3.45 / 1000, 2448, 2048, name="IMX264")
    Cannon5D = Cmos(5.36 / 1000, 6720, 4480, name="Cannon 5D mark IV")
    SonyILx = Cmos(3.8 / 1000, 9504, 6336, name="SonyILx")
    # sensor_list = [IMX366, IMX455, IMX540, IMX541, IMX571, IMX677, SonyBSI, Cannon5D]
    sensor_list = [IMX541, IMX540, IMX264, SonyILx]
    lens_list = [8, 12, 16, 20, 24,35, 50]
    agl = 4500
    with open("rst.csv", "w") as f:
        f.write("Sensor,lens(mm),AGL,fov(deg),swath,smallest feature, pixel size, H, V\n")
        for s in sensor_list:
            for lens in lens_list:
                swath, fov_ang, smallest_feature = cal_sensor(s, lens, agl)
                fov_deg = math.degrees(fov_ang)
                if 40 <= fov_deg <= 90:
                    print(s.name, "    lens: ", lens, "    fov: ", fov_deg, "    swath:", swath,
                          "    smallest feature: ", smallest_feature)
                    line = s.name + "," + str(lens) + "," + str(agl) + "," + str(fov_deg) + "," + \
                           str(swath) + "," + str(smallest_feature) + "," + str(s.ps) + "," + str(s.H) + "," + str(
                        s.V) + "\n"
                    f.write(line)
