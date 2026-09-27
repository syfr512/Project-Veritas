import os
import json
import argparse
from typing import List
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from app.services.video_analyzer import analyze_video
from app.services.audio_analyzer import analyze_audio

def evaluate_dataset(dataset_dir: str, file_type: str = "video"):
    """
    Evaluates the Project Veritas detection models against a structured dataset
    expected to have two subdirectories: 'real' and 'fake'.
    """
    y_true = []
    y_scores = []
    
    real_dir = os.path.join(dataset_dir, "real")
    fake_dir = os.path.join(dataset_dir, "fake")
    
    if not os.path.exists(real_dir) or not os.path.exists(fake_dir):
        print(f"Dataset directory must contain 'real' and 'fake' subfolders.")
        return
        
    print(f"Starting evaluation on dataset: {dataset_dir}")
    
    # Process Real
    for file in os.listdir(real_dir):
        path = os.path.join(real_dir, file)
        score = process_file(path, file_type)
        y_true.append(0) # 0 for real
        y_scores.append(score)
        
    # Process Fake
    for file in os.listdir(fake_dir):
        path = os.path.join(fake_dir, file)
        score = process_file(path, file_type)
        y_true.append(1) # 1 for fake
        y_scores.append(score)
        
    if not y_true:
        print("No files processed.")
        return
        
    # Calculate metrics (Threshold = 0.5)
    y_pred = [1 if s >= 0.5 else 0 for s in y_scores]
    
    roc_auc = roc_auc_score(y_true, y_scores) if len(set(y_true)) > 1 else 0.0
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    print("\n--- Evaluation Results ---")
    print(f"Total Files: {len(y_true)}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    
    # Save results
    with open(os.path.join(dataset_dir, "evaluation_results.json"), "w") as f:
        json.dump({
            "roc_auc": roc_auc,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }, f, indent=4)

def process_file(filepath: str, file_type: str) -> float:
    print(f"Processing: {os.path.basename(filepath)}")
    try:
        if file_type == "video":
            result = analyze_video(filepath)
        else:
            result = analyze_audio(filepath)
        return float(result.get("risk_score", 0.0))
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Veritas ML Models for Thesis")
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset directory (containing 'real' and 'fake' folders)")
    parser.add_argument("--type", type=str, choices=["video", "audio"], default="video", help="Type of media to evaluate")
    
    args = parser.parse_args()
    evaluate_dataset(args.dataset, args.type)
