import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {
        final String SERVER_IP = "localhost";
        final int SERVER_PORT = 12345;

        try (Socket socket = new Socket(SERVER_IP, SERVER_PORT);
             Scanner scanner = new Scanner(System.in);
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
             Scanner input = new Scanner(socket.getInputStream())) {

            System.out.println("Conectat la server. Puteți începe să trimiteți mesaje.");

            while (true) {
                System.out.print("Trimiteți un mesaj către server: ");
                String message = scanner.nextLine();

                output.println(message);

                String response = input.nextLine();
                System.out.println("Răspuns de la server: " + response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}