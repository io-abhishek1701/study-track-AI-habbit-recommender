import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from io import BytesIO

FEATURE_COLUMNS = ['StudyHours', 'WorkHours', 'PlayHours', 'SleepHour', 'Marks']


def get_cluster_performance_map(kmeans, scaler):
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    marks_index = FEATURE_COLUMNS.index('Marks')
    clusters_by_marks = sorted(
        enumerate(centers),
        key=lambda item: item[1][marks_index]
    )

    labels = [
        "Performance: CRITICAL (Needs Improvement)",
        "Performance: OK (Room for Optimization)",
        "Performance: EXCELLENT (Maintain Trajectory)"
    ]

    return {
        cluster_id: labels[rank]
        for rank, (cluster_id, _) in enumerate(clusters_by_marks)
    }


def get_cluster_status_map(kmeans, scaler):
    performance_map = get_cluster_performance_map(kmeans, scaler)
    return {
        cluster_id: label.replace("Performance: ", "")
        for cluster_id, label in performance_map.items()
    }


def train_kmeans_clustering(df):
   
    # Select features for clustering
    X = df[FEATURE_COLUMNS]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster_Number'] = kmeans.fit_predict(X_scaled)

    df['Remark'] = df['Cluster_Number'].map(get_cluster_status_map(kmeans, scaler))

    return df, scaler, kmeans


def save_clustered_excel(df, filename="student_remarks.xlsx"):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer


def plot_clusters(df):
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(df['StudyHours'], df['Marks'], c=df['Cluster_Number'])
    plt.xlabel("Study Hours")
    plt.ylabel("Marks")
    plt.title("K-Means Clustering of Students (3 Clusters)")
    plt.grid(True)

    # Legend
    handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
    plt.legend(handles, [f"Cluster {i}" for i in range(3)], title="Clusters")

    plt.show()
