import tkinter as tk
import Data_to_tap.RequestManager as RM

transformation_choix_to_topic = {
    'Hello world' : "basic",
    'Pokemon' : "pokemon",
    'Chat GPT': "gpt"
}

class Set_Data: # cette classe permet d'appeler les méthode pour récupéré ce que le robot doit taper
    @staticmethod
    def Ask_To_OpenAI(): # retourne none s'il y a une erreur sinon, il met les data dans la db
        openAIRequester = RM.OpenAIRequester(key="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")
        response = openAIRequester.make_request(prompt="Donne moi une phrase de 5 mots cohérent")

        if(response == None):
            return None
        else:
            RM.OpenAIRequester.Update_Data_To_DB("mongodb://127.0.0.1:27017/")
            # Je dois le mettre sur MongoDB
            # return response

    @staticmethod
    def Ask_To_PokeApi():
        pokeAPIRequester = RM.PokeAPIRequester()
        jsonResponse = pokeAPIRequester.make_request()

        mongoUpdater = RM.MongoDBUpdater("mongodb://127.0.0.1:27017/")

        name = jsonResponse["chain"]["species"]["name"]
        evolutions = jsonResponse["chain"]["evolves_to"]

        if len(evolutions) > 0:
            mongoUpdater.update_pokeApi(name , evolution = evolutions[0]["species"]["name"] )
        else:
            mongoUpdater.update_pokeApi(name , "nothing")

class Get_Data:
    @staticmethod
    def get_hello_world():
        return RM.MongoDbGetData.get_sentence_hello_world("mongodb://127.0.0.1:27017/")
    
    @staticmethod
    def get_poke_api():
        return RM.MongoDbGetData.get_sentence_pokemon("mongodb://127.0.0.1:27017/")
    
    @staticmethod
    def get_gpt():
        return RM.MongoDbGetData.get_sentence_GPT("mongodb://127.0.0.1:27017/")

class GUI:

    coord_label = ""

    def __init__(self):
        # Crée une instance de Tkinter
        self.root = tk.Tk()
        self.root.title("Menu")
        # Crée le panel du haut
        self.frame_haut = tk.Frame(self.root)
        self.frame_haut.pack(side=tk.TOP, pady=10)

        # Crée la liste des choix
        self.liste = tk.Listbox(self.frame_haut)
        self.liste.pack(side=tk.LEFT, padx=10)

        # Ajoute des éléments à la liste
        self.liste.insert(1, "Hello world")
        self.liste.insert(2, "Pokemon")
        self.liste.insert(3, "Chat GPT")

        # Crée le bouton pour valider le choix
        self.bouton_valider = tk.Button(self.frame_haut, text="Valider", command=self.valider)
        self.bouton_valider.pack(side=tk.LEFT, padx=10)

        # Crée le panel du bas
        self.frame_bas = tk.Frame(self.root)
        self.frame_bas.pack(side=tk.BOTTOM, pady=10)

        # Crée un Label pour afficher les coordonnées
        GUI.coord_label = tk.Label(self.frame_bas, text="Coordonnées: ")
        GUI.coord_label.pack()

        # Envoie une première coordonnée au robot KUKA
        self.nouvelle_coord = (1, 2, 3) # Exemple de coordonnée
        GUI.mettre_a_jour_coord(self.nouvelle_coord)

        # Lance la boucle principale de Tkinter
        self.root.mainloop()

    # Fonction pour mettre à jour les coordonnées dans le Label
    @staticmethod
    def mettre_a_jour_coord(coord):
        GUI.coord_label.configure(text="Coordonnées: {}".format(coord))

    # Fonction appelée lorsque le bouton est cliqué
    def valider(self):
        choix = self.liste.curselection() # Récupère l'indice de l'élément sélectionné dans la liste
        if choix:
            choix = self.liste.get(choix[0]) # Récupère la valeur de l'élément sélectionné

            topic = transformation_choix_to_topic.get(choix)

            data = ""

            if(topic == "basic"):
                data = Get_Data.get_hello_world()
            elif(topic == "pokemon"):
                Set_Data.Ask_To_PokeApi() # on demande à l'api pour changer les data des pokemons
                data = Get_Data.get_poke_api()
            elif(topic == "gpt"):
                Set_Data.Ask_To_OpenAI() # On demande à chat gpt
                data = Get_Data.get_gpt()

            print("Chose à écrire: ", data)


GUI()