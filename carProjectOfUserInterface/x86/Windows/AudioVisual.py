import math
import random
import colorsys
import librosa.display
import numpy as np


# 创建随机色彩
def rnd_color():
    h, s, l = random.random(), 0.5 + random.random() / \
        2.0, 0.4 + random.random() / 5.0
    # 返回一个具有RGB色彩的列表
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]


def rgb2hex(color):
    r, g, b = int(color[0]), int(color[1]), int(color[2])
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def rotate(xy, theta):
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)
    return (xy[0] * cos_theta - xy[1] * sin_theta, xy[0] * sin_theta + xy[1] * cos_theta)


def translate(xy, offset):
    return xy[0] + offset[0], xy[1] + offset[1]


def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


class AudioAnalyzer:

    def __init__(self):

        self.frequencies_index_ratio = 0  # array for frequencies
        self.time_index_ratio = 0  # array of time periods
        # a matrix that contains decibel values according to frequency and time indexes
        self.spectrogram = None

    # 加载音频文件
    def load(self, filename):

        time_series, sample_rate = librosa.load(
            filename)  # getting information from the file

        # 通过时间序列与频率以获取振幅
        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

        # 将任意频率的振幅转换为分贝
        # converting the matrix to decibel matrix
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        # 获取基本频率分布
        frequencies = librosa.core.fft_frequencies(
            n_fft=2048*4)  # getting an array of frequencies

        # 通过采样率与分贝值获取每个音频帧的时间经过
        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(
            self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(times)/times[len(times) - 1]

        self.frequencies_index_ratio = len(
            frequencies)/frequencies[len(frequencies)-1]

    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (
            self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = clamp(self.min_height, self.max_height, self.height)


class AverageAudioBar(AudioBar):

    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height,
                         max_height, min_decibel, max_decibel)
        self.rng = rng
        self.avg = 0

    def update_all(self, dt, time, analyzer):
        self.avg = 0
        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)

        self.avg /= len(self.rng)
        self.update(dt, self.avg)


class RotatedAverageAudioBar(AverageAudioBar):

    def __init__(self, x, y, rng, color, angle=0, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height,
                         max_height, min_decibel, max_decibel)
        self.rng = rng
        self.rect = None
        self.angle = angle

    def update_rect(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.rect.rotate(self.angle)


class Rect:

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.points = []

        # origin定义原始坐标，offset定义目标坐标
        self.origin = [self.w/2, 0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]
        self.rotate(0)

    def rotate(self, angle):

        template = [
            (-self.origin[0], self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1] - self.h),
            (-self.origin[0], self.origin[1] - self.h)
        ]

        self.points = [
            translate(rotate(xy, math.radians(angle)), self.offset) for xy in template]


class AduioVisualize:

    def __init__(self):
        self.avg_bass = 0
        self.bass_trigger = -30
        self.bass_trigger_started = 0
        self.min_decibel = -80
        self.max_decibel = 80

        self.circle_color = (40, 40, 40)
        self.polygon_default_color = [255, 255, 255]
        self.polygon_bass_color = self.polygon_default_color.copy()
        self.poly_color = self.polygon_default_color.copy()
        self.polygon_color_vel = [0, 0, 0]

        self.bass = {"start": 70, "stop": 120, "count": 10}
        self.heavy_area = {"start": 120, "stop": 250, "count": 15}
        self.low_mids = {"start": 251, "stop": 1500, "count": 20}
        self.high_mids = {"start": 1501, "stop": 5000, "count": 15}

        self.poly = []
        self.bars = []



    def MainAnalyze(self, MusicFile,ScreenWidth,ScreenHeight):
        self.min_radius = ScreenWidth // 15
        self.max_radius = ScreenWidth // 12
        self.radius = self.min_radius
        self.radius_vel = 0

        self.analyzer = AudioAnalyzer()
        self.analyzer.load(MusicFile)

        self.circleX = int(ScreenWidth / 2)
        self.circleY = int(ScreenHeight / 2)

        freq_groups = [self.bass, self.heavy_area,
                       self.low_mids, self.high_mids]

        tmp_bars = []
        length = 0

        for group in freq_groups:
            g = []
            s = group["stop"] - group["start"]
            count = group["count"]
            reminder = s % count
            step = int(s/count)
            rng = group["start"]
            for _ in range(count):
                arr = None
                if reminder > 0:
                    reminder -= 1
                    arr = np.arange(start=rng, stop=rng + step + 2)
                    rng += step + 3
                else:
                    arr = np.arange(start=rng, stop=rng + step + 1)
                    rng += step + 2
                g.append(arr)
                length += 1
            tmp_bars.append(g)

        angle_dt = 360/length

        ang = 0

        for g in tmp_bars:
            gr = []
            for c in g:
                gr.append(
                    RotatedAverageAudioBar(self.circleX+self.radius*math.cos(math.radians(ang - 90)), self.circleY+self.radius*math.sin(math.radians(ang - 90)), c, (255, 0, 255), angle=ang, width=ScreenWidth//150, max_height=ScreenWidth//4))

                ang += angle_dt
            self.bars.append(gr)

