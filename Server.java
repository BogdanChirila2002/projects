import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Server {

    public static void main(String[] args) {
        final int PORT = 12345;

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Serverul este pornit și ascultă pe portul " + PORT);

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Conexiune acceptată de la " + clientSocket.getInetAddress());

                ClientHandler clientHandler = new ClientHandler(clientSocket);
                new Thread(clientHandler).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;
    private Scanner input;
    private PrintWriter output;

    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
        try {
            this.input = new Scanner(socket.getInputStream());
            this.output = new PrintWriter(socket.getOutputStream(), true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        try {
            while (true) {
                if (input.hasNext()) {
                    String clientMessage = input.nextLine();
                    System.out.println("Mesaj de la client: " + clientMessage);

                    output.println("Mesaj primit: " + clientMessage);
                }
            }
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}