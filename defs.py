import numpy as np

p = 9 #nb de points de vie initial 
malus_mort = 30 #nb de points de vie pour une personne décédée 
min_eau = 1 #besoin en eau quotidien
min_miam = 1 #besoin en nourriture quotidien
ppe_f = 0.25 #production par unité d'eau des fermes
ppe_u = 0.5 #production par unité d'eau des usines

## Définition des différents agents 

class agent():
    def __init__(self, s):
        self.secteur = s #s = secteur auquel l'agent est rattaché
        self.id = s.nb
        self.eau = 0
        s.ajout_agent(self)  #met à jour le secteur pour ajouter un agent

class ferme(agent):
    def __init__(self, s):
        agent.__init__(self, s)
        s.nb_fermes +=1
        s.fermes.append(self)
        self.ppe = ppe_f #nb d'unités produites pour une unité d'eau 
           
    def produire(self):
        self.secteur.miam += self.eau * self.ppe
        self.eau = 0

class usine(agent):
    def __init__(self, s, prod):
        agent.__init__(self, s)
        self.prod = prod 
        self.stock = 0
        self.ppe = ppe_u
        s.nb_usines += 1
        s.usines.append(self)

    def produire(self):
        self.secteur.truc += self.eau * self.ppe
        self.eau = 0

class gens(agent):
    def __init__(self, s):
        agent.__init__(self, s)
        self.pdv = p #points de vie, représentent la santé des agents 
        self.garde_manger = 0 #quantité de nourriture disponible 
        self.tiroir = 0 #quantité de biens manufacturés disponibles 
        s.nb_gens += 1
        s.gens.append(self)
    
    def mort(self):
        #self.secteur.nb_vivants -= 1
        self.secteur.nb -= 1
        self.secteur.nb_gens -= 1
        self.secteur.gens.remove(self)
        self.secteur.agents.remove(self)
        #self.vivant = False
        self.secteur.malus += malus_mort
        if self.eau < min_eau: #si l'individu est mort de soif
            self.secteur.morts_soif += 1
        else: #si l'individu est mort de faim
            self.secteur.morts_faim += 1

    def vivre(self):
        #calcul des pdv : - si on n'a pas assez à boire ou à manger, on perd 3 pdv 
        # - sinon, on mange, boit, et gagne un pdv 
        if self.eau < min_eau or self.garde_manger < min_miam:
            self.pdv -= 3 
        else:
            self.eau -= min_eau
            self.garde_manger -= min_miam
            self.pdv += 1
        #on meurt si on a un nb de points de vie négatif en fin de journée
        if self.pdv < 0:
            self.mort()

## Définition des secteurs (une source + des agents associés)

#Rq: le secteur sera l'objet utilisé pour modifier les agents, répartir l'eau ...

class source():
    def __init__(self, D, cap, r):
        self.debit = D  #debit = debit de la source (en unité d'eau / jour) 
        self.capacite = cap #capacite de la source (en unité d'eau) 
        self.remplissage = r #r = remplissage de la source, en unité d'eau

class secteur():
    def __init__(self, s):
        self.source = s  #source associée, type source
        self.agents = [] #liste des agents associés à la source
        self.nb = 0  #nombre d'agents du secteur
        self.repartition = [] #liste des quantités d'eau allouées à chaque agent (repartition.[i] = qté d'eau pour l'agent i, en unités) 
        self.nb_gens = 0  #nb de foyers dans le secteur
        #self.nb_vivants = 0 #nombre de personnes encore vivantes (les morts restent comptés dans les gens)
        self.nb_usines = 0 #nb d'usines dans le secteur
        self.nb_fermes = 0 #nb de fermes dans le secteur
        self.gens = []  #liste des gens du secteur
        self.usines = [] #liste des usines du secteur
        self.fermes = [] #liste des fermes du secteur 
        self.miam = 0 #stock de nourriture dans le secteur
        self.truc = 0 #stock de biens manufacturés dans le secteur
        self.be = 0
        self.morts_soif = 0 #nb de morts de soif
        self.morts_faim = 0 #nb de morts de faim
        self.malus = 0
            
    def ajout_agent(self, a): #a nouvel agent à ajouter
        self.agents.append(a)
        self.nb += 1

#repartitions
    #eau

    #ci-dessous l'eau est répartie de manière égale entre tous les agents
    #la source est intégralement vidée après répartition (NB: la capacité a donc peu d'intérêt ici, puisque la source revient
    # toujours à min(C, D))
    def repartir_eau_eq(self):
        #nb_morts = self.nb_gens - self.nb_vivants
        #n = self.nb - nb_morts
        if self.nb > 0:
            q = self.source.remplissage//self.nb
            self.source.remplissage = 0
            for f in self.fermes:
                f.eau = q
            for g in self.gens:
                g.eau = q
            for u in self.usines:
                u.eau = q

    
    def repartir_eau_paps(self):
        # on donne d'abord de l'eau aux gens, à hauteur du min, puis on répartit équitablement ce qui reste (gens + fermes)
        i = 0
        while self.source.remplissage > min_eau and i < self.nb_gens:
            self.gens[i].eau += min_eau
            self.source.remplissage -= min_eau
            i += 1
        if i < self.nb_gens:
            self.gens[i].eau = self.source.remplissage
            self.source.remplissage = 0

        else: 
            self.repartir_eau_eq()
    
    def repartir_eau_priofermes(self):
        i=0
        while self.source.remplissage > min_eau and i < self.nb_fermes:
            self.fermes[i].eau += min_eau
            self.source.remplissage -= min_eau
            i +=1
        if i < self.nb_fermes:
            self.fermes[i].eau = self.source.remplissage
            self.source.remplissage = 0
        else: 
            self.repartir_eau_eq()

    #nourriture
    def repartir_agri_eq(self): #la production est suposée périssable (+ indivisible => //): tout est distribué le jour de la production
        #remarque: ici, on a une répartition équitable de la nourriture. S'il n'y a pas assez pour nourir tout le monde, 
        # tout le monde reçoit trop peu 
        gens = self.gens
        n = self.nb_gens
        if n > 0:
            q = self.miam //n
            for i in range(n):
                gens[i].garde_manger += q
                self.miam = 0

    def repartir_agri_paps(self):
        #cette fois, s'il n'y a pas assez pour nourrir tout le monde au min, on distribue le min dans l'ordre
        if self.nb_gens * min_miam > self.miam:
            i = 0
            gens = self.gens
            while self.miam > min_miam:
                gens[i].garde_manger += min_miam
                self.miam -= min_miam
                i += 1
            #on cherche le prochain vivant de la liste pour lui donner le reste de nourriture
            gens[i].garde_manger = self.miam
            self.miam = 0      
        else:
            self.repartir_agri_eq()


#production
    def produire(self):
        for f in self.fermes:
            f.produire()
        for u in self.usines:
            u.produire()

    def bienetre(self):
        for g in self.gens:
            g.vivre()
        return sum([g.pdv for g in self.gens]) - self.malus

#simulations de journée
    #1: répartition égale de l'eau et de la nourriture
    def journee_1(self):
        self.repartir_eau_eq()
        self.produire()
        self.repartir_agri_eq()
        self.source.remplissage = min(self.source.capacite, self.source.remplissage + self.source.debit)
        return self.bienetre(), self.nb_gens
        
    #2: répartition eq de l'eau et répartition de la nourriture au PAPS (premier arrivé premier servi)
    def journee_2(self):
        self.repartir_eau_eq()
        self.produire()
        self.repartir_agri_paps()
        self.source.remplissage = min(self.source.capacite, self.source.remplissage + self.source.debit)
        return self.bienetre(), self.nb_gens

    #3: répartition au paps de l'eau et de la nourriture ( avec gens prioritaires quand même sur l'eau ) 
    def journee_3(self):
        self.repartir_eau_paps()
        self.produire()
        self.repartir_agri_paps()
        self.source.remplissage = min(self.source.capacite, self.source.remplissage + self.source.debit)
        return self.bienetre(), self.nb_gens

    ##4 : on donne d'abord aux fermes avec le modèle de répartition paps
    def journee_4(self):
        self.repartir_eau_priofermes()
        self.produire()
        self.repartir_agri_paps()
        self.source.remplissage = min(self.source.capacite, self.source.remplissage + self.source.debit)
        return self.bienetre(), self.nb_gens

#tests unitaires


source_ex = source(2, 3, 4)
secteur_ex = secteur(source_ex)
assert(source_ex.debit, source_ex.capacite, source_ex.remplissage) == (2, 3, 4)
assert (secteur_ex.source, secteur_ex.agents, secteur_ex.nb, secteur_ex.repartition)  == (source_ex, [], 0, [])


assert (secteur_ex.nb_fermes, secteur_ex.nb_gens, secteur_ex.nb_usines) == (0, 0, 0)
assert (secteur_ex.fermes, secteur_ex.gens, secteur_ex.usines) == ([],[],[])

# def agents

#agents
source_ex = source(2, 3, 4)
secteur_ex = secteur(source_ex)
agent_ex = agent(secteur_ex)

assert (agent_ex.secteur, agent_ex.id) == (secteur_ex, 0)

# on vérifie que l'ajout s'est bien fait dans le secteur:
assert (secteur_ex.agents, secteur_ex.nb) == ([agent_ex], 1)

#fermes
ferme_ex = ferme(secteur_ex)
assert (ferme_ex.ppe, secteur_ex.miam) == (0.25, 0)
assert secteur_ex.nb == 2

#gens
gens_ex = gens(secteur_ex)
assert (gens_ex.pdv) == (p)

#usines
usine_ex = usine(secteur_ex, 4)
assert (usine_ex.ppe, usine_ex.prod) == (0.5, 4)
assert secteur_ex.nb == 4

assert secteur_ex.nb_fermes == 1
assert secteur_ex.fermes == [ferme_ex]
assert secteur_ex.nb_usines == 1
assert secteur_ex.usines == [usine_ex]
assert secteur_ex.nb_gens == 1
assert secteur_ex.gens == [gens_ex]

#mort d'une personne
gens_ex.mort()
assert secteur_ex.nb_gens == 0
assert gens_ex.secteur.malus == malus_mort

#répartitions de l'eau
source_ex = source(2, 3, 4)
secteur_ex = secteur(source_ex)
ferme_ex = ferme(secteur_ex)
usine_ex = usine(secteur_ex, 4)


#répartition équitable 
assert(source_ex.remplissage == 4)
secteur_ex.repartir_eau_eq()
assert (ferme_ex.eau, source_ex.remplissage) == (2, 0)

# productions 
source_ex = source(2, 3, 4)
secteur_ex = secteur(source_ex)
ferme_ex = ferme(secteur_ex)
usine_ex = usine(secteur_ex, 4) 
gens_ex = gens(secteur_ex)

secteur_ex.repartir_eau_eq()
ferme_ex.produire()

assert secteur_ex.miam == ferme_ex.ppe

# répartitions de la production agricole 

#repartition équitable
source_ex = source(2, 3, 100)
secteur_ex = secteur(source_ex)
ferme_ex = ferme(secteur_ex)
usine_ex = usine(secteur_ex, 4)
gens_ex = gens(secteur_ex)

secteur_ex.repartir_eau_eq()
ferme_ex.produire()
secteur_ex.repartir_agri_eq()

assert secteur_ex.miam == 0
assert gens_ex.garde_manger == 8

#mort 
source_ex = source(2, 3, 100)
secteur_ex = secteur(source_ex)
ferme_ex = ferme(secteur_ex)
usine_ex = usine(secteur_ex, 4)
gens_ex = gens(secteur_ex)


gens_ex.pdv = 0
gens_ex.vivre()
assert(secteur_ex.nb_gens, secteur_ex.morts_faim, secteur_ex.morts_soif) == (0, 0, 1)