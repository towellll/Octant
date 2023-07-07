import math


class SBFL_compute(object):
    def __init__(self, ef, ep, nf, np):
        self.ep = ep
        self.ef = ef
        self.nf = nf
        self.np = np
        self.sus_list = []

    def __repr__(self):
        pass

    def ochiai(self) -> float:
        if (self.ef + self.nf) * (self.ef + self.ep):
            ochiai_sus = self.ef / math.sqrt((self.ef + self.nf) * (self.ef + self.ep))
        else:
            ochiai_sus = 0.0

        return ochiai_sus

    def dstar(self) -> float:
        if self.nf + self.ep:
            dstar_sus = self.ef * self.ef / (self.nf + self.ep)
        else:
            dstar_sus = 0.0

        return dstar_sus

    def ochiai2(self) -> float:
        if (self.ef + self.ep) * (self.ef + self.np) * (self.nf + self.np) * (self.ep + self.nf):
            ochiai2_sus = self.ef * self.np / math.sqrt(
                (self.ef + self.ep) * (self.ef + self.np) * (self.nf + self.np) * (self.ep + self.nf))
        else:
            ochiai2_sus = 0.0
        return ochiai2_sus

    def gp02(self) -> float:
        gp02_sus = 2 * (self.ef + math.sqrt(self.np)) + math.sqrt(self.ep)
        return gp02_sus

    def gp03(self) -> float:
        gp03_sus = math.sqrt(abs(self.ef * self.ef - math.sqrt(self.ep)))
        return gp03_sus

    def gp13(self) -> float:
        if (2 * self.ep + self.ef):
            gp13_sus = self.ef * (1 + self.ep / (2 * self.ep + self.ef))
        else:
            gp13_sus = 0.0
        return gp13_sus

    def gp19(self) -> float:
        gp19_sus = self.ef * math.sqrt(abs(self.ep - self.ef + self.nf - self.np))
        return gp19_sus

    def jaccard(self) -> float:
        if self.ef + self.nf + self.ep:
            jaccard_sus = self.ef / (self.ef + self.nf + self.ep)
        else:
            jaccard_sus = 0.0
        return jaccard_sus

    def wong2(self) -> float:
        if self.ef + self.ep:
            wong2_sus = self.ef / (self.ef + self.ep)
        else:
            wong2_sus = 0.0
        return wong2_sus

    def tarantula(self) -> float:
        if (self.ef + self.nf) and (self.ep + self.np):
            if (self.ef / (self.ef + self.nf)) + (self.ep / (self.ep + self.np)):
                tarantula_sus = (self.ef / (self.ef + self.nf)) / (
                        (self.ef / (self.ef + self.nf)) + (self.ep / (self.ep + self.np)))
            else:
                tarantula_sus = 0.0
        else:
            tarantula_sus = 0.0
        return tarantula_sus

    def barinel(self) -> float:
        if self.ep + self.ef:
            barinel_sus = 1 - self.ep / (self.ep + self.ef)
        else:
            barinel_sus = 0.0
        return barinel_sus


if __name__ == '__main__':
    example = SBFL_compute(0, 3, 2, 2)
