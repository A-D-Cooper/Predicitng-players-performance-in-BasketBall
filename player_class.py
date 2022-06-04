


class player:

    def __init__(self, name, cost, pp, position, data, p_pos, tm, opp):
        self.cost = cost
        self.pp = pp
        self.name = name
        self.position = position
        self.data = data
        self.p_pos = p_pos
        self.tm = tm
        self.opp = opp


class team:

    def __init__(self, name, opp):
        self.name = name
        self.opp = opp
        self.players = []


class algo:

    def __init__(self, lst):
        self.all = lst
        self.b = lst
        self.pg, self.sg, self.sf, self.pf, self.c, self.f, self.g, self.util = [], [], [], [], [], [], [], []
        self.c1, self.c2, self.c3, self.c4, self.c5, self.c6 = 0, 0, 0, 0, 0, 0
        self.player_pg, self.player_sg, self.player_sf, self.player_pf, self.player_c, self.player_g, self.player_f, self.player_u = None, None, None, None, None, None, None, None
        self.combo = []

    def fill_lsts(self):

        for i in self.all:
            if 'SG' in i.position:
                self.sg.append(i)
            if 'PG' in i.position:
                self.pg.append(i)
            if 'SF' in i.position:
                self.sf.append(i)
            if 'PF' in i.position:
                self.pf.append(i)
            if 'C' in i.position:
                self.c.append(i)
            if 'G' in i.position:
                self.g.append(i)
            if 'F' in i.position:
                self.f.append(i)
            self.util.append(i)
        self.pg.sort(key=lambda x: x.pp, reverse=True)
        self.sg.sort(key=lambda x: x.pp, reverse=True)
        self.pf.sort(key=lambda x: x.pp, reverse=True)
        self.sf.sort(key=lambda x: x.pp, reverse=True)
        self.c.sort(key=lambda x: x.pp, reverse=True)
        self.g.sort(key=lambda x: x.pp, reverse=True)
        self.f.sort(key=lambda x: x.pp, reverse=True)
        self.util.sort(key=lambda x: x.pp, reverse=True)
        #print(len(self.sg), len(self.pg), len(self.sf), len(self.pf), len(self.c), len(self.g), len(self.f), len(self.util))

    def cost(self):
        c = 0
        for i in self.combo:
            c += i.cost
        return c

    def init(self):

        while True:
            pg = self.pg.pop(0)
            if pg not in self.combo:
                self.combo.append(pg)
                self.player_pg = pg
                break

        while True:
            #print(self.sg, "sg")
            sg = self.sg.pop(0)
            if sg not in self.combo:
                self.combo.append(sg)
                self.player_sg = sg
                break

        while True:
            sf = self.sf.pop(0)
            if sf not in self.combo:
                self.combo.append(sf)
                self.player_sf = sf
                break

        while True:
            pf = self.pf.pop(0)
            if pf not in self.combo:
                self.combo.append(pf)
                self.player_pf = pf
                break

        while True:
            g = self.g.pop(0)
            if g not in self.combo:
                self.combo.append(g)
                self.player_g = g
                break

        while True:
            c = self.c.pop(0)
            if c not in self.combo:
                self.combo.append(c)
                self.player_c = c
                break

        while True:
            f = self.f.pop(0)
            if f not in self.combo:
                self.combo.append(f)
                self.player_f = f
                break

        while True:
            util = self.util.pop(0)
            if util not in self.combo:
                self.combo.append(util)
                self.player_u = util
                break


    def best(self):
        #print(len(self.sg), len(self.pg), len(self.sf), len(self.pf), len(self.c), len(self.g), len(self.f), len(self.util))
        if (self.pg[0].pp >= self.sg[0].pp) and (self.pg[0].pp >= self.sf[0].pp) and (self.pg[0].pp >= self.pf[0].pp) and (self.pg[0].pp >= self.c[0].pp) and (self.pg[0].pp >= self.g[0].pp) and (self.pg[0].pp >= self.f[0].pp) and (self.pg[0].pp >= self.util[0].pp):
            return 'pg'
        elif (self.sg[0].pp >= self.pg[0].pp) and (self.sg[0].pp >= self.sf[0].pp) and (self.sg[0].pp >= self.pf[0].pp) and (self.sg[0].pp >= self.c[0].pp) and (self.sg[0].pp >= self.g[0].pp) and (self.sg[0].pp >= self.f[0].pp) and (self.sg[0].pp >= self.util[0].pp):
            return 'sg'
        elif (self.sf[0].pp >= self.pg[0].pp) and (self.sf[0].pp >= self.sg[0].pp) and (self.sf[0].pp >= self.pf[0].pp) and (self.sf[0].pp >= self.c[0].pp) and (self.sf[0].pp >= self.g[0].pp) and (self.sf[0].pp >= self.f[0].pp) and (self.sf[0].pp >= self.util[0].pp):
            return 'sf'
        elif (self.pf[0].pp >= self.pg[0].pp) and (self.pf[0].pp >= self.sg[0].pp) and (self.pf[0].pp >= self.sf[0].pp) and (self.pf[0].pp >= self.c[0].pp) and (self.pf[0].pp >= self.g[0].pp) and (self.pf[0].pp >= self.f[0].pp) and (self.pf[0].pp >= self.util[0].pp):
            return 'pf'
        elif (self.c[0].pp >= self.pg[0].pp) and (self.c[0].pp >= self.sg[0].pp) and (self.c[0].pp >= self.sf[0].pp) and (self.c[0].pp >= self.pf[0].pp) and (self.c[0].pp >= self.g[0].pp) and (self.c[0].pp >= self.f[0].pp) and (self.c[0].pp >= self.util[0].pp):
            return 'c'
        elif (self.g[0].pp >= self.pg[0].pp) and (self.g[0].pp >= self.sg[0].pp) and (self.g[0].pp >= self.sf[0].pp) and (self.g[0].pp >= self.pf[0].pp) and (self.g[0].pp >= self.c[0].pp) and (self.g[0].pp >= self.f[0].pp) and (self.g[0].pp >= self.util[0].pp):
            return 'g'
        elif (self.f[0].pp >= self.pg[0].pp) and (self.f[0].pp >= self.sg[0].pp) and (self.f[0].pp >= self.sf[0].pp) and (self.f[0].pp >= self.pf[0].pp) and (self.f[0].pp >= self.c[0].pp) and (self.f[0].pp >= self.g[0].pp) and (self.f[0].pp >= self.util[0].pp):
            return 'f'
        elif (self.util[0].pp >= self.pg[0].pp) and (self.util[0].pp >= self.sg[0].pp) and (self.util[0].pp >= self.sf[0].pp) and (self.util[0].pp >= self.pf[0].pp) and (self.util[0].pp >= self.c[0].pp) and (self.util[0].pp >= self.g[0].pp) and (self.util[0].pp >= self.f[0].pp):
            return 'util'


    def plug(self):

        while True:
            bst = self.best()
            #print(bst)
            if bst == 'pg':
                pg = self.pg.pop(0)
                if pg not in self.combo:
                    #pg = self.pg.pop(0)
                    self.combo.remove(self.player_pg)
                    self.combo.append(pg)
                    self.player_pg = pg
                    break

            if bst == 'sg':
                #print(self.sg)
                sg = self.sg.pop(0)
                if sg not in self.combo:
                    self.combo.remove(self.player_sg)
                    self.combo.append(sg)
                    self.player_sg = sg
                    break

            if bst == 'sf':
                sf = self.sf.pop(0)
                if sf not in self.combo:
                    self.combo.remove(self.player_sf)
                    self.combo.append(sf)
                    self.player_sf = sf
                    break

            if bst == 'pf':
                pf = self.pf.pop(0)
                if pf not in self.combo:
                    self.combo.remove(self.player_pf)
                    self.combo.append(pf)
                    self.player_pf = pf

            if bst == 'c':
                c = self.c.pop(0)
                if c not in self.combo:
                    self.combo.remove(self.player_c)
                    self.combo.append(c)
                    self.player_c = c
                    break

            if bst == 'g':
                g = self.g.pop(0)
                if g not in self.combo:
                    self.combo.remove(self.player_g)
                    self.combo.append(g)
                    self.player_g = g
                    break

            if bst == 'f':
                f = self.f.pop(0)
                if f not in self.combo:
                    self.combo.remove(self.player_f)
                    self.combo.append(f)
                    self.player_f = f
                    break

            if bst == 'util':
                util = self.util.pop(0)
                if util not in self.combo:
                    self.combo.remove(self.player_u)
                    self.combo.append(util)
                    self.player_u = util
                    break


    def comb(self, budget, n):
        #pop, remove
        t = True
        counter = 0
        combos = []
        while t:

            if budget < self.cost():
                print(self.cost())
                self.plug()
            else:
                print(self.cost())
                #print(self.combo)
                combos.append(self.combo)
                self.plug()
                counter += 1
                if counter == n:
                    break

        return combos

    def execute(self, budget=50000, n=1):
        self.fill_lsts()
        self.init()
        s = self.comb(budget, n)
        return s

