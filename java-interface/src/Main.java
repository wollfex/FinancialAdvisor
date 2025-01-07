import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Main {
    public static void main(String[] args) {
        // Creates the window
        JFrame frame = new JFrame("Financial Tracker");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        frame.setLayout(new FlowLayout());


        // Create dropdown account selection
        String[] accounts = {"All Accounts", "Checking Account", "Savings Account"};
        JComboBox<String> accountDropdown = new JComboBox<>(accounts);
        accountDropdown.addItem("Loading. Please wait.");

        // Create a refresh button
        JButton refreshButton = new JButton("Refresh");

        // Handles button clicks
        refreshButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    String[] accounts = APIClient.fetchAccounts();
                    accountDropdown.removeAllItems();
                    for (String account : accounts) {
                        accountDropdown.addItem(account);
                    }
                    JOptionPane.showMessageDialog(frame, "Accounts refreshed");
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, "Failed to fetch accounts: " + ex.getMessage());
                }
            }
        });

        frame.add(accountDropdown);
        frame.add(refreshButton);
        frame.setVisible(true);
    }
}