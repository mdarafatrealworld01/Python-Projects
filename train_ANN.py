import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.model_selection import KFold
from LoadDataset import X_train_pca, y_train

# Convert data to PyTorch tensors
X_train_pca = torch.tensor(X_train_pca, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)

# Define ANN model class
class ANN(nn.Module):
    def __init__(self, input_size):
        super(ANN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc3(x))
        return x

# Train function
def train_model(model, X_train, y_train, epochs=20, batch_size=32):
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train).squeeze()
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 5 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
    
    return model

# K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
fold = 1
accuracies = []
roc_auc_scores = []

for train_idx, val_idx in kf.split(X_train_pca):
    print(f'Fold {fold}')
    X_train_fold, X_val_fold = X_train_pca[train_idx], X_train_pca[val_idx]
    y_train_fold, y_val_fold = y_train[train_idx], y_train[val_idx]
    
    model = ANN(X_train_pca.shape[1])
    model = train_model(model, X_train_fold, y_train_fold)
    
    # Get the predictions for ROC curve
    y_prob = model(X_val_fold).detach().numpy().squeeze()  # Probability of fraud
    
    # Compute accuracy
    y_pred = (y_prob > 0.5).astype("int32")
    acc = accuracy_score(y_val_fold, y_pred)
    accuracies.append(acc)
    
    # Print classification report for Precision, Recall, F1-Score
    print(f"Classification Report for Fold {fold}:\n")
    print(classification_report(y_val_fold, y_pred, target_names=["Not Fraud", "Fraud"]))
    
    # Calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_val_fold, y_prob)
    roc_auc = auc(fpr, tpr)
    roc_auc_scores.append(roc_auc)
    
    # Plot ROC curve
    plt.plot(fpr, tpr, label=f'Fold {fold} (AUC = {roc_auc:.2f})')
    
    print(f'Accuracy for Fold {fold}: {acc:.4f}')
    print(f'AUC for Fold {fold}: {roc_auc:.4f}\n')
    fold += 1

# Average accuracy and AUC across all folds
print(f'Average Accuracy: {sum(accuracies) / len(accuracies):.4f}')
print(f'Average AUC: {sum(roc_auc_scores) / len(roc_auc_scores):.4f}')

# Plot the ROC curve for all folds
plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line (no discrimination)
plt.title('ROC Curve for Fraud Detection')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.show()
