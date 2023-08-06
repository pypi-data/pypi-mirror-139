# Author : Kartik Panchal
# All required dependency
import math

import cv2
import mediapipe as mp


# ***********************

# Creating Hand Detector Class.
class MbHandDetector:

    # Constructor
    def __init__(self, iMaxHands=2, iMinDetectionCon=0.5):
        # important params
        self.maxHands = iMaxHands
        self.minDetectionCon = iMinDetectionCon

        # some useful variables for
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpDrawingStyles = mp.solutions.drawing_styles
        self.mpHands = mp.solutions.hands

        # configuring hand solutions from media pipe
        self.hands = self.mpHands.Hands(
            max_num_hands=self.maxHands,
            min_detection_confidence=self.minDetectionCon
        )

    # Detect hands method.
    def detectHands(self, inputImage):
        # first convert image from bgr to rgb
        inputImage.flags.writeable = False
        inputToRgb = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
        # now detecting hand
        result = self.hands.process(inputToRgb)

        if result.multi_hand_landmarks:
            # drawing hand skeleton
            for self.handLandmarks in result.multi_hand_landmarks:
                self.mpDrawing.draw_landmarks(
                    image=inputImage,
                    landmark_list=self.handLandmarks,
                    connections=self.mpHands.HAND_CONNECTIONS,
                    connection_drawing_spec=self.mpDrawingStyles.get_default_hand_connections_style()
                )
        return inputImage

