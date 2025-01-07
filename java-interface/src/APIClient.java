import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.BufferOverflowException;

public class APIClient {

    // Method that fetches accounts using Flask
    public static String[] fetchAccounts() throws Exception {
        String apiUrl = "http://127.0.0.1:5000/accounts"; // Flask API endpoint
        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Accept", "application/json");

        // Read response
        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
        connection.disconnect();

        // Parse JSON response
        JSONArray jsonArray = new JSONArray(response.toString());
        String[] accounts = new String[jsonArray.length()];
        for (int i = 0; i < jsonArray.length(); i++) {
            accounts[i] = jsonArray.getJSONObject(i).getString("name");
        }
        return accounts;
    }
}
