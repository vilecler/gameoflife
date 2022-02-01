import numpy as np
import time
import tkinter as tk
import random as rd

#Enlevez les '#' devant les print pour le # DEBUG:

#'Arreter' ne fait que mettre le jeu sur pause
#'Initialiser' crée un nouveau jeu
#'Lancer' ne fonctionne que si le jeu a ete initialisé une première fois

class MaFenetre(tk.Tk):
    """Class MaFenetre héritant de Tk, librarie pour créer des interfaces graphiques en Python."""

    def __init__(self):
        """Constructeur de la class MaFenetre. Initialisez size pour changer la taille de la fenêtre."""
        tk.Tk.__init__(self)
        self.size = 600
        self.speed = 5  #Valeur par défaut sur la capture d'écran donnée en sujet
        self.percents_life = 20 #Valeur par défaut sur la capture d'écran donnée en sujet
        self.grid_size = 30 #Valeur par défaut sur la capture d'écran donnée en sujet
        self.creer_widget() #Création de l'interface graphique
        self.initialized = False #Valeur par défaut, le programme n'est pas encore initialisé
        self.running = False #Valeur par défaut, le programme ne fonctionne pas

    def creer_widget(self):
        """Méthode creer_widget, permet de mettre en place d'interface graphique"""
        #La grille
        self.canvas = tk.Canvas(self, height=self.size, width=self.size, bg='white')
        self.canvas.pack(side = tk.LEFT)

        #Les boutons
        #Bouton "Lancer"
        self.bouton_lancer = tk.Button(self, text="Lancer", width=20, command=self.lancer, fg="blue")
        self.bouton_lancer.pack(side = tk.TOP)

        #Bouton "Arreter"
        self.bouton_arreter = tk.Button(self, text="Arreter", width=20, command=self.arreter, fg="blue")
        self.bouton_arreter.pack()

        #Bouton "Initialiser"
        self.bouton_initialiser = tk.Button(self, text="Initialiser", width=20, command=self.initialiser, fg="blue")
        self.bouton_initialiser.pack()

        #Bouton "Quitter"
        self.bouton_quitter = tk.Button(self, text="Quitter", width=20, command=self.quitter, fg="blue")
        self.bouton_quitter.pack(side = tk.BOTTOM)

        #Les scales
        #Scale vitesse
        self.scale_speed = tk.Scale(self, orient='horizontal', from_=1, to=60, width=20, label='Vitesse', command=self.onSpeedChanged, fg="blue")
        self.scale_speed.set(self.speed)
        self.scale_speed.pack(side = tk.BOTTOM)

        #Scale pourcentage de vie
        self.scale_percents_life = tk.Scale(self, orient='horizontal', from_=1, to=100, width=20, label='% de Vie', command=self.onPercentsLifeChanged, fg="blue")
        self.scale_percents_life.set(self.percents_life)
        self.scale_percents_life.pack(side = tk.BOTTOM)

        #Scale taille de la grille
        self.scale_grid_size = tk.Scale(self, orient='horizontal', from_=1, to=100, width=20, label='Taille de la grille', command=self.onGridSizeChanged, fg="blue")
        self.scale_grid_size.set(self.grid_size)
        self.scale_grid_size.pack(side = tk.BOTTOM)


    def lancer(self):
        """Méthode lancer, appelée lorsque l'on clique sur le bouton 'Lancer'. Execute le jeu de la vie en boucle."""
        #print("Onclick lancer")
        self.running = True #Le programme est en cours d'execution
        while self.running == True and self.initialized == True: #permet de s'arreter si l'etat de running n'est plus vrai et ne déclenche pas la boucle si le jeu n'a pas été initialisé
            for i in range(0, self.grid_size):
                for j in range(0, self.grid_size):
                    #On est à A[i, j]
                    count = 0   #compteur sur le nombre de cases voisines

                    i_moins_un = i-1
                    j_moins_un = j-1

                    i_plus_un = i+1
                    j_plus_un = j+1

                    if i_moins_un < 0:
                        i_moins_un = self.grid_size - 1
                    if j_moins_un < 0:
                        j_moins_un = self.grid_size - 1

                    if i_plus_un > (self.grid_size - 1):
                        i_plus_un = 0
                    if j_plus_un > (self.grid_size - 1):
                        j_plus_un = 0

                    if(self.A[i_moins_un,j_moins_un] == 1):
                        count = count +1
                    if(self.A[i_moins_un,j] == 1):
                        count = count +1
                    if(self.A[i_moins_un,j_plus_un] == 1):
                        count = count +1
                    if(self.A[i,j_moins_un] == 1):
                        count = count +1
                    if(self.A[i,j_plus_un] == 1):
                        count = count +1
                    if(self.A[i_plus_un,j_moins_un] == 1):
                        count = count +1
                    if(self.A[i_plus_un,j] == 1):
                        count = count +1
                    if(self.A[i_plus_un,j_plus_un] == 1):
                        count = count +1

                    #On crée une copie de A (nommée B) qu'on mettra à jour à la fin pour stocker les résultats et ne pas affecter A
                    if self.A[i, j] == 0:
                        if count == 3:
                            self.B[i, j] = 1
                        else:
                            self.B[i, j] = 0
                    else:
                        if count == 3 or count == 2:
                            self.B[i, j] = 1
                        else:
                            self.B[i, j] = 0


            time.sleep((60-self.speed)*2/60) #speed = 1 -> sleep 2s, speed = 60 -> sleep 0s
            #print("Fin d'un cycle")
            self.A = self.B
            self.show_matrice()
            self.update_idletasks() #mise à jour de l'interface
            self.update()
        #print("Fin de lancer")

    def arreter(self):
        """Méthode arreter, appelée lorsque l'on clique sur le bouton 'Arreter', change l'état de la variable running à False (et interromp donc la boucle de lancer)"""
        #print("Onclick arreter")
        self.running = False

    def initialiser(self):
        """Méthode initialiser, appelée lorsque l'on clique sur le bouton 'Initialiser', change l'état de la variable initialized à True (et permet d'executer la boucle de lancer)"""
        #print("Onclick initialiser")
        if self.running == False:   #on ne réinitialise pas si on est en train de jouer
            self.create_grid()  #on refait une grille
            self.init_matrice() #on réinitialise la matrice A aléatoirement
            self.show_matrice() #on affiche la matrice A
            self.initialized = True

    def create_grid(self):
        """Méthode create_grid, permet de créer la grille pour accueillir la matrice"""
        #initialisation du canvas
        w = self.canvas.winfo_width() #w = largeur de canvas
        h = self.canvas.winfo_height() #h = hauteur de canvas
        self.canvas.delete('grid_line') #On supprime l'ancienne grille

        self.taille = w//self.grid_size #taille d'une cellule

        for i in range(0, w, self.taille):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line')

        for i in range(0, h, self.taille):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')

    def init_matrice(self):
        """Méthode init_matrice, permet d'initialiser la matrice A aléatoirement et d'en créer un copie B."""
        self.A = np.random.choice([0, 1], size=(self.grid_size, self.grid_size), p=[float(1 - self.percents_life/100), float(self.percents_life/100)])
        self.B = self.A

    def create_cell(self, i, j, alive):
        """Méthode create_cell, permet d'afficher une cellule sur la grille selon qu'elle soit vivante ou morte"""
        if alive == 1:
            self.canvas.create_rectangle(i*self.taille, j*self.taille, (i+1)*self.taille, (j+1)*self.taille, fill='red', tag='cel')
        else:
            self.canvas.create_rectangle(i*self.taille, j*self.taille, (i+1)*self.taille, (j+1)*self.taille, fill='white', tag='cel')

    def show_matrice(self):
        """Méthode show_matrice, permet d'afficher la matrice sur la grille"""
        self.canvas.delete('cel') #On supprime les anciennes cellules
        for i in range(0, self.grid_size):
            for j in range(0, self.grid_size):
                self.create_cell(i=i, j=j, alive=self.A[i, j])

    def quitter(self):
        """Méthode quitter, appelée lorque l'on clique sur le bouton 'Quitter', change la variable running à False et ferme la fenêtre"""
        #print("Onclick quitter")
        self.running = False
        self.quit()

    def onSpeedChanged(self, new_value):
        """Méthode onSpeedChanged appelée lorque le curseur sur la vitesse change"""
        #print("OnSpeedChanged", new_value)
        if self.running == False: #n'a d'effet que si on exécute pas la fonction lancer pour ne pas modifier le jeu en cours
            self.speed = int(new_value)

    def onPercentsLifeChanged(self, new_value):
        """Méthode onPercentsLifeChanged appelée lorque le curseur sur le pourcentage de cellules en vie à t=0 change"""
        #print("OnPercentsLifeChanged", new_value)
        if self.running == False: #n'a d'effet que si on exécute pas la fonction lancer pour ne pas modifier le jeu en cours
            self.percents_life = int(new_value)

    def onGridSizeChanged(self, new_value):
        """Méthode onGridSizeChanged appelée lorque le curseur sur la taille de la grille change"""
        #print("OnGridSizeChanged", new_value)
        if self.running == False: #n'a d'effet que si on exécute pas la fonction lancer pour ne pas modifier le jeu en cours
            self.grid_size = int(new_value)

#ici notre programme main
if __name__ == "__main__":
    app = MaFenetre()
    app.title("SR01 Jeu de la vie")
    app.mainloop()
