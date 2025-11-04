package com.example.grpc;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.Random;

public class HelloWorldServer {
    private Server server;
    private Random random = new Random();
    
    static class GreeterServiceImpl extends GreeterGrpc.GreeterImplBase {
        
        private Random random = new Random();
        
        // Retourne différentes façons de saluer selon la langue
        private String[] getFrenchGreetings(String name) {
            return new String[] {
                "Bonjour " + name + "! Comment allez-vous?",
                "Salut " + name + "! Ravie de vous voir!",
                "Bien le bonjour " + name + "! Belle journée n'est-ce pas?",
                "Coucou " + name + "! Tout va bien?",
                "Hey " + name + "! Content de te revoir!"
            };
        }
        
        private String[] getEnglishGreetings(String name) {
            return new String[] {
                "Hello " + name + "! How are you doing?",
                "Hi " + name + "! Great to see you!",
                "Hey " + name + "! What's up?",
                "Good day " + name + "! Lovely weather today!",
                "Welcome " + name + "! Nice to meet you!"
            };
        }
        
        private String[] getArabicGreetings(String name) {
            return new String[] {
                "مرحبا " + name + "! كيف حالك؟",
                "أهلا " + name + "! سعيد برؤيتك!",
                "سلام " + name + "! ما الأخبار؟",
                "تحية " + name + "! يوم جميل اليوم!",
                "أهلا وسهلا " + name + "! تشرفنا!"
            };
        }
        
        @Override
        public void sayHello(HelloRequest req, StreamObserver<HelloReply> responseObserver) {
            System.out.println("Requête reçue - Nom: " + req.getName() + ", Langue: " + req.getLanguage());
            
            String greeting = getSingleGreeting(req.getName(), req.getLanguage());
            HelloReply reply = HelloReply.newBuilder()
                .setMessage(greeting)
                .setLanguage(req.getLanguage())
                .build();
                
            responseObserver.onNext(reply);
            responseObserver.onCompleted();
        }
        
        private String getSingleGreeting(String name, String language) {
            String[][] allGreetings;
            switch (language.toLowerCase()) {
                case "fr":
                    allGreetings = new String[][]{getFrenchGreetings(name)};
                    break;
                case "ar":
                    allGreetings = new String[][]{getArabicGreetings(name)};
                    break;
                case "en":
                default:
                    allGreetings = new String[][]{getEnglishGreetings(name)};
            }
            String[] greetings = allGreetings[0];
            return greetings[random.nextInt(greetings.length)];
        }
        
        @Override
        public void streamHello(HelloRequest req, StreamObserver<HelloReply> responseObserver) {
            System.out.println("Streaming demandé pour: " + req.getName() + ", Langue: " + req.getLanguage());
            
            String language = req.getLanguage().toLowerCase();
            String[][] allGreetings;
            
            // Si aucune langue spécifiée, envoyer toutes les langues
            if (language.isEmpty()) {
                allGreetings = new String[][]{
                    getFrenchGreetings(req.getName()),
                    getEnglishGreetings(req.getName()), 
                    getArabicGreetings(req.getName())
                };
            } else {
                // Sinon, envoyer seulement la langue demandée
                switch (language) {
                    case "fr":
                        allGreetings = new String[][]{getFrenchGreetings(req.getName())};
                        break;
                    case "ar":
                        allGreetings = new String[][]{getArabicGreetings(req.getName())};
                        break;
                    case "en":
                    default:
                        allGreetings = new String[][]{getEnglishGreetings(req.getName())};
                }
            }
            
            // Envoyer 5 salutations différentes
            for (String[] greetings : allGreetings) {
                for (int i = 0; i < 5; i++) {
                    String greeting = greetings[i];
                    HelloReply reply = HelloReply.newBuilder()
                        .setMessage(greeting)
                        .setLanguage(language.isEmpty() ? 
                            (greetings == getFrenchGreetings(req.getName()) ? "fr" :
                             greetings == getArabicGreetings(req.getName()) ? "ar" : "en")
                            : language)
                        .build();
                        
                    responseObserver.onNext(reply);
                    
                    try {
                        Thread.sleep(1500); // Pause de 1.5 secondes
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
            
            responseObserver.onCompleted();
            System.out.println("Streaming terminé");
        }
    }
    
    public void start(int port) throws IOException {
        server = ServerBuilder.forPort(port)
            .addService(new GreeterServiceImpl())
            .build()
            .start();
        
        System.out.println("✅ Serveur démarré sur le port " + port);
        
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.err.println("⚠️  Arrêt du serveur gRPC...");
            try {
                HelloWorldServer.this.stop();
            } catch (InterruptedException e) {
                e.printStackTrace(System.err);
            }
        }));
    }
    
    private void stop() throws InterruptedException {
        if (server != null) {
            server.shutdown().awaitTermination(30, TimeUnit.SECONDS);
        }
    }
    
    public void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }
    
    public static void main(String[] args) throws Exception {
        HelloWorldServer server = new HelloWorldServer();
        server.start(50051);
        server.blockUntilShutdown();
    }
}

