import cv2
import numpy as np


def find_countur_of_threshold(start_point, gray_image, feather_edges, threshold):
    x, y = start_point
    start_pixel = gray_image[y][x]
    if feather_edges % 2 == 0:
        feather_edges += 1
    gray_image = cv2.medianBlur(gray_image, feather_edges)
    gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
    gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
    gray_image = np.where(gray_image == 0, gray_image, 255)
    contours = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours[1]:
        min_left = (
            min(contour, key=lambda x: x[0][0])[0][0], min(contour, key=lambda x: x[0][1])[0][1])
        max_right = (
            max(contour, key=lambda x: x[0][0])[0][0], max(contour, key=lambda x: x[0][1])[0][1])
        if start_point[0] > min_left[0] and start_point[0] < max_right[0] and start_point[1] > min_left[
            1] and start_point[1] < max_right[1]:
            target_contour = contour
    target_mask = np.zeros(gray_image.shape, dtype=np.uint8)
    cv2.fillPoly(target_mask, np.int32([target_contour]), (127, 127, 127))
    result_mask = target_mask + gray_image
    result_mask = np.where(result_mask != 255, result_mask, 0)
    result_mask = np.where(result_mask != 127, result_mask, 0)
    _, contours, hierarchy = cv2.findContours(result_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, target_contour


def find_all_counturs_of_threshold(start_point, gray_image, feather_edges, threshold):
    x, y = start_point
    start_pixel = gray_image[y][x]
    if feather_edges % 2 == 0:
        feather_edges += 1
    gray_image = cv2.medianBlur(gray_image, feather_edges)
    gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
    gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
    gray_image = np.where(gray_image == 0, gray_image, 255)
    contours = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def choise_selection_mask(image, selection_criterion):
    if selection_criterion == 'composite':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif selection_criterion == 'red':
        gray_image = self.image[:, :, 0]
    elif selection_criterion == 'green':
        gray_image = self.image[:, :, 1]
    elif selection_criterion == 'blue':
        gray_image = self.image[:, :, 2]
    else:
        temp_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        if selection_criterion == 'hue':
            gray_image = temp_image[:, :, 0]
        elif selection_criterion == 'lightness':
            gray_image = temp_image[:, :, 1]
        elif selection_criterion == 'saturation':
            gray_image = temp_image[:, :, 2]
    return gray_image




def main_function(image, cursor_coord_x, cursor_coord_y, wand, antialiasing, edges, threshold, mode, criterion, shape0, shape1, shape2, mask):
    image = np.frombuffer(image, dtype=np.uint8).reshape(shape0, shape1, shape2)
    mask = np.frombuffer(mask, dtype=np.uint8).reshape(shape0, shape1)
    start_point = (cursor_coord_x, cursor_coord_y)
    gray_image = choise_selection_mask(image, criterion)

    if wand == 1:
        all_contours, contour = find_countur_of_threshold(start_point, gray_image, edges, threshold)
        if mode == 3:
            mask_substract = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            cv2.fillPoly(mask_substract, [contour], (1, 1, 1))
            mask = mask + mask_substract
            mask = np.where(mask > 1, mask, 0)

        elif mode == 4:
            mask_substract = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            cv2.fillPoly(mask_substract, [contour], (2, 2, 2))
            mask = mask + mask_substract
            mask = np.where(mask < 2, mask, 0)
            mask *= 255

        else:
            for cnt in all_contours:
                if len(cnt) == len(contour):
                    cv2.fillPoly(mask, [cnt], (255, 255, 255))
                else:
                    cv2.fillPoly(mask, [cnt], (0, 0, 0))

    else:
        contours = find_all_counturs_of_threshold(start_point, gray_image, edges, threshold)
        if mode == 3:
            mask_substract = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            for contour in contours[1]:
                cv2.fillPoly(mask_substract, [contour], (1, 1, 1))
            mask = mask + mask_substract
            mask = np.where(mask > 1, mask, 0)

        elif mode == 4:
            mask_substract = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            for contour in contours[1]:
                cv2.fillPoly(mask_substract, [contour], (2, 2, 2))
            mask = mask + mask_substract
            mask = np.where(mask < 2, mask, 0)
            mask *= 255

        else:
            for contour in contours[1]:
                cv2.fillPoly(mask, np.int32([contour]), (255, 255, 255))

    contours_from_mask = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour_from_mask in contours_from_mask[1]:
        if antialiasing == 1:
            if cv2.contourArea(contour_from_mask) > 20:
                cv2.drawContours(image, [contour_from_mask], -1, (0, 255, 0), 1)
        else:
            cv2.drawContours(image, [contour_from_mask], -1, (0, 255, 0), 1)
    image = image.tobytes()
    mask = mask.tobytes()
    return image, mask
