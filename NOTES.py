import glob
import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


# ------------------------------ #
#            Dataset             #
# ------------------------------ #
class StockDataset(Dataset):
    def __init__(self, csv_files, sequence_length=20):
        self.sequence_length = sequence_length
        all_data = []
        for file in csv_files:
            df = pd.read_csv(file)
            # Convert the 'Date' column to a numerical timestamp, if it exists.
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: x.timestamp())
            all_data.append(df)

        # Concatenate all CSV files
        self.data = pd.concat(all_data, ignore_index=True)

        # Define the feature columns (order is important)
        feature_cols = [
            'Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'MACD', 'CCI', 'ATR', 'BOLL',
            'EMA20', 'MA5', 'MA10', 'MTM6', 'MTM12', 'ROC', 'SMI', 'WVAD', 'Exchange rate', 'Interest rate'
        ]

        # Keep only the defined columns
        self.data = self.data[feature_cols]

        # Our target is the "Close" column; note that "Close" is also one of the features.
        self.target = self.data['Close']

        # Normalize features (including "Close" and converted Date)
        scaler = StandardScaler()
        self.features = scaler.fit_transform(self.data.values)

        # Create sequences using a sliding window.
        # Each input sample is a window of length `sequence_length` of consecutive rows,
        # and the target is the normalized "Close" value from the next time step.
        self.sequences = []
        self.sequence_targets = []
        # In our data, the "Close" column corresponds to index 1 (based on the order above).
        for i in range(len(self.features) - self.sequence_length):
            self.sequences.append(self.features[i:i + self.sequence_length])
            self.sequence_targets.append(self.features[i + self.sequence_length, 1])

        self.sequences = np.array(self.sequences)
        self.sequence_targets = np.array(self.sequence_targets)

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, index):
        # Return the sequence and its corresponding target.
        seq = torch.tensor(self.sequences[index], dtype=torch.float32)
        target = torch.tensor(self.sequence_targets[index], dtype=torch.float32)
        return seq, target


# ------------------------------ #
#            LSTM Model          #
# ------------------------------ #
class StockPriceLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super(StockPriceLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        batch_size = x.size(0)
        # Initialize hidden and cell states with zeros
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)

        # Pass the sequence through LSTM layers
        out, _ = self.lstm(x, (h0, c0))
        # Use the output from the final time step
        out = self.fc(out[:, -1, :])
        return out


# ------------------------------ #
#         Main Script            #
# ------------------------------ #
if __name__ == '__main__':
    # Locate CSV files in the provided folder.
    csv_folder = "/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/actions_data/connected_training_data"  # Ensure your CSV files are stored in this folder.
    csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

    # Create the dataset using a sliding window (default sequence_length = 20).
    sequence_length = 20
    dataset = StockDataset(csv_files, sequence_length)

    # Split the dataset: 80% training, 20% testing.
    train_size = int(0.8 * len(dataset)) #TODO return here, from this part not verified
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    batch_size = 64
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # Set the device (GPU if available).
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Define model parameters.
    input_dim = 20  # There are 20 features as listed above.
    hidden_dim = 64
    num_layers = 2
    output_dim = 1  # Predicting one value, the "Close" price.

    model = StockPriceLSTM(input_dim, hidden_dim, num_layers, output_dim).to(device)

    # Set the loss function and optimizer.
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # ------------------------------ #
    #         Training Loop          #
    # ------------------------------ #
    num_epochs = 50
    print("Training Model...")
    for epoch in range(num_epochs):
        model.train()
        train_losses = []

        for batch_seq, batch_target in train_loader:
            batch_seq = batch_seq.to(device)
            batch_target = batch_target.to(device).unsqueeze(1)  # Make sure target shape is [batch, 1]

            optimizer.zero_grad()
            outputs = model(batch_seq)
            loss = criterion(outputs, batch_target)
            loss.backward()
            optimizer.step()

            train_losses.append(loss.item())

        print(f"Epoch {epoch + 1}/{num_epochs}, Training Loss: {np.mean(train_losses):.4f}")

    # ------------------------------ #
    #         Evaluation             #
    # ------------------------------ #
    model.eval()
    predictions = []
    actuals = []
    with torch.no_grad():
        for batch_seq, batch_target in test_loader:
            batch_seq = batch_seq.to(device)
            batch_target = batch_target.to(device).unsqueeze(1)
            outputs = model(batch_seq)
            predictions.extend(outputs.cpu().numpy())
            actuals.extend(batch_target.cpu().numpy())

    predictions = np.array(predictions).squeeze()
    actuals = np.array(actuals).squeeze()
    test_loss = np.mean((predictions - actuals) ** 2)
    print(f"Test Loss: {test_loss:.4f}")

    # ------------------------------ #
    #         Plotting               #
    # ------------------------------ #
    # Plot 1: Predicted vs Actual values for the test set.
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(actuals)), actuals, label='Actual Close')
    plt.plot(range(len(predictions)), predictions, label='Predicted Close')
    plt.xlabel('Sample Index')
    plt.ylabel('Normalized Close Value')
    plt.title('Predicted vs Actual Close Values on Test Set')
    plt.legend()
    plt.show()

    # Plot 2: Display a sample input sequence with true and predicted target values.
    sample_index = 10  # You can modify this index to inspect a different sample.
    sample_seq, sample_target = test_dataset[sample_index]
    sample_seq_unsqueezed = sample_seq.unsqueeze(0).to(device)
    with torch.no_grad():
        sample_pred = model(sample_seq_unsqueezed).cpu().item()

    # For visualization, extract the Close values from the sequence.
    # The "Close" column is at index 1 based on the order in feature_cols.
    close_sequence = sample_seq.numpy()[:, 1]

    plt.figure(figsize=(8, 4))
    plt.plot(range(sequence_length), close_sequence, marker='o', label='Input Sequence (Close)')
    plt.axhline(y=sample_target, color='green', linestyle='--', label='True Target (Next Close)')
    plt.axhline(y=sample_pred, color='red', linestyle='--', label='Predicted Target')
    plt.xlabel('Time Step')
    plt.ylabel('Normalized Value')
    plt.title('Sample Input Sequence with True and Predicted Close Price')
    plt.legend()
    plt.show()
