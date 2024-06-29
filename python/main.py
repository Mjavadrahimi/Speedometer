from math import tan, radians
from motionDetector import MotionDetector
from arduinoInterface import ArduinoI


def calculate_location(x, radius, fov) -> int:
    theta = x / WIDTH * fov
    alpha = fov / 2 - theta
    s = radius * (tan(radians(fov / 2)) - tan(radians(alpha)))
    s = round(s, 2)
    return s


def calculate_velocity(x1, x2, duration, radius, fov):
    loc_x1 = calculate_location(x1, radius, fov)
    loc_x2 = calculate_location(x2, radius, fov)
    velocity = abs(loc_x1 - loc_x2) / duration
    velocity = int(abs(velocity))
    return velocity


my_map = {
    "Start": {
        "Stop": None,
    },
    "Change Distance": None,
    "Change FoV": None,
    "Quit": None,
}

capture_duration = 5  # second
FoV = 72  # degree, iPhone 13 1x field of view
distance = 100  # cm
scale_distance = 'cm'  # cm | m | km
scale_time = 's'  # s / m / H
VIDEO_FILE_NAME = 'video.MOV'
VIDEO_PATH = '../' + VIDEO_FILE_NAME
WIDTH = MotionDetector.WIDTH

if __name__ == '__main__':
    while True:
        print("=" * 80)
        print(f'FoV is: {FoV} degree | distance is: {distance}{scale_distance} | scale is: {scale_distance}/{scale_time}')
        print("commands:")
        print("0) Run Speedometer")
        print("1) Modify distance")
        print("2) Modify distance scale")
        print("3) Modify time scale")
        print("4) Modify FoV")
        print("5) Quit")
        command = input("select your command: ")

        if command == "1":
            try:
                inp = int(input("Enter your distance: "))
                distance = inp
            except:
                print("Invalid number")
            continue
        elif command == "2":
            inp = input("Enter your distance scale | Options : cm, m, km: ").lower()
            if inp == "cm":
                scale_distance = 'cm'
            elif inp == "m":
                scale_distance = 'm'
            elif inp == "km":
                scale_distance = 'km'
            else:
                print("Invalid distance Scale")
            continue
        elif command == "3":
            inp = input("Enter your time scale | Options : s, m, h: ").lower()
            if inp == "s":
                scale_time = 's'
            elif inp == "m":
                scale_time = 'm'
            elif inp == "h":
                scale_time = 'h'
            else:
                print("Invalid time Scale")
            continue

        elif command == "4":
            try:
                inp = int(input("Enter your FoV: "))
                FoV = inp
            except:
                print("Invalid number")
            continue

        elif command == "5":
            quit()

        elif command != "0":
            print("Invalid command")
            continue

        myArduino = ArduinoI()
        entity = MotionDetector(video_path=VIDEO_PATH)
        entity.debug_mode = True
        Results = []
        print(f'Calculating velocity for "{VIDEO_FILE_NAME}"...')
        while not entity.is_video_ended:
            result = entity.capture_motion()
            Results.append(result)

        not_null_Results = [i for i in Results if i is not None and i[1] is not None]

        first_motion = not_null_Results[0]
        last_motion = not_null_Results[-1]
        # print(first_motion, last_motion)

        first_motion_time = first_motion[0]
        last_motion_time = last_motion[0]
        # print(first_motion_time, last_motion_time)

        first_motion_x = first_motion[1][0]
        last_motion_x = last_motion[1][0]
        # print(first_motion_x, last_motion_x)

        velocity = calculate_velocity(
            x1=first_motion_x, x2=last_motion_x,
            duration=first_motion_time - last_motion_time,
            radius=distance,
            fov=FoV
        )
        print()
        print(f' {"*"*3}  velocity = {velocity} {scale_distance}/{scale_time}  {"*"*3} ')
        print()
        myArduino.display(velocity)
        myArduino.close()
        entity.release()
        del myArduino
        del entity
