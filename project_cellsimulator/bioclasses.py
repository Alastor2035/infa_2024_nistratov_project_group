import math
from requirements import *



class Cell:
    """Модель клетки с концентрациями и запасом АТФ."""
    
    def __init__(self, x, y):
        self.type = "Cell"
        self.x = x
        self.y = y
        self.K = DEFAULT_K
        self.Na = DEFAULT_NA
        self.ATP = DEFAULT_ATP
        self.delta = 99
        self.contacts = []

    def to_dict(self):
        """Вернуть состояние клетки в виде словаря."""
        return {
            "x": self.x,
            "y": self.y,
            "K": self.K,
            "Na": self.Na,
            "ATP": self.ATP
        }


class ExtracellularSpace:
    """Внеклеточное пространство с заданными концентрациями."""
    
    def __init__(self, x, y):
        self.type = "ECS"
        self.x = x
        self.y = y
        self.delta = 99
        self.ATP = 0
        self.K = DEFAULT_ECS_K
        self.Na = DEFAULT_ECS_NA

    def to_dict(self):
        """Вернуть состояние внеклеточного пространства."""
        return {
            "x": self.x,
            "y": self.y,
            "K": self.K,
            "Na": self.Na
        }


class CellContact:
    """Контакт между двумя средами: пассивный и активный транспорт."""
    
    def __init__(self, source, target, delta, membrane_permeability=DEFAULT_P_K, membrane_thickness=DEFAULT_THICKNESS):
        self.source = source
        self.target = target
        self.P_K = membrane_permeability
        self.thickness = membrane_thickness
        self.Vmax = DEFAULT_VMAX
        self.Km = DEFAULT_KM
        self.delta = delta

    def transport(self, dt):
        """
        1) Пассивный транспорт по закону Фика.
        2) Активный Na⁺/K⁺-насос по кинетике Михаэлиса–Ментен.
        """
        # --- ПАССИВНЫЙ ТРАНСПОРТ (Фик) ---
        # J = P * (A / thickness) * (C_src - C_tgt)
        area = self.source.K * 1e-12
        flux_K = self.P_K * area / self.thickness * (self.source.K - self.target.K)
        dK = flux_K * dt
        dK_clamped = max(-self.source.K, min(self.target.K, dK)) * self.delta
        self.source.K -= dK_clamped
        self.target.K += dK_clamped

        # --- АКТИВНЫЙ ТРАНСПОРТ (Na⁺/K⁺-насос) ---
        # скорость насоса зависит от [Na]_source и [ATP]_source
        pump_rate = self.Vmax * (self.source.Na / (self.Km + self.source.Na))
        cycles = pump_rate * dt * (self.source.ATP / (self.Km + self.source.ATP))
        total_cycles = cycles * self.delta
        na_to_move = min(self.source.Na, 3 * total_cycles)
        k_to_move = min(self.target.K, 2 * total_cycles)
        atp_cost = total_cycles

        if self.source.ATP >= atp_cost:
            self.source.ATP -= atp_cost
            self.source.Na -= na_to_move
            self.target.Na += na_to_move
            self.target.K -= k_to_move
            self.source.K += k_to_move
