import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import os
import time
from datetime import datetime

class GRPCClient:
    def __init__(self):
        self.host = "localhost"
        self.port = "50051"
        self.stub = None
        self.connected = False
        
    def display_header(self, title=""):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("🌟 CLIENT gRPC HELLOWORLD 🌟")
        print("=" * 60)
        if title:
            print(f"📋 {title}")
            print("-" * 60)
        print(f"📡 Serveur: {self.host}:{self.port}")
        print(f"🔗 Statut: {'✅ Connecté' if self.connected else '❌ Déconnecté'}")
        print("=" * 60)
        
    def connect_to_server(self):
        try:
            channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            self.stub = helloworld_pb2_grpc.GreeterStub(channel)
            
            # Test de connexion
            test_request = helloworld_pb2.HelloRequest(name="test", language="en")
            self.stub.SayHello(test_request, timeout=5)
            self.connected = True
            return True
            
        except Exception as e:
            print(f"❌ Erreur de connexion: {str(e)}")
            return False
    
    def choose_language_menu(self):
        """Menu principal pour choisir la langue"""
        while True:
            self.display_header("CHOISIR UNE LANGUE")
            
            print("🌍 SELECTION DE LA LANGUE:")
            print("1. 🇫🇷  Français")
            print("2. 🇬🇧  English") 
            print("3. 🇹🇳  Arabe (Tunisie)")
            print("4. 🔧  Changer le serveur")
            print("5. 🚪  Quitter")
            print("-" * 40)
            
            choice = input("\nVotre choix [1-5]: ")
            
            if choice in ["1", "2", "3"]:
                language_map = {"1": "fr", "2": "en", "3": "ar"}
                language = language_map[choice]
                self.language_actions_menu(language)
            elif choice == "4":
                self.change_server()
            elif choice == "5":
                print("\n👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide, veuillez réessayer.")
                time.sleep(1)
    
    def language_actions_menu(self, language):
        """Menu des actions pour une langue spécifique"""
        language_names = {
            "fr": "Français",
            "en": "English", 
            "ar": "Arabe (Tunisie)"
        }
        
        language_icons = {
            "fr": "🇫🇷",
            "en": "🇬🇧",
            "ar": "🇹🇳"
        }
        
        lang_name = language_names[language]
        icon = language_icons[language]
        
        while True:
            self.display_header(f"{icon} LANGUE: {lang_name}")
            
            print(f"📝 Actions disponibles en {lang_name}:")
            print("1. 👋  Salutation simple")
            print("2. 🔄  Streaming de salutations")
            print("3. 🔙  Changer de langue")
            print("4. 🚪  Quitter")
            print("-" * 40)
            
            choice = input("\nVotre choix [1-4]: ")
            
            if choice == "1":
                self.simple_greeting(language, lang_name, icon)
            elif choice == "2":
                self.streaming_greeting(language, lang_name, icon)
            elif choice == "3":
                break  # Retour au menu langue
            elif choice == "4":
                print("\n👋 Au revoir !")
                exit()
            else:
                print("❌ Choix invalide")
                time.sleep(1)
    
    def simple_greeting(self, language, lang_name, icon):
        """Salutation simple dans une langue"""
        self.display_header(f"{icon} SALUTATION SIMPLE - {lang_name}")
        
        name = input("Entrez votre nom: ")
        if not name:
            print("❌ Le nom est obligatoire")
            input("\nAppuyez sur Entrée pour continuer...")
            return
            
        try:
            start_time = time.time()
            request = helloworld_pb2.HelloRequest(name=name, language=language)
            response = self.stub.SayHello(request)
            response_time = (time.time() - start_time) * 1000
            
            print(f"\n🎯 RÉSULTAT:")
            print(f"   {icon} {response.message}")
            print(f"   🌐 Langue: {lang_name}")
            print(f"   ⚡ Temps de réponse: {response_time:.2f} ms")
            print(f"   🕐 Heure: {datetime.now().strftime('%H:%M:%S')}")
            
        except grpc.RpcError as e:
            print(f"❌ Erreur gRPC: {e.details()}")
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            
        input("\n↵ Appuyez sur Entrée pour continuer...")
    
    def streaming_greeting(self, language, lang_name, icon):
        """Streaming de salutations dans une langue"""
        self.display_header(f"{icon} STREAMING - {lang_name}")
        
        name = input("Entrez votre nom: ")
        if not name:
            print("❌ Le nom est obligatoire")
            input("\nAppuyez sur Entrée pour continuer...")
            return
            
        print(f"\n🔄 Démarrage du streaming en {lang_name}...")
        print(f"📨 Vous allez recevoir plusieurs salutations différentes")
        print("=" * 50)
        
        try:
            request = helloworld_pb2.HelloRequest(name=name, language=language)
            message_count = 0
            start_time = time.time()
            
            for response in self.stub.StreamHello(request):
                message_count += 1
                print(f"{icon} Message {message_count}:")
                print(f"   💬 {response.message}")
                print(f"   🕐 {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 40)
                
            total_time = time.time() - start_time
            print(f"✅ STREAMING TERMINÉ")
            print(f"📊 {message_count} messages reçus en {total_time:.2f} secondes")
            
        except grpc.RpcError as e:
            print(f"❌ Erreur gRPC: {e.details()}")
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            
        input("\n↵ Appuyez sur Entrée pour continuer...")
    
    def change_server(self):
        """Changer la configuration du serveur"""
        self.display_header("CONFIGURATION SERVEUR")
        
        print("🔧 Paramètres de connexion:")
        new_host = input("Adresse du serveur [localhost]: ") or "localhost"
        new_port = input("Port [50051]: ") or "50051"
        
        old_target = f"{self.host}:{self.port}"
        self.host = new_host
        self.port = new_port
        self.connected = False
        
        print(f"\n🔄 Tentative de connexion à {self.host}:{self.port}...")
        if self.connect_to_server():
            print("✅ Connexion établie avec succès!")
        else:
            print("❌ Échec de la connexion")
            print("Retour aux paramètres précédents...")
            # Restaurer les anciens paramètres
            parts = old_target.split(":")
            self.host = parts[0]
            self.port = parts[1] if len(parts) > 1 else "50051"
            
        input("\n↵ Appuyez sur Entrée pour continuer...")
    
    def start(self):
        """Démarrer le client"""
        print("🔄 Connexion au serveur...")
        if self.connect_to_server():
            print("✅ Connecté avec succès!")
            time.sleep(1)
            self.choose_language_menu()
        else:
            print("❌ Impossible de se connecter au serveur par défaut")
            self.change_server()
            if self.connected:
                self.choose_language_menu()

def main():
    client = GRPCClient()
    client.start()

if __name__ == "__main__":
    main()