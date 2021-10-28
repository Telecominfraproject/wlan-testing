#!/usr/bin/env python3

import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)


class VideoRates:
    def __init__(self):
        self.avail_stream_res = {
            # nicname             w,    h,  interlaced,   audio,    vid bps,   tt bps   framerate
            "sqvga-4:3": (160, 120, 0, 16000, 32000, 48000, 30),
            "sqvga-16:9": (160, 90, 0, 16000, 32000, 48000, 30),
            "qvga-4:3": (320, 240, 0, 16000, 32000, 48000, 30),
            "qvga-16:9": (320, 180, 0, 16000, 32000, 48000, 30),
            "qcif-48k-4:3": (144, 108, 0, 16000, 32000, 48000, 30),
            "qcif-48k-16:9": (192, 108, 0, 16000, 32000, 48000, 30),
            "qcif-96k-4:3": (192, 144, 0, 16000, 80000, 96000, 30),
            "qcif-96k-16:9": (256, 144, 0, 16000, 80000, 96000, 30),
            "cif": (352, 288, 0, 32000, 268000, 300000, 30),
            "cif-300k-4:3": (288, 216, 0, 32000, 268000, 300000, 30),
            "cif-300k-16:9": (384, 216, 0, 32000, 268000, 300000, 30),
            "cif-500k-4:3": (320, 240, 0, 32000, 468000, 500000, 30),
            "cif-500k-16:9": (384, 216, 0, 32000, 468000, 500000, 30),
            "d1-800k-4:3": (640, 480, 0, 32000, 768000, 800000, 30),
            "d1-800k-16:9": (852, 480, 0, 32000, 768000, 800000, 30),
            "d1-1200k-4:3": (640, 480, 0, 32000, 1168000, 1200000, 30),
            "d1-1200k-16:9": (852, 480, 0, 32000, 1168000, 1200000, 30),
            "hd-1800k-16:9": (1280, 720, 0, 64000, 1736000, 1800000, 59.94),
            "hd-2400k-16:9": (1280, 720, 0, 64000, 2272000, 2336000, 59.94),

            "108p4:3": (144, 108, 0, 16000, 32000, 48000, 30),
            "144p16:9": (192, 144, 0, 16000, 80000, 96000, 30),
            "216p4:3": (288, 216, 0, 32000, 268000, 300000, 30),
            "216p16:9": (384, 216, 0, 32000, 268000, 300000, 30),
            "240p4:3": (320, 240, 0, 32000, 468000, 500000, 30),

            "360p4:3": (480, 360, 0, 32000, 768000, 800000, 30),
            "480i4:3": (640, 480, 1, 32000, 768000, 800000, 30),
            "480p4:3": (640, 480, 0, 32000, 768000, 800000, 30),
            "480p16:9": (852, 480, 0, 32000, 1168000, 1200000, 30),

            # unadopted standard
            # "720i"          : ( 1280,  720,    1,        64000,  1736000,    1800000,    30),
            # 0.92 megapixels, 2.76MB per frame
            "720p": (1280, 720, 0, 64000, 1736000, 1800000, 59.94),

            # https://support.google.com/youtube/answer/1722171?hl=en
            # h.264 stream rates, SDR quality
            "yt-sdr-360p30": (640, 360, 0, 128000, 1000000, 1128000, 30),
            "yt-sdr-480p30": (852, 480, 0, 128000, 2500000, 2628000, 30),
            "yt-sdr-720p30": (1280, 720, 0, 384000, 5000000, 5384000, 30),
            "yt-sdr-1080p30": (1920, 1080, 0, 384000, 8000000, 8384000, 30),
            "yt-sdr-1440p30": (2560, 1440, 0, 512000, 16000000, 16512000, 30),
            "yt-sdr-2160p30": (3840, 2160, 0, 512000, 40000000, 40512000, 30),

            "yt-sdr-360p60": (640, 360, 0, 128000, 1500000, 1628000, 60),
            "yt-sdr-480p60": (852, 480, 0, 128000, 4000000, 4128000, 60),
            "yt-sdr-720p60": (1280, 720, 0, 384000, 7500000, 7884000, 60),
            "yt-sdr-1080p60": (1920, 1080, 0, 384000, 12000000, 12384000, 60),
            "yt-sdr-1440p60": (2560, 1440, 0, 512000, 24000000, 24512000, 60),
            "yt-sdr-2160p60": (3840, 2160, 0, 512000, 61000000, 61512000, 60),
            # "yt-hdr-360p60"  : ( 1280,  720,    0,        32000,  1000000,   1800000,    60), # yt unsupported
            # "yt-hdr-480p60"  : ( 1280,  720,    0,        32000,  1000000,   1800000,    60), # yt unsupported

            "yt-hdr-720p30": (1280, 720, 0, 384000, 6500000, 6884000, 30),
            "yt-hdr-1080p30": (1920, 1080, 0, 384000, 10000000, 10384000, 30),
            "yt-hdr-1440p30": (2560, 1440, 0, 512000, 20000000, 20512000, 30),
            "yt-hdr-2160p30": (3840, 2160, 0, 512000, 50000000, 50512000, 30),

            "yt-hdr-720p60": (1280, 720, 0, 384000, 9500000, 9884000, 60),
            "yt-hdr-1080p60": (1920, 1080, 0, 384000, 15000000, 15384000, 60),
            "yt-hdr-1440p60": (2560, 1440, 0, 512000, 30000000, 30512000, 60),
            "yt-hdr-2160p60": (3840, 2160, 0, 512000, 75500000, 76012000, 60),

            "raw720p30": (1280, 720, 0, 64000, 221120000, 221184000, 30),
            "raw720p60": (1280, 720, 0, 64000, 442304000, 442368000, 60),

            # frame size 6.2MB
            # 1080i60 1920x1080 186MBps
            "raw1080i": (1920, 540, 1, 128000, 1486384000, 1486512000, 59.94),
            "raw1080i30": (1920, 540, 1, 128000, 1487872000, 1488000000, 30),
            "raw1080i60": (1920, 540, 1, 128000, 1487872000, 1488000000, 60),

            # 1080p60 1920x1080 373MBps, 6.2Mbps frame size
            "raw1080p": (1920, 1080, 0, 128000, 2975872000, 2976000000, 60),

            # Skype requirements below as listed on https://support.skype.com/en/faq/FA1417/how-much-bandwidth-does-skype-need
            # ^--- indicates there is a minimum TX requirement for stations
            #      group calls range from 128k up to 512k up, roughly HQ-recommended, maybe 1280x720x15
            # https://www.quora.com/Does-Skype-support-1080p-HD-video-calls
            # https://tomtalks.blog/2018/04/set-skype-for-business-to-record-meetings-at-1080p-and-30-fps/
            # Transmission quality is fundamentally different than YouTube -- it is constant TX that varies by
            # the amount of compression available. Variation between minimum required bandwidth and recommended
            # bandwidth is visible in packet captures.
            # Actual capture resolutions depend on your camera and can be manipulated via settings, esp frame rate:
            # https://superuser.com/questions/180690/how-to-reduce-the-skype-video-settings-to-work-with-an-older-computer
            # https://lifehacker.com/how-to-get-better-quality-out-of-your-video-chats-5836186
            # https://docs.microsoft.com/en-us/skypeforbusiness/plan-your-deployment/clients-and-devices/video-resolutions
            # ^--- This outlines a requirements for 4 core processors as requirement for Skype at 720p!
            # Jed is roughly interpolating many of these values for this table
            # nicname                       w,    h,  interlaced,   audio,    vid bps,   tt bps   framerate
            "skype-vox-min": (0, 0, 0, 30000, 0, 30000, 0),
            "skype-vox-rcmd": (0, 0, 0, 100000, 0, 100000, 0),
            # screen sharing falls into min requirement
            "skype-vid-min": (424, 240, 0, 30000, 98000, 128000, 15),
            "skype-vid-rcmd": (640, 360, 0, 100000, 200000, 300000, 30),
            "skype-vid-hq-min": (960, 540, 0, 100000, 300000, 400000, 15),
            "skype-vid-hq-rcmd": (1280, 720, 0, 100000, 400000, 500000, 30),
            "skype-vid-hd-min": (1920, 1080, 0, 100000, 1100000, 1200000, 15),
            "skype-vid-hd-rcmd": (1920, 1080, 0, 100000, 1400000, 1500000, 30),
            "skype-vid-grp3-min": (640, 480, 0, 30000, 482000, 512000, 15),
            "skype-vid-grp3-rcmd": (1280, 720, 0, 100000, 900000, 2000000, 15),
            "skype-vid-grp5-min": (640, 360, 0, 30000, 1700000, 2000000, 15),
            "skype-vid-grp5-rcmd": (1280, 720, 0, 100000, 3700000, 4000000, 15),
            "skype-vid-grp7-min": (640, 360, 0, 30000, 3700000, 4000000, 15),
            "skype-vid-grp7-rcmd": (1280, 720, 0, 100000, 7700000, 8000000, 15)
        }

        """ 
        Below items are sorted by "tt bps" of tuple, -2 mostly for youtube rates
        """
        self.sdr_30_fps_rates = {}
        self.sdr_60_fps_rates = {}
        self.hdr_30_fps_rates = {}
        self.hdr_60_fps_rates = {}
        self.raw_1080i30 = {}
        self.raw_1080i60 = {}

        for (stream_name, stream_params) in sorted(self.avail_stream_res, key=lambda x: x[1][-2]):
            if (stream_name.startswith("raw")):
                if stream_params[-1] == 30:
                    self.raw_1080i30[stream_params[-2]] = stream_name
                if stream_params[-1] > 59:
                    self.raw_1080i60[stream_params[-2]] = stream_name
                continue

            if stream_name.find("-hdr-"):
                if stream_params[-1] == 30:
                    self.hdr_30_fps_rates[stream_params[-1]] = stream_name

                if stream_params[-1] > 59:
                    self.hdr_60_fps_rates[stream_params[-1]] = stream_name
                continue

            if stream_params[-1] == 30:
                self.sdr_30_fps_rates[stream_params[-2]] = stream_name

            if stream_params[-1] > 59:
                self.sdr_60_fps_rates[stream_params[-2]] = stream_name

    def rate_matches_30fps_sdr(self, live_rate):
        prev_rate_name = None
        for (rate_limit, name) in self.sdr_30_fps_rates.items():
            prev_rate_name = name
            if live_rate < rate_limit:
                return prev_rate_name
        return prev_rate_name

    def rate_matches_30fps_hdr(self, live_rate):
        prev_rate_name = None
        for (rate_limit, name) in self.hdr_30_fps_rates.items():
            prev_rate_name = name
            if live_rate < rate_limit:
                return prev_rate_name
        return prev_rate_name

    def rate_matches_60fps_sdr(self, live_rate):
        prev_rate_name = None
        for (rate_limit, name) in self.sdr_60_fps_rates.items():
            prev_rate_name = name
            if live_rate < rate_limit:
                return prev_rate_name
        return prev_rate_name

    def rate_matches_60fps_hdr(self, live_rate):
        prev_rate_name = None
        for (rate_limit, name) in self.hdr_30_fps_rates.items():
            prev_rate_name = name
            if live_rate < rate_limit:
                return prev_rate_name
        return prev_rate_name

#