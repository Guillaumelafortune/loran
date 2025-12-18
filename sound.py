import pygame
import threading
import time
import os
import tkinter as tk
from PIL import Image, ImageTk
import random

class ImageDisplayer:
    def __init__(self):
        self.root = None
        self.windows = []
        self.running = False
    
    def show_images_on_screen(self, image_path, num_images=5, duration=10):
        """
        Affiche plusieurs copies d'une image à des positions aléatoires sur l'écran
        
        Args:
            image_path (str): Chemin vers le fichier image
            num_images (int): Nombre d'images à afficher
            duration (float): Durée d'affichage en secondes
        """
        
        # Vérifier que le fichier image existe
        if not os.path.exists(image_path):
            print(f"Erreur: Le fichier image {image_path} n'existe pas!")
            return False
        
        try:
            # Créer la fenêtre principale
            self.root = tk.Tk()
            self.root.withdraw()  # Cacher la fenêtre principale
            
            # Charger l'image avec PIL
            pil_image = Image.open(image_path)
            
            # Redimensionner l'image pour qu'elle soit plus petite avec 100 images
            max_size = (150, 200)  # Taille plus petite pour 100 images
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Obtenir les dimensions de l'écran
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Créer plusieurs fenêtres avec l'image
            for i in range(num_images):
                # Créer une nouvelle fenêtre
                window = tk.Toplevel(self.root)
                window.title(f"Image {i+1}")
                
                # Supprimer les bordures de la fenêtre
                window.overrideredirect(True)
                
                # Convertir l'image pour tkinter
                tk_image = ImageTk.PhotoImage(pil_image)
                
                # Créer un label avec l'image
                label = tk.Label(window, image=tk_image)
                label.image = tk_image  # Garder une référence
                label.pack()
                
                # Position aléatoire sur l'écran
                x = random.randint(0, max(0, screen_width - pil_image.width))
                y = random.randint(0, max(0, screen_height - pil_image.height))
                window.geometry(f"+{x}+{y}")
                
                # Rendre la fenêtre toujours au premier plan
                window.attributes('-topmost', True)
                
                self.windows.append(window)
                print(f"Image {i+1} affichée à la position ({x}, {y})")
            
            # Programmer la fermeture automatique
            self.root.after(int(duration * 1000), self.close_images)
            
            self.running = True
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'affichage des images: {e}")
            return False
    
    def start_display(self):
        """Démarre la boucle d'affichage tkinter"""
        if self.root and self.running:
            self.root.mainloop()
    
    def close_images(self):
        """Ferme toutes les fenêtres d'images"""
        self.running = False
        for window in self.windows:
            try:
                window.destroy()
            except:
                pass
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass


def play_mp3_with_delay(file_path, delay_seconds=0.01, repetitions=5):
    """
    Lance un fichier MP3 plusieurs fois avec un décalage entre chaque lecture
    
    Args:
        file_path (str): Chemin vers le fichier MP3
        delay_seconds (float): Délai en secondes entre chaque lecture (défaut: 0.01)
        repetitions (int): Nombre de répétitions (défaut: 5)
    """
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path):
        print(f"Erreur: Le fichier {file_path} n'existe pas!")
        return
    
    # Initialiser pygame mixer avec plus de canaux pour permettre la lecture simultanée
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)  # Permettre beaucoup plus de sons simultanés pour l'amplification
    
    # Charger le son une seule fois
    try:
        sound = pygame.mixer.Sound(file_path)
        # Volume maximum (pygame limite à 1.0)
        sound.set_volume(1.0)
        print(f"Fichier audio chargé: {file_path} (volume: MAXIMUM)")
    except pygame.error as e:
        print(f"Erreur lors du chargement du fichier: {e}")
        return
    
    print(f"Lancement de {repetitions} lectures avec un décalage de {delay_seconds}s")
    
    # Liste pour stocker les objets de lecture
    playing_sounds = []
    
    # AMPLIFICATION EXTRÊME : Jouer plusieurs copies simultanées pour créer de la distorsion
    amplification_factor = 5  # Jouer 3 copies de chaque son pour amplifier
    
    # Lancer chaque lecture avec le décalage spécifié
    for i in range(repetitions):
        print(f"Démarrage de la lecture {i+1}/{repetitions} (avec amplification x{amplification_factor})")
        
        # Jouer plusieurs copies du même son simultanément pour amplifier
        for amp in range(amplification_factor):
            channel = sound.play()
            if channel:
                playing_sounds.append(channel)
            else:
                print(f"Impossible de jouer la copie {amp+1} du son {i+1}")
        
        # Attendre le délai avant la prochaine lecture (sauf pour la dernière)
        if i < repetitions - 1:
            time.sleep(delay_seconds)
    
    # Attendre que tous les sons se terminent VRAIMENT
    print("Attente de la fin de toutes les lectures...")
    
    # Première vérification : attendre que tous les canaux se libèrent
    while any(channel and channel.get_busy() for channel in playing_sounds):
        time.sleep(0.1)
    
    # Deuxième vérification : attendre que pygame mixer soit vraiment libre
    while pygame.mixer.get_busy():
        time.sleep(0.1)
    
    # Attendre encore un peu pour être sûr que tout est terminé
    print("Attente supplémentaire pour s'assurer que tout est terminé...")
    time.sleep(2)  # 2 secondes de sécurité
    
    print("Toutes les lectures sont terminées!")
    pygame.mixer.quit()

def run_infinite_chaos():
    """Lance les images et le son en boucle infinie - JAMAIS D'ARRÊT !"""
    # Noms des fichiers dans le même répertoire
    mp3_file = "Screen Recording 2025-12-17 165910.mp3"
    image_file = "1cd6f970-57cc-4943-9ad2-91fed3b4d214.jpg"
    
    print("=== DÉMARRAGE DU CHAOS INFINI ===")
    print("⚠️  ATTENTION: Ce script ne s'arrêtera JAMAIS !")
    print("⚠️  Pour l'arrêter, fermez le terminal ou appuyez sur Ctrl+C")
    
    cycle_count = 0
    
    # BOUCLE INFINIE
    while True:
        cycle_count += 1
        print(f"\n🔥 === CYCLE {cycle_count} - CHAOS ÉTERNEL === 🔥")
        
        try:
            # Créer un nouvel afficheur d'images pour chaque cycle
            displayer = ImageDisplayer()
            
            # Durée courte pour chaque cycle (pour relancer rapidement)
            cycle_duration = 8  # secondes par cycle
            
            # Configurer l'affichage des images
            print(f"Préparation de l'affichage des 200 images (cycle {cycle_count})...")
            if displayer.show_images_on_screen(image_file, num_images=200, duration=cycle_duration):
                
                # Lancer le son dans un thread séparé
                def play_sound_cycle():
                    time.sleep(0.2)  # Pause plus courte
                    print(f"🔊 Lancement du son amplifié (cycle {cycle_count})...")
                    play_mp3_with_delay(mp3_file, delay_seconds=0.01, repetitions=5)
                    print(f"✅ Son terminé pour le cycle {cycle_count}")
                
                sound_thread = threading.Thread(target=play_sound_cycle)
                sound_thread.daemon = True  # Daemon pour pouvoir passer au cycle suivant
                sound_thread.start()
                
                # Démarrer la boucle d'affichage pour ce cycle
                print(f"🖼️  Affichage de 200 images en cours (cycle {cycle_count})...")
                displayer.start_display()
                
            else:
                print("Impossible d'afficher les images, lancement du son seulement...")
                play_mp3_with_delay(mp3_file, delay_seconds=0.01, repetitions=5)
            
            # Petite pause entre les cycles pour éviter la surcharge
            print(f"⏳ Pause de 1 seconde avant le cycle {cycle_count + 1}...")
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🛑 ARRÊT FORCÉ PAR L'UTILISATEUR (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ Erreur dans le cycle {cycle_count}: {e}")
            print("🔄 Redémarrage automatique dans 2 secondes...")
            time.sleep(2)
            continue
    
    print("=== CHAOS TERMINÉ ===")

if __name__ == "__main__":
    run_infinite_chaos()
