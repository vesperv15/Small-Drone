import time

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.time()

    def calculate(self, error):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0: dt= 1e-6
        # 1. Proportional (P)
        p_term = self.kp * error
        # 2. Integral (I) - Hataları topluyoruz
        self.integral += error * dt
        i_term = self.ki * self.integral
        # 3. Derivative (D) - Değişim hızına bakıyoruz (Sıçrama engelleyici)
        derivative = (error - self.prev_error) / dt
        d_term = self.kd * derivative
        # Toplam çıktı (Motorlara gidecek komut)
        output = p_term + i_term + d_term
        
        # Değerleri bir sonraki adım için sakla
        self.prev_error = error
        self.last_time = current_time
        
        return output