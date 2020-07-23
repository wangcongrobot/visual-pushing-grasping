########################################################################
#
# Copyright (c) 2020, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl


class Camera(object):

    def __init__(self):

        # Create a Camera object
        self.zed = sl.Camera()

        # Create a InitParameters object and set configureation parameters
        self.init_params = sl.InitParameters()
        self.init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use PERFORMANCE depth mode
        self.init_params.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
        self.init_params.camera_resolution = sl.RESOLUTION.HD720 # HD1080
        self.init_params.camera_fps = 30 # Set fps at 30

        # Open the camera
        err = self.zed.open(self.init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            exit(1)


        # Create and set RuntimeParameters after opening the camera
        self.runtime_parameters = sl.RuntimeParameters()
        self.runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  # Use STANDARD sensing mode
        # Setting the depth confidence parameters
        self.runtime_parameters.confidence_threshold = 100
        self.runtime_parameters.textureness_confidence_threshold = 100

        # Data options
        self.im_height = 720
        self.im_width = 1280
        self.buffer_size = 4098

    def get_data(self):

        # Capture images and depth
        i = 0
        color_img = sl.Mat()
        depth_img = sl.Mat()
        point_cloud_img = sl.Mat()

        # mirror_ref = sl.Transform()
        # mirror_ref.set_translation(sl.Translation(2.75, 4.0, 0))
        # tr_np = mirror_ref.m

        while i < 5:
            # A new image is available if grab() returns SUCCESS
            if self.zed.grab(self.runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                # Retrieve left image
                self.zed.retrieve_image(color_img, sl.VIEW.LEFT)
                # Retrieve depth map. Depth is aligned on the left image
                self.zed.retrieve_measure(depth_img, sl.MEASURE.DEPTH)
                # Retrieve colored point cloud. Point cloud is aligned on the left image.
                self.zed.retrieve_measure(point_cloud_img, sl.MEASURE.XYZRGBA)
            i += 1
            print("color_img: ", color_img)
            print("dpeth_img: ", depth_img)

        return color_img, depth_img

    def __del__(self):
        # Close the camera
        self.zed.close()
