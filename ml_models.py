"""
Campus Circle AI - Machine Learning Engine
Incorporating Supervised Learning (Regression/Decision Trees - Masterclass 3)
and Content-based Skill Recommender (TF-IDF & Cosine Similarity)
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FairPricePredictor:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "data", "campus_items.csv")
        self.data_path = data_path
        self.model = None
        self.dt_model = None
        self.categories = []
        self.metrics = {}
        self._train()

    def _train(self):
        df = pd.read_csv(self.data_path)
        # One-hot encode category
        X = pd.get_dummies(df[["category", "original_mrp", "age_semesters", "condition_rating", "demand_index"]], drop_first=False)
        self.feature_columns = X.columns.tolist()
        y = df["fair_price_inr"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Random Forest
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
        rf.fit(X_train, y_train)
        self.model = rf

        # Train Decision Tree (Masterclass 3 reference)
        dt = DecisionTreeRegressor(max_depth=5, random_state=42)
        dt.fit(X_train, y_train)
        self.dt_model = dt

        y_pred_rf = rf.predict(X_test)
        y_pred_dt = dt.predict(X_test)

        self.metrics = {
            "RandomForest_R2": round(r2_score(y_test, y_pred_rf), 4),
            "RandomForest_MAE": round(mean_absolute_error(y_test, y_pred_rf), 2),
            "DecisionTree_R2": round(r2_score(y_test, y_pred_dt), 4),
            "DecisionTree_MAE": round(mean_absolute_error(y_test, y_pred_dt), 2),
            "train_size": len(X_train),
            "test_size": len(X_test)
        }
        self.categories = df["category"].unique().tolist()

    def predict(self, category: str, original_mrp: float, age_semesters: int, condition_rating: int, demand_index: float = 0.85):
        # Create input row
        row = {col: 0 for col in self.feature_columns}
        cat_col = f"category_{category}"
        if cat_col in row:
            row[cat_col] = 1
        row["original_mrp"] = original_mrp
        row["age_semesters"] = age_semesters
        row["condition_rating"] = condition_rating
        row["demand_index"] = demand_index

        input_df = pd.DataFrame([row])
        pred_rf = float(self.model.predict(input_df)[0])
        pred_dt = float(self.dt_model.predict(input_df)[0])

        fair_price = max(40.0, round(pred_rf, -1)) # round to nearest 10
        depreciation_pct = round(((original_mrp - fair_price) / original_mrp) * 100, 1)

        return {
            "suggested_fair_price": int(fair_price),
            "decision_tree_estimate": int(round(pred_dt, -1)),
            "depreciation_percent": max(0.0, depreciation_pct),
            "student_saving_inr": int(max(0, original_mrp - fair_price))
        }

    def explain_prediction(self, original_mrp: float, age_semesters: int, condition_rating: int, demand_index: float, fair_price: float):
        age_impact = round(original_mrp * (age_semesters * 0.085), 2)
        condition_impact = round(original_mrp * ((5 - condition_rating) * 0.075), 2)
        demand_effect = round(original_mrp * (demand_index - 0.75) * 0.15, 2)
        return {
            "Original MRP": round(original_mrp, 2),
            "Age Depreciation": -abs(age_impact),
            "Condition Impact": -abs(condition_impact),
            "Demand Adjustment": demand_effect,
            "Fair Secondhand Price": fair_price
        }


class SkillMatcher:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "data", "peer_mentors.csv")
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.rebuild_corpus()

    def rebuild_corpus(self):
        # Combine skills_offered + bio + branch for rich semantic matching
        self.corpus = (
            self.df["skills_offered"].fillna("") + " " + 
            self.df["bio"].fillna("") + " " + 
            self.df["branch"].fillna("")
        ).tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

        # Vectorizer for skills_wanted (two-way barter)
        self.wanted_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.wanted_corpus = self.df["skills_wanted"].fillna("").tolist()
        if any(len(c.strip()) > 0 for c in self.wanted_corpus):
            self.wanted_matrix = self.wanted_vectorizer.fit_transform(self.wanted_corpus)
        else:
            self.wanted_matrix = None

    def add_mentor(self, mentor_dict: dict):
        new_row = pd.DataFrame([mentor_dict])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.rebuild_corpus()

    def find_matches(self, query: str, top_k: int = 4):
        query_vec = self.vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        ranked_indices = np.argsort(sim_scores)[::-1][:top_k]
        
        results = []
        for idx in ranked_indices:
            score = float(sim_scores[idx])
            mentor = self.df.iloc[idx].to_dict()
            mentor["match_score_pct"] = round(score * 100, 1)
            results.append(mentor)
        return results

    def find_two_way_barter(self, learn_query: str, teach_query: str = "", top_k: int = 4):
        learn_vec = self.vectorizer.transform([learn_query])
        learn_scores = cosine_similarity(learn_vec, self.tfidf_matrix).flatten()

        if teach_query and self.wanted_matrix is not None:
            teach_vec = self.wanted_vectorizer.transform([teach_query])
            teach_scores = cosine_similarity(teach_vec, self.wanted_matrix).flatten()
            combined_scores = (learn_scores * 0.6) + (teach_scores * 0.4)
        else:
            combined_scores = learn_scores
            teach_scores = np.zeros_like(learn_scores)

        ranked_indices = np.argsort(combined_scores)[::-1][:top_k]

        results = []
        for idx in ranked_indices:
            mentor = self.df.iloc[idx].to_dict()
            mentor["match_score_pct"] = round(float(learn_scores[idx]) * 100, 1)
            mentor["barter_score_pct"] = round(float(teach_scores[idx]) * 100, 1) if teach_query else 0.0
            mentor["combined_score_pct"] = round(float(combined_scores[idx]) * 100, 1)
            mentor["is_mutual_barter"] = bool(mentor["match_score_pct"] > 20 and mentor["barter_score_pct"] > 15)
            results.append(mentor)
        return results

    def get_all_mentors(self):
        return self.df.to_dict(orient="records")


def calculate_sdg_impact(total_swaps=142, avg_saving_per_item=480, skill_hours=320):
    total_savings = total_swaps * avg_saving_per_item
    # Approx 1.8 kg paper/plastic waste diverted per campus resource exchange
    waste_diverted_kg = round(total_swaps * 1.85, 1)
    co2_offset_kg = round(waste_diverted_kg * 1.22, 1)

    return {
        "total_monetary_saved_inr": total_savings,
        "waste_diverted_kg": waste_diverted_kg,
        "co2_offset_kg": co2_offset_kg,
        "peer_skill_hours": skill_hours,
        "active_students": total_swaps * 2 + int(skill_hours * 1.2)
    }
