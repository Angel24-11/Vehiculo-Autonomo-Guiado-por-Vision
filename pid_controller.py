import time
import json


class PIDController:
    def __init__(self, Kp=0.0, Ki=0.0, Kd=0.0, setpoint=0, output_limits=(-255, 255)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        self._integral = 0.0
        self._prev_error = 0.0
        self._last_time = None
        self._last_output = 0.0

        self._metrics = {
            "error": 0.0,
            "integral": 0.0,
            "derivative": 0.0,
            "output": 0.0,
            "pwm_left": 0,
            "pwm_right": 0,
            "dt": 0.0,
            "fps": 0.0,
        }

    def compute(self, error, dt=None):
        if dt is None:
            now = time.perf_counter()
            if self._last_time is not None:
                dt = now - self._last_time
            else:
                dt = 1.0 / 60.0
            self._last_time = now

        if dt <= 0:
            dt = 1e-6

        p_term = self.Kp * error
        d_term = self.Kd * (error - self._prev_error) / dt

        self._integral += error * dt
        i_raw = self.Ki * self._integral

        output = p_term + i_raw + d_term
        output = self._clamp(output, self.output_limits[0], self.output_limits[1])

        if self.Ki != 0.0:
            i_actual = output - p_term - d_term
            self._integral = i_actual / self.Ki if self.Ki != 0 else 0.0

        self._prev_error = error
        self._last_output = output

        fps = 1.0 / dt if dt > 0 else 0.0
        self._metrics = {
            "error": round(error, 2),
            "integral": round(self._integral, 4),
            "derivative": round(d_term, 4),
            "output": round(output, 2),
            "pwm_left": 0,
            "pwm_right": 0,
            "dt": round(dt, 6),
            "fps": round(fps, 1),
        }

        return output

    def reset(self):
        self._integral = 0.0
        self._prev_error = 0.0
        self._last_time = None
        self._last_output = 0.0
        self._metrics = {k: 0.0 if isinstance(v, (int, float)) else v for k, v in self._metrics.items()}
        self._metrics["error"] = 0.0
        self._metrics["pwm_left"] = 0
        self._metrics["pwm_right"] = 0

    def tune(self, Kp=None, Ki=None, Kd=None):
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd

    def map_to_pwm(self, u, base_speed=100):
        pwm_left = self._clamp(base_speed + u, 0, 255)
        pwm_right = self._clamp(base_speed - u, 0, 255)

        self._metrics["pwm_left"] = int(pwm_left)
        self._metrics["pwm_right"] = int(pwm_right)

        return int(pwm_left), int(pwm_right)

    def get_metrics(self):
        return dict(self._metrics)

    def metrics_to_csv_line(self):
        m = self._metrics
        return f"{m['error']},{m['integral']},{m['derivative']},{m['output']},{m['pwm_left']},{m['pwm_right']},{m['dt']},{m['fps']}"

    def _clamp(self, value, min_val, max_val):
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value

    def __repr__(self):
        return (f"PIDController(Kp={self.Kp}, Ki={self.Ki}, Kd={self.Kd}, "
                f"setpoint={self.setpoint}, limits={self.output_limits})")


class NavegadorFSM:
    def __init__(self, pid_controller):
        self.pid = pid_controller
        self.estado = "SEGUIMIENTO"
        self.tiempo_estado = 0.0
        self.duracion_giro = 1.0
        self.duracion_rebaso = 2.0
        self.duracion_retorno = 1.0

    def actualizar_estado(self, error_camara, obstaculo_detectado):
        tiempo_actual = time.perf_counter()

        # 1. Seguimiento normal de línea
        if self.estado == "SEGUIMIENTO":
            if obstaculo_detectado:
                print("¡Obstáculo detectado! Iniciando maniobra de evasión...")
                self.estado = "GIRO_EVASION"
                self.tiempo_estado = tiempo_actual
                return 0, 150
            else:

                correccion = self.pid.compute(error_camara)
                return self.pid.map_to_pwm(correccion, base_speed=120)

        # 2. Girar para salir del carril
        elif self.estado == "GIRO_EVASION":
            if (tiempo_actual - self.tiempo_estado) > self.duracion_giro:
                self.estado = "AVANCE_REBASO"
                self.tiempo_estado = tiempo_actual
            return 0, 150

            # 3. Avanzar recto por el carril izquierdo (rebasando)
        elif self.estado == "AVANCE_REBASO":
            if (tiempo_actual - self.tiempo_estado) > self.duracion_rebaso:
                self.estado = "REALINEACION"
                self.tiempo_estado = tiempo_actual
            return 120, 120

            # 4. Volver a meterse a la línea blanca
        elif self.estado == "REALINEACION":
            if (tiempo_actual - self.tiempo_estado) > self.duracion_retorno:
                self.estado = "SEGUIMIENTO"
                self.pid.reset()
            return 150, 0
