import math

# Parameters:
# uav_longitude - longitude of the center of the image in degrees
# uav_latitude - latitude of the center of the image in degrees
# uav_altitude - altitude of the uav in meters
# cam_fov - field of view of the camera in degrees
# img_width_px - width of the image in pixels
# img_height_px - height of the image in pixels
# obj_x_px - x coordinate of the target object in pixels
# obj_y_px - y coordinate of the target object in pixels
# Returns:
# (obj_longitude, obj_latitude) - the estimated longitude and latitude of the object

def locate(uav_longitude, uav_latitude, uav_altitude, bearing, cam_fov, img_width_px, img_height_px, obj_x_px, obj_y_px):
    cam_fov_rad = math.radians(cam_fov)
    diagonal_dist = math.tan(cam_fov_rad) * uav_altitude
    img_width = math.sqrt(diagonal_dist**2 / (1 + img_height_px / img_width_px)) # w^2 + (h/w)*w^2 = diag^2
    img_height = img_height_px / img_width_px * img_width
    length_per_px = img_width / img_width_px
    obj_x = obj_x_px * length_per_px
    obj_y = obj_y_px * length_per_px
    dist = math.sqrt(obj_x**2 + obj_y**2)
    theta = (90 - bearing) - math.atan(obj_y/obj_x) # Angle between the line through the center and object w.r.t. true bearing reference (ie. North)
    theta_rad = math.radians(theta)
    abs_x = dist * math.sin(theta_rad) # x distance in m relative to the bearing reference
    abs_y = dist * math.cos(theta_rad)
    # Approximate conversions
    # Latitude: 1 deg = 110.574 km
    # Longitude: 1 deg = 111.320*cos(latitude) km
    obj_longitude = uav_longitude + (abs_x / 1000) / 110.574
    obj_latitude = uav_latitude + (abs_y / 1000) / (111.320*math.cos(math.radians(uav_latitude)))
    return (obj_longitude, obj_latitude)


if __name__ == "__main__":
    uav_longitude = 56
    uav_latitude = -840
    uav_altitude = 1000
    bearing = 40
    cam_fov = 60
    img_width_px = 2000
    img_height_px = 1000
    obj_x_px = 1000
    obj_y_px = 500
    (obj_longitude, obj_latitude) = locate(uav_longitude=uav_longitude, uav_latitude=uav_latitude, uav_altitude=uav_altitude, bearing=bearing, cam_fov=cam_fov, img_width_px=img_width_px,
        img_height_px=img_height_px, obj_x_px=obj_x_px, obj_y_px=obj_y_px)
    print("obj_longitude={}, obj_latitude={}", obj_longitude, obj_latitude)