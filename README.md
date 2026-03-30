# Small-Drone (MİLO)
A small assistant drone that responds to voice commands and tracks using a video tracking system.
This project is a smart drone system that is compact in size, can follow the user using both Bluetooth (BLE) signals and computer vision, and can understand and respond to voice commands.
-------------------------------------
🚀Key Features
1. Hybrid Tracking System: Coarse positioning with Bluetooth RSSI data, precise visual lock-on with camera data.
2. Voice Command Interface: Natural Language Processing (NLP) logic for recognizing commands such as "Follow me" and "Land".
3. Autonomous Decision Mechanism: Smooth movement capability thanks to PID controller.
4. Compact Design: Small enough to fit in the palms of two hands (Whoop type) chassis architecture.
-------------------------------------
Software and Algorithms
1. Distance Estimation (RSSI)
The drone calculates the distance of the chip (phone) in hand using the Log-Distance Path Loss model:
d= 10**(A-RSSI/10n)  NOTE: Here, (A) represents the reference signal strength, and (n) represents the ambient coefficient.
2. Motion Control (PID)
The PID algorithm is used to minimize the margin of error for smooth tracking:
$$u(t) = K_p e(t) + K_i \int e(t)dt + K_d \frac{de(t)}{dt}$$ NOTE: K_p, K_i, K_d: Subscripted coefficients.
\int: Integral symbol.
\frac{de(t)}{dt}: Fractional derivative expression.
3. Computer Vision: The target is tracked in the image captured by the camera based on its distance from the center (x=160, y=120). The area occupied by the target on the screen determines the drone's forward and backward movement.
!!!!!
Future Plans
[ ] Integration of Kalman Filter for noise reduction.

[ ] Capability for more complex dialogues with LLM (Large Language Model).

[ ] Obstacle avoidance sensors.
