import cv2 as cv
import numpy as np


class MotionDetector:
    WIDTH = 1000
    HEIGHT = 600
    BLUR_THRESH = 10
    BLUR_KSIZE_SMALL = (5, 5)
    BLUR_KSIZE_MEDIUM = (9, 9)
    BLUR_KSIZE_LARGE = (11, 11)

    def __init__(self, is_webcam=False, video_path=None, camera_port=0, debug_mode=False):
        self.debug_mode = debug_mode
        self.is_webcam = is_webcam
        if is_webcam:
            self.cap = cv.VideoCapture(camera_port)
        else:
            self.video_path = video_path
            self.is_video_ended = False
            self.cap = cv.VideoCapture(video_path)
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.positions = []

    def release(self):
        self.cap.release()

    def replay_video(self):
        cv.destroyAllWindows()
        self.is_video_ended = False
        self.cap = cv.VideoCapture(self.video_path)

    def capture_motion(self):  # Captures two frames, whether it's from a webcam or a video
        if self.is_webcam:
            return self.capture_motion_webcam()
        else:
            return self.capture_motion_video()

    def capture_motion_webcam(self):  # TODO
        return

    def capture_motion_video(self):  # => return = array of ints
        cap = self.cap
        debug_mode = self.debug_mode
        if cap.isOpened():
            _, frame1_org = cap.read()
            ret, frame2_org = cap.read()
            if not ret:
                self.is_video_ended = True
                return None
            frame1_org = cv.resize(frame1_org, (self.WIDTH, self.HEIGHT))
            frame2_org = cv.resize(frame2_org, (self.WIDTH, self.HEIGHT))

            frame1 = frame1_org
            frame2 = frame2_org

            for i in range(2):
                frame1 = cv.blur(frame1, self.BLUR_KSIZE_MEDIUM)
                frame2 = cv.blur(frame2, self.BLUR_KSIZE_MEDIUM)

            motion_diff = cv.absdiff(frame1, frame2)
            if debug_mode: img1 = motion_diff
            gray = cv.cvtColor(motion_diff, cv.COLOR_BGR2GRAY)
            if debug_mode: img2 = gray

            thresh = cv.GaussianBlur(gray, self.BLUR_KSIZE_SMALL, 0)
            if debug_mode: img3 = thresh
            _, thresh = cv.threshold(thresh, self.BLUR_THRESH, 255, cv.THRESH_BINARY)
            if debug_mode: img4 = thresh

            thresh = cv.blur(thresh, self.BLUR_KSIZE_MEDIUM)
            if debug_mode: img5 = thresh
            _, thresh = cv.threshold(thresh, self.BLUR_THRESH, 255, cv.THRESH_BINARY)
            if debug_mode: img6 = thresh

            kernel = np.ones((5, 5), np.uint8)
            thresh = cv.dilate(thresh, kernel, iterations=15)
            thresh = cv.erode(thresh, kernel, iterations=15)

            contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            x_min = self.WIDTH
            x_max = 0
            y_min = self.HEIGHT
            y_max = 0

            m = None
            timestamp = round(self.cap.get(cv.CAP_PROP_POS_MSEC) / 1000, 3)

            for contour in contours:
                x, y, w, h = cv.boundingRect(contour)
                if x < x_min:
                    x_min = x
                if x + w > x_max:
                    x_max = x + w
                if y < y_min:
                    y_min = y
                if y + h > y_max:
                    y_max = y + h
            if x_min < x_max and y_min < y_max:
                m = ((x_min + x_max) // 2, (y_min + y_max) // 2)
            if debug_mode:
                cv.waitKey(int((1 / self.fps) * 1000))
                frame = frame2_org
                print('time stamp: ', int(cap.get(cv.CAP_PROP_POS_MSEC)) / 1000)
                print(f'number of detected objects: {len(contours)}')

                # drawings
                if x_min < x_max and y_min < y_max:
                    center = ((x_min + x_max) // 2, (y_min + y_max) // 2)
                    cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
                    cv.circle(img=frame, center=center, radius=1, color=(0, 0, 255), thickness=10)
                cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
                cv.imshow("Original", frame)
                # cv.imshow("Motion_diff_1", img1)
                cv.imshow("Motion_diff_2", img4)

            position = (timestamp, m)
            return position
        else:
            return None


def test1():
    cap = cv.VideoCapture(VIDEO_PATH)  # you can choose any video from your pc (the video while cap.isOpened():
    fps = int(cap.get(cv.CAP_PROP_FPS))
    resume = True
    while cap.isOpened():
        _, frame1_org = cap.read()
        ret, frame2_org = cap.read()
        if not ret:
            break

        # resize
        frame1_org = cv.resize(frame1_org, (WIDTH, HEIGHT))
        frame2_org = cv.resize(frame2_org, (WIDTH, HEIGHT))

        frame1 = frame1_org
        frame2 = frame2_org

        for i in range(2):
            frame1 = cv.blur(frame1, BLUR_KSIZE_MEDIUM)
            frame2 = cv.blur(frame2, BLUR_KSIZE_MEDIUM)

        motion_diff = cv.absdiff(frame1, frame2)
        gray = cv.cvtColor(motion_diff, cv.COLOR_BGR2GRAY)
        cv.imshow("motion_diff1", gray)

        thresh = cv.GaussianBlur(gray, BLUR_KSIZE_SMALL, 0)
        _, thresh = cv.threshold(thresh, BLUR_THRESH, 255, cv.THRESH_BINARY)
        cv.imshow("motion_diff2", thresh)

        thresh = cv.blur(thresh, BLUR_KSIZE_MEDIUM)
        _, thresh = cv.threshold(thresh, BLUR_THRESH, 255, cv.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        thresh = cv.dilate(thresh, kernel, iterations=15)
        thresh = cv.erode(thresh, kernel, iterations=15)

        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        x_min = WIDTH
        x_max = 0
        y_min = HEIGHT
        y_max = 0
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            if x < x_min:
                x_min = x
            if x + w > x_max:
                x_max = x + w
            if y < y_min:
                y_min = y
            if y + h > y_max:
                y_max = y + h

        # drawings
        cv.imshow("Original", frame2_org)
        frame = frame2_org
        cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
        if x_min < x_max and y_min < y_max:
            cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
            center = ((x_min + x_max) // 2, (y_min + y_max) // 2)
            cv.circle(img=frame, center=center, radius=1, color=(0, 0, 255), thickness=10)

        print('time stamp: ', int(cap.get(cv.CAP_PROP_POS_MSEC)) / 1000)
        print(f'number of detected objects: {len(contours)}')

        cv.imshow("Original-with-mask", frame)

        cv.imshow("Motion", thresh)
        cv.imshow("motion_diff", motion_diff)

        key = cv.waitKey(int((1 / fps) * 1000))
        if key == ord('r'):  # resume toggle
            resume = not resume
        if key == 27:  # Esc key
            break
        while key != ord('f') and not resume:  # Esc key
            key = cv.waitKey(0)
            if key == ord('r'):  # resume toggle
                resume = not resume
            if key == 27:  # Esc key
                cap.release()
                break
    cap.release()
    cv.destroyAllWindows()


def test2():
    Results = []
    entity = MotionDetector(video_path=VIDEO_PATH)
    entity.debug_mode = True
    while not entity.is_video_ended:
        result = entity.capture_motion()
        Results.append(result)
        print(result)
    print(Results)
    not_null_Results = [i for i in Results if i is not None and i[1] is not None]
    print(not_null_Results)
    print(f'total number of detected motions: {len(not_null_Results)}')
    print(f'first element: location:{not_null_Results[0][1]}, time:{not_null_Results[0][0]}')
    print(f'last element: location:{not_null_Results[-1][1]}, time:{not_null_Results[-1][0]}')


if __name__ == '__main__':
    VIDEO_PATH = '../video.MOV'

    WIDTH = 1000
    HEIGHT = 600
    BLUR_THRESH = 10
    BLUR_KSIZE_SMALL = (5, 5)
    BLUR_KSIZE_MEDIUM = (9, 9)
    BLUR_KSIZE_LARGE = (11, 11)

    test1()
    # test2()
