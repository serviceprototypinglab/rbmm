import matchmaker as mm
import time
import random

class Generator:
    def __init__(self):
        self.app = []
        self.res = []

    def generate(self, numapp, numres):
        for i in range(numapp):
            app = mm.Artefact()
            app.factors = self.generatefactors_app()
            self.app.append(app)
        for i in range(numres):
            res = mm.Resource()
            res.factors = self.generatefactors_res()
            self.res.append(res)

    def generatefactors_app(self):
        possible = ({"vulnerability": 0.8}, {"memory": 200}, {"runtime": "java"})
        sel = {}
        for p in possible:
            if random.choice([0, 1, 2]) < 2:
                for k, v in p.items():
                    sel[k] = v
        return sel

    def generatefactors_res(self):
        possible = ({"location": "intranet"}, {"memory": 800}, {"memory": 150}, {"location": "dmz"}, {"runtime": "java"})
        sel = {}
        for p in possible:
            if random.choice([0, 1, 2]) < 2:
                for k, v in p.items():
                    sel[k] = v
        return sel

    def benchmatch(self):
        dep_rules = {
            "vulnerability": ("location", "=", "dmz"),
            "memory": ("memory", ">=", mm.IDENTITY),
            "runtime": ("runtime", "=", mm.IDENTITY)
        }

        acc_rules = {
            "memory": "-"
        }

        m = mm.Matchmaker()

        ts1 = time.time()
        mapping = m.match(self.app, self.res, dep_rules, None)
        te1 = time.time()

        m.setrec(len(self.app))

        ts2 = time.time()
        mapping = m.match(self.app, self.res, dep_rules, acc_rules)
        te2 = time.time()

        appfactors = sum([len(x.factors) for x in self.app])
        resfactors = sum([len(x.factors) for x in self.res])

        print(f"{len(self.app)} apps X {len(self.res)} resources = {len(self.app) * len(self.res)} mapping possibilities")
        print(f"with {appfactors} X {resfactors} = {appfactors * resfactors} factors")
        print(f"= {len(mapping)} valid mappings")
        print(f"= {te1 - ts1}s in combinatorial mode (infinite resources / hypothetical scenarios)")
        print(f"= {te2 - ts2}s in recursive mode (limited resources / realistic scenarios)")

if __name__ == "__main__":
    g = Generator()
    g.generate(200, 200)
    g.benchmatch()
