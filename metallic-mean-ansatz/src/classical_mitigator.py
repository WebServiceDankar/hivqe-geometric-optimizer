"""
Classical Mitigator — Regressão Linear por Mínimos Quadrados.

Responsabilidade:
  - Receber séries temporais (epoch, energy) da QPU.
  - Aplicar regressão linear em janela deslizante para filtrar ruído.
  - Detectar convergência quando o erro residual permanece baixo por N epochs.

Referência: CLAUDE.MD → seção "classical_mitigator.py"
"""


def compute_regression(points):
    """
    Calcula regressão linear por mínimos quadrados.

    Args:
        points: Lista de tuplas (x, y).

    Returns:
        Dict com {m, b, R2, SQR} ou None se cálculo impossível.
        - m:   coeficiente angular (inclinação)
        - b:   intercepto
        - R2:  coeficiente de determinação (0..1)
        - SQR: soma dos quadrados dos resíduos
    """
    n = len(points)
    if n < 2:
        return None

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    xm = sum(xs) / n
    ym = sum(ys) / n

    sXX = sum((x - xm) ** 2 for x in xs)
    sXY = sum((xs[i] - xm) * (ys[i] - ym) for i in range(n))
    sYY = sum((y - ym) ** 2 for y in ys)

    if sXX == 0:
        return None

    m = sXY / sXX
    b = ym - m * xm

    SQR = sum((ys[i] - (m * xs[i] + b)) ** 2 for i in range(n))
    R2 = 1 - SQR / sYY if sYY != 0 else 1.0
    R2 = max(0.0, R2)

    return {"m": m, "b": b, "R2": R2, "SQR": SQR}


class ClassicalMitigator:
    """
    Mitigador clássico com janela deslizante e detecção de convergência.

    Mantém um buffer dos últimos `window_size` pontos (epoch, energy),
    aplica regressão linear, e verifica se a energia predita permanece
    próxima do target por `patience` epochs consecutivos.
    """

    def __init__(self, window_size=5, target_energy=-5.609,
                 convergence_threshold=0.05, patience=5):
        self.window_size = window_size
        self.target_energy = target_energy
        self.convergence_threshold = convergence_threshold
        self.patience = patience

        self.buffer = []
        self._consecutive_close = 0

    def update(self, epoch, energy_raw):
        """
        Processa uma nova amostra de energia bruta da QPU.

        Args:
            epoch: Número da iteração (int).
            energy_raw: Energia bruta retornada pelo hardware/simulador (float).

        Returns:
            Dict com {energy_pred, m, b, R2, converged}.
        """
        self.buffer.append((epoch, energy_raw))

        # Manter janela deslizante
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)

        # Se dados insuficientes para regressão, retornar valor bruto
        if len(self.buffer) < 3:
            return {
                "energy_pred": energy_raw,
                "m": 0.0,
                "b": energy_raw,
                "R2": 0.0,
                "converged": False,
            }

        reg = compute_regression(self.buffer)

        if reg is None:
            energy_pred = energy_raw
            m, b, R2 = 0.0, energy_raw, 0.0
        else:
            m = reg["m"]
            b = reg["b"]
            R2 = reg["R2"]
            # Predição no epoch atual usando a reta ajustada
            energy_pred = m * epoch + b

        # Verificar convergência
        delta = abs(energy_pred - self.target_energy)
        if delta < self.convergence_threshold:
            self._consecutive_close += 1
        else:
            self._consecutive_close = 0

        converged = self._consecutive_close >= self.patience

        return {
            "energy_pred": energy_pred,
            "m": m,
            "b": b,
            "R2": R2,
            "converged": converged,
        }
