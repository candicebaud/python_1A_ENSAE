## Optimisation numérique
#Optimisation sur les fermes et les gens pour D,cap,r, no_journee, nb_iterations fixés
from defs import *
import numpy as np
import matplotlib.pyplot as plt

def test(D, cap, r, nb_f, nb_g, no_journee, nb_iterations):
    res = np.zeros((nb_f,nb_g))
    resbis = 0
    for k in range (nb_f):
        for i in range (nb_g):
            resbis = test2(D, cap, r, k, i, no_journee, nb_iterations)
            res[k][i] = resbis
    return (res)


def test2(D, cap, r, nb_f, nb_g, no_journee, nb_iterations):
    source_simul = source(D, cap, r)
    secteur_simul = secteur(source_simul)
    for i in range(nb_f):
        ferme(secteur_simul)
    for i in range(nb_g):
        gens(secteur_simul)
#simulation
    be = 0
       
    if no_journee == 1:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_1()
            
    elif no_journee == 2:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_2()    
    
    elif no_journee == 3:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_3()   
       
    elif no_journee == 4:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_4()
                   
    return (be)

def recherche_fg(D, cap, r, nb_f, nb_g, no_journee, nb_iterations): #on recherche nb_f et nb_g pour un optimum de bien-être pour D, cap, r, no_journee, nb_iterations donnés
    res = test(D, cap, r, nb_f, nb_g, no_journee, nb_iterations) #renvoie matrice
    M = res.max()
    res2 = np.where(res == M )
    return (M, res2)

## Simulations

def simulation_aux(D, cap, r, nb_f, nb_g, no_journee, nb_iterations):
#initialisationdef simulation(D, cap, r, n
    source_simul = source(D, cap, r)
    secteur_simul = secteur(source_simul)
    for i in range(nb_f):
        ferme(secteur_simul)
    for i in range(nb_g):
        gens(secteur_simul)
#simulation
    be_simul = []
    nb_vivants_simul = []
    morts_soif_simul = []
    morts_faim_simul = []
    
    if no_journee == 1:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_1()
            be_simul.append(be)
            nb_vivants_simul.append(nb_v)
            morts_soif_simul.append(secteur_simul.morts_soif)
            morts_faim_simul.append(secteur_simul.morts_faim)
            
        
    elif no_journee == 2:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_2()
            be_simul.append(be)
            nb_vivants_simul.append(nb_v)
            morts_soif_simul.append(secteur_simul.morts_soif)
            morts_faim_simul.append(secteur_simul.morts_faim)
            
    
    elif no_journee == 3:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_3()
            be_simul.append(be)
            nb_vivants_simul.append(nb_v)
            morts_soif_simul.append(secteur_simul.morts_soif)
            morts_faim_simul.append(secteur_simul.morts_faim)
            
       
    elif no_journee == 4:
        for k in range(nb_iterations):
            be, nb_v = secteur_simul.journee_4()
            be_simul.append(be)
            nb_vivants_simul.append(nb_v)
            morts_soif_simul.append(secteur_simul.morts_soif)
            morts_faim_simul.append(secteur_simul.morts_faim)
            
    return (be_simul, nb_vivants_simul, morts_soif_simul, morts_faim_simul)
    

#visualisation
def visualisation(nb_iterations, be_simul, nb_vivants_simul, morts_soif_simul, morts_faim_simul):
    abscisse = [i for i in range (nb_iterations)]
    plt.plot(abscisse, be_simul, label=simulation)
    plt.title('points de bien-être en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('points de vie')
    plt.legend()

    plt.plot(abscisse, nb_vivants_simul, label=simulation)
    plt.title('population en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('nombre de vivants')
    plt.legend()

    plt.plot(abscisse, morts_soif_simul, label=simulation)
    plt.title('morts de soif')
    plt.xlabel('temps')
    plt.ylabel('nombre de morts de soif')
    plt.legend()


    plt.plot(abscisse, morts_faim_simul, label=simulation)
    plt.title('morts de faim')
    plt.xlabel('temps')
    plt.ylabel('nombre de morts de faim')
    plt.legend()
    plt.show()
    plt.close()

def simulation(D, cap, r, nb_f, nb_g, no_journee, nb_iterations):
    be_simul, nb_vivants_simul, morts_soif_simul, morts_faim_simul = (simulation_aux(D, cap, r, nb_f, nb_g, no_journee, nb_iterations))
    visualisation(nb_iterations, be_simul, nb_vivants_simul, morts_soif_simul, morts_faim_simul)

def visualisation_double(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2, simulation1, simulation2):
    abscisse = [i for i in range (nb_iterations)]
    plt.plot(abscisse, be_simul1, label=simulation1, c='b')
    plt.plot(abscisse, be_simul2, label=simulation2, c='r')
    plt.title('points de bien-être en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('bien-être')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, nb_vivants_simul1, label=simulation1,c='b')
    plt.plot(abscisse, nb_vivants_simul2, label=simulation2, c='r')
    plt.title('nombre de vivants en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('nb de vivants')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_soif_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_soif_simul2, label=simulation2, c='r')
    plt.title('nombre de morts dues à la soif')
    plt.xlabel('temps')
    plt.ylabel('morts de soif')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_faim_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_faim_simul2, label=simulation2,c='r')
    plt.title('nombre de morts de faim')
    plt.xlabel('temps')
    plt.ylabel('morts de faim')
    plt.legend()
    plt.show()
    plt.close()

def visualisation_triple(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3, simulation1, simulation2, simulation3):
    abscisse = [i for i in range (nb_iterations)]
    plt.plot(abscisse, be_simul1, label=simulation1,c='b')
    plt.plot(abscisse, be_simul2, label=simulation2, c='r')
    plt.plot(abscisse, be_simul3, label=simulation3, c='g')
    plt.title('points de bien-être en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('bien-être')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, nb_vivants_simul1, label=simulation1, c='b')
    plt.plot(abscisse, nb_vivants_simul2, label=simulation2, c='r')
    plt.plot(abscisse, nb_vivants_simul3, label=simulation3, c='g')
    plt.title('nombre de vivants en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('nb de vivants')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_soif_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_soif_simul2, label=simulation2, c='r')
    plt.plot(abscisse, morts_soif_simul3, label=simulation3, c='g')
    plt.title('nombre de morts dues à la soif')
    plt.xlabel('temps')
    plt.ylabel('morts de soif')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_faim_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_faim_simul2, label=simulation2, c='r')
    plt.plot(abscisse, morts_faim_simul3, label=simulation3, c='g')
    plt.title('nombre de morts de faim')
    plt.xlabel('temps')
    plt.ylabel('morts de faim')
    plt.legend()
    plt.show()
    plt.close

def visualisation_quadruple(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3,be_simul4, nb_vivants_simul4, morts_soif_simul4, morts_faim_simul4, simulation1, simulation2, simulation3, simulation4):
    abscisse = [i for i in range (nb_iterations)]
    plt.plot(abscisse, be_simul1, label=simulation1,c='b')
    plt.plot(abscisse, be_simul2, label=simulation2, c='r')
    plt.plot(abscisse, be_simul3, label=simulation3, c='g')
    plt.plot(abscisse, be_simul4, label=simulation4, c='k')
    plt.title('points de bien-être en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('bien-être')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, nb_vivants_simul1, label=simulation1, c='b')
    plt.plot(abscisse, nb_vivants_simul2, label=simulation2, c='r')
    plt.plot(abscisse, nb_vivants_simul3, label=simulation3, c='g')
    plt.plot(abscisse, nb_vivants_simul4, label=simulation4, c='k')
    plt.title('nombre de vivants en fonction du temps')
    plt.xlabel('temps')
    plt.ylabel('nb de vivants')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_soif_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_soif_simul2, label=simulation2, c='r')
    plt.plot(abscisse, morts_soif_simul3, label=simulation3, c='g')
    plt.plot(abscisse, morts_soif_simul4, label=simulation4, c='k')
    plt.title('nombre de morts dues à la soif')
    plt.xlabel('temps')
    plt.ylabel('morts de soif')
    plt.legend()
    plt.show()
    plt.close()

    plt.plot(abscisse, morts_faim_simul1, label=simulation1, c='b')
    plt.plot(abscisse, morts_faim_simul2, label=simulation2, c='r')
    plt.plot(abscisse, morts_faim_simul3, label=simulation3, c='g')
    plt.plot(abscisse, morts_faim_simul4, label=simulation4, c='k')
    plt.title('nombre de morts de faim')
    plt.xlabel('temps')
    plt.ylabel('morts de faim')
    plt.legend()
    plt.show()
    plt.close()

def simulation_double(D1, D2, cap1, cap2, r1, r2, nb_f1, nb_f2, nb_g1, nb_g2, no_journee1, no_journee2, nb_iterations, simulation1, simulation2):
    be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1 = simulation_aux(D1, cap1, r1, nb_f1, nb_g1, no_journee1, nb_iterations)
    be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2 = simulation_aux(D2, cap2, r2, nb_f2, nb_g2, no_journee2, nb_iterations)
    visualisation_double(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,simulation1, simulation2)

def simulation_triple(D1, D2, D3, cap1, cap2, cap3, r1, r2, r3, nb_f1, nb_f2, nb_f3, nb_g1, nb_g2, nb_g3, no_journee1, no_journee2, no_journee3, nb_iterations, simulation1, simulation2, simulation3):
    be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1 = simulation_aux(D1, cap1, r1, nb_f1, nb_g1, no_journee1, nb_iterations)
    be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2 = simulation_aux(D2, cap2, r2, nb_f2, nb_g2, no_journee2, nb_iterations)
    be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3 = simulation_aux(D3, cap3, r3, nb_f3, nb_g3, no_journee3, nb_iterations)
    visualisation_triple(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3, simulation1, simulation2, simulation3)

def simulation_double(D1, D2, cap1, cap2, r1, r2, nb_f1, nb_f2, nb_g1, nb_g2, no_journee1, no_journee2, nb_iterations, simulation1, simulation2):
    be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1 = simulation_aux(D1, cap1, r1, nb_f1, nb_g1, no_journee1, nb_iterations)
    be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2 = simulation_aux(D2, cap2, r2, nb_f2, nb_g2, no_journee2, nb_iterations)
    visualisation_double(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,simulation1, simulation2)

def simulation_quadruple(D1, D2, D3, D4, cap1, cap2, cap3, cap4, r1, r2, r3, r4, nb_f1, nb_f2, nb_f3, nb_f4, nb_g1, nb_g2, nb_g3, nb_g4, no_journee1, no_journee2, no_journee3, no_journee4, nb_iterations, simulation1, simulation2, simulation3, simulation4):
    be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1 = simulation_aux(D1, cap1, r1, nb_f1, nb_g1, no_journee1, nb_iterations)
    be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2 = simulation_aux(D2, cap2, r2, nb_f2, nb_g2, no_journee2, nb_iterations)
    be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3 = simulation_aux(D3, cap3, r3, nb_f3, nb_g3, no_journee3, nb_iterations)
    be_simul4, nb_vivants_simul4, morts_soif_simul4, morts_faim_simul4 = simulation_aux(D4, cap4, r4, nb_f4, nb_g4, no_journee4, nb_iterations)
    visualisation_quadruple(nb_iterations, be_simul1, nb_vivants_simul1, morts_soif_simul1, morts_faim_simul1, be_simul2, nb_vivants_simul2, morts_soif_simul2, morts_faim_simul2,be_simul3, nb_vivants_simul3, morts_soif_simul3, morts_faim_simul3,be_simul4, nb_vivants_simul4, morts_soif_simul4, morts_faim_simul4, simulation1, simulation2, simulation3, simulation4)

## Optimisation numérique
#Optimisation sur les fermes et les gens pour D,cap,r, no_journee, nb_iterations fixés
def recherche_fg(D, cap, r, nb_f, nb_g, no_journee, nb_iterations): #on recherche nb_f et nb_g pour un optimum de bien-être pour D, cap, r, no_journee, nb_iterations donnés
    res = test(D, cap, r, nb_f, nb_g, no_journee, nb_iterations) #renvoie matrice
    M = res.max()
    res2 = np.where(res == M )
    return (M, res2)

#Optimisation sur les fermes, les gens et les types de méthodes à D,cap,r, nb_iterations fixés. 

def afficher(D, cap, r, nb_f, nb_g, no_journee, nb_iterations, simulation):
    res = test(D, cap, r, nb_f, nb_g, no_journee, nb_iterations)
    abscisse = [i for i in range (nb_g)]
    abscisse2 = [k for k in range (nb_f)]
    X, Y = np.meshgrid(abscisse, abscisse2)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, res, rstride=1, cstride=1, cmap='jet', edgecolor='none', label=simulation)
    plt.title(simulation)
    ax.set_xlabel("Nombre de gens")
    ax.set_ylabel("Nombre de fermes")
    ax.set_zlabel("Bien-être")
    plt.savefig('image.png')
    plt.tight_layout()
    plt.show()
    plt.close()

