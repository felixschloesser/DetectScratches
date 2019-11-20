#!/usr/bin/env python

from fcntl import ioctl
from PIL import Image, ImageFile
import mmap
import os
from io import BytesIO
import struct
import v4l2
import sys
sys.path.append("/home/tintin/rongheng/cv/")


NUM_BUFFERS = 10


class Camera(object):
    """The camera object, handles mainly IO."""
    def __init__(self, device_name):
        """Initialize object with the name of the device, ex: /dev/video0."""
        self.device_name = device_name
        self.open_device()
        self.init_device()

    def open_device(self):
        """Set the file discriptor to the openend camera Object."""
        self.fd = os.open(self.device_name, os.O_RDWR, 0)

    def init_device(self):
        cap = v4l2.v4l2_capability()
        fmt = v4l2.v4l2_format()

        ioctl(self.fd, v4l2.VIDIOC_QUERYCAP, cap)

        if not (cap.capabilities & v4l2.V4L2_CAP_VIDEO_CAPTURE):
            raise Exception("{} is not a video capture \
                             device".format(self.device_name))

        fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        ioctl(self.fd, v4l2.VIDIOC_G_FMT, fmt)

        self.init_mmap()

    def init_mmap(self):
        req = v4l2.v4l2_requestbuffers()

        req.count = NUM_BUFFERS
        req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        req.memory = v4l2.V4L2_MEMORY_MMAP

        try:
            ioctl(self.fd, v4l2.VIDIOC_REQBUFS, req)
        except Exception:
            raise Exception("video buffer request failed")

        if req.count < 2:
            raise Exception("Insufficient buffer memory \
                             on {}".format(self.device_name))
        self.buffers = []
        for x in range(req.count):
            buf = v4l2.v4l2_buffer()
            buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
            buf.memory = v4l2.V4L2_MEMORY_MMAP
            buf.index = x

            ioctl(self.fd, v4l2.VIDIOC_QUERYBUF, buf)

            buf.buffer = mmap.mmap(self.fd, buf.length, mmap.PROT_READ,
                                   mmap.MAP_SHARED, offset=buf.m.offset)
            self.buffers.append(buf)

    def start_capturing(self):
        for buf in self.buffers:
            ioctl(self.fd, v4l2.VIDIOC_QBUF, buf)
        video_type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        ioctl(self.fd, v4l2.VIDIOC_STREAMON, struct.pack('I', video_type))

    def process_image(self, buf):
        video_buffer = self.buffers[buf.index].buffer
        data = video_buffer.read(buf.bytesused)

        print("Verifing Image..")
        try:
            img = Image.open(BytesIO(data))
            video_buffer.seek(0)

            img.verify()
            assert img.format == 'JPEG'
            ImageFile.LOAD_TRUNCATED_IMAGES = True

            print('Valid image')

            img = Image.open(BytesIO(data))
            return img

        except Exception as e:
            print("Invalid image:", e)

    def get_frame(self):
        frame = None
        f = 0
        while frame is None:
            print("Grabbing Frame...")
            buf = self.buffers[f % NUM_BUFFERS]
            ioctl(self.fd, v4l2.VIDIOC_DQBUF, buf)
            frame = self.process_image(buf)
            ioctl(self.fd, v4l2.VIDIOC_QBUF, buf)
            f += 1
        return frame


if __name__ == "__main__":
    cam = Camera("/dev/video0")
    cam.start_capturing()
    img = cam.get_frame()
    img.show()
