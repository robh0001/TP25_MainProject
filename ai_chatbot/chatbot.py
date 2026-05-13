import json
import os
from typing import List, Dict, Optional, Tuple

import anthropic
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FAQ_PATH = os.path.join(BASE_DIR, "faq_data.json")


class HealthyKidsChatbot:
    def __init__(
        self,
        faq_file: str = DEFAULT_FAQ_PATH,
        embedding_model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.45,
        short_query_threshold: float = 0.30,
        use_llm: bool = False,
        llm_model: str = "claude-haiku-4-5-20251001",
        top_k: int = 3,
    ) -> None:
        self.faq_file = faq_file
        self.embedding_model_name = embedding_model_name
        self.similarity_threshold = similarity_threshold
        self.short_query_threshold = short_query_threshold
        self.use_llm = use_llm
        self.llm_model = llm_model
        self.top_k = top_k

        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        self.faq_data = self._load_faq_data()

        self.intent_to_items = self._group_by_intent(self.faq_data)

        self.all_questions = [item["question"] for item in self.faq_data]
        self.all_answers = [item["answer"] for item in self.faq_data]
        self.all_intents = [item["intent"] for item in self.faq_data]

        self.all_embeddings = self.embedding_model.encode(
            self.all_questions,
            convert_to_numpy=True
        )

        self.intent_embeddings = {}
        for intent, items in self.intent_to_items.items():
            questions = [item["question"] for item in items]
            self.intent_embeddings[intent] = self.embedding_model.encode(
                questions,
                convert_to_numpy=True
            )

        self.vectorizer, self.classifier = self._train_classifier()

        if self.use_llm:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "ANTHROPIC_API_KEY environment variable is not set. "
                    "Please set it before running with use_llm=True."
                )
            self.llm_client = anthropic.Anthropic(api_key=api_key)

    def _load_faq_data(self) -> List[Dict[str, str]]:
        with open(self.faq_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("FAQ data must be a list.")

        for item in data:
            if "intent" not in item or "question" not in item or "answer" not in item:
                raise ValueError("Each FAQ item must contain intent, question, and answer.")

        return data

    def _group_by_intent(self, data: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        grouped: Dict[str, List[Dict[str, str]]] = {}
        for item in data:
            grouped.setdefault(item["intent"], []).append(item)
        return grouped

    def _train_classifier(self) -> Tuple[TfidfVectorizer, LogisticRegression]:
        questions = [item["question"] for item in self.faq_data]
        labels = [item["intent"] for item in self.faq_data]

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        X = vectorizer.fit_transform(questions)

        classifier = LogisticRegression(max_iter=1000)
        classifier.fit(X, labels)

        return vectorizer, classifier

    def _is_short_query(self, user_input: str) -> bool:
        return len(user_input.strip().split()) <= 3

    def _detect_intent_by_keywords(self, user_input: str) -> Optional[str]:
        text = user_input.lower()

        nutrition_keywords = [
            "food", "eat", "eating", "vegetable", "vegetables", "fruit", "fruits",
            "snack", "snacks", "dinner", "breakfast", "lunch", "meal", "meals",
            "picky", "drink", "drinks", "juice", "protein", "calcium", "iron",
            "fibre", "fiber", "vitamin", "vitamins", "cheese", "chips", "sweets",
            "sugar", "fast food", "smoothie", "smoothies", "vegetarian", "meat",
            "milk", "appetite"
        ]

        activity_keywords = [
            "exercise", "sport", "sports", "activity", "activities", "active",
            "play", "playing", "outdoor", "walk", "walking", "run", "running",
            "swim", "swimming", "bike", "biking", "cycle", "cycling", "dance",
            "dancing", "yoga", "stretch", "stretching", "martial arts", "hike",
            "hiking", "movement", "fitness"
        ]

        screen_keywords = [
            "screen", "screens", "ipad", "tablet", "phone", "tv", "youtube",
            "game", "games", "gaming", "device", "devices", "roblox", "movie",
            "movies", "streaming", "social media", "online", "internet",
            "parental controls", "bedtime screen", "screen-free"
        ]

        routine_keywords = [
            "sleep", "bedtime", "routine", "routines", "schedule", "morning",
            "habit", "habits", "homework", "after-school", "weekend", "reading",
            "transition", "transitions", "wake", "waking", "alarm", "checklist",
            "visual schedule", "evening", "daily structure"
        ]

        if any(word in text for word in nutrition_keywords):
            return "nutrition"
        if any(word in text for word in activity_keywords):
            return "activity"
        if any(word in text for word in screen_keywords):
            return "screen"
        if any(word in text for word in routine_keywords):
            return "routine"

        return None

    def _predict_intent(self, user_input: str) -> Tuple[str, float]:
        X = self.vectorizer.transform([user_input])
        probabilities = self.classifier.predict_proba(X)[0]
        labels = self.classifier.classes_

        best_index = int(np.argmax(probabilities))
        return labels[best_index], float(probabilities[best_index])

    def _predict_top_intents(
        self,
        user_input: str,
        top_n: int = 2
    ) -> List[Tuple[str, float]]:
        X = self.vectorizer.transform([user_input])
        probabilities = self.classifier.predict_proba(X)[0]
        labels = self.classifier.classes_

        top_n = min(top_n, len(labels))
        top_indices = np.argsort(probabilities)[::-1][:top_n]
        return [(labels[i], float(probabilities[i])) for i in top_indices]

    def _search_by_intent(
        self,
        user_input: str,
        intent: str,
        top_k: Optional[int] = None,
    ) -> List[Tuple[Dict[str, str], float]]:
        k = top_k if top_k is not None else self.top_k
        items = self.intent_to_items[intent]
        embeddings = self.intent_embeddings[intent]

        user_embedding = self.embedding_model.encode([user_input], convert_to_numpy=True)
        similarities = cosine_similarity(user_embedding, embeddings)[0]

        k = min(k, len(items))
        top_indices = np.argsort(similarities)[::-1][:k]

        return [(items[i], float(similarities[i])) for i in top_indices]

    def _build_faq_context(
        self,
        top_results: List[Tuple[Dict[str, str], float]],
        min_score: float,
    ) -> str:
        lines: List[str] = []

        for rank, (item, score) in enumerate(top_results, start=1):
            if score < min_score:
                continue

            lines.append(
                f"[{rank}] Q: {item['question']}\n"
                f"    A: {item['answer']}"
            )

        return "\n\n".join(lines) if lines else ""

    def _rewrite_with_llm(
        self,
        user_input: str,
        top_results: List[Tuple[Dict[str, str], float]],
        intent: str,
    ) -> str:
        threshold = (
            self.short_query_threshold
            if self._is_short_query(user_input)
            else self.similarity_threshold
        )

        faq_context = self._build_faq_context(top_results, min_score=threshold)

        if not faq_context:
            return top_results[0][0]["answer"]

        system_prompt = (
            "You are a warm and supportive assistant helping parents with children's health and wellness.\n\n"
            "Your task:\n"
            "- Answer the parent's question using ONLY the FAQ references provided.\n"
            "- Synthesise the references into one clear and practical reply.\n"
            "- Speak directly to the parent in a friendly and supportive tone.\n"
            "- Keep the response concise (2–3 sentences maximum).\n"
            "- Prefer short, direct sentences over long explanations.\n"
            "- Do NOT add any information, examples, numbers, or advice that are not supported by the references.\n"
            "- Do NOT suggest consulting doctors, pediatricians, professionals, or external websites unless this is explicitly mentioned in the references.\n"
            "- If the references do not fully answer the question, say that clearly instead of guessing.\n"
            "- Respond in the same language as the parent.\n"
            "- If multiple references provide slightly different suggestions, combine them into a consistent and coherent answer."
        )

        user_message = (
            f"Parent's question: {user_input}\n\n"
            f"FAQ references (topic: {intent}):\n"
            f"{faq_context}\n\n"
            "Please provide a helpful, synthesised response based solely on "
            "the references above."
        )

        response = self.llm_client.messages.create(
            model=self.llm_model,
            max_tokens=150,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        return response.content[0].text

    def get_response(self, user_input: str) -> Dict[str, Optional[str]]:
        cleaned_input = user_input.strip()

        if not cleaned_input:
            return {
                "user_input": user_input,
                "predicted_intent": None,
                "intent_confidence": None,
                "matched_question": None,
                "similarity_score": None,
                "answer": "Please enter a valid question.",
            }

        intent_confidence: Optional[float] = None

        if self._is_short_query(cleaned_input):
            predicted_intent = self._detect_intent_by_keywords(cleaned_input)

            if predicted_intent is None:
                predicted_intent, intent_confidence = self._predict_intent(cleaned_input)
        else:
            predicted_intent, intent_confidence = self._predict_intent(cleaned_input)

        LOW_CONFIDENCE_THRESHOLD = 0.5

        if intent_confidence is not None and intent_confidence < LOW_CONFIDENCE_THRESHOLD:
            top_intents = self._predict_top_intents(cleaned_input, top_n=2)
            top_results = []
            seen_questions: set = set()

            for intent_name, _ in top_intents:
                for item, score in self._search_by_intent(cleaned_input, intent_name):
                    if item["question"] not in seen_questions:
                        top_results.append((item, score))
                        seen_questions.add(item["question"])

            top_results.sort(key=lambda x: x[1], reverse=True)
        else:
            top_results = self._search_by_intent(cleaned_input, predicted_intent)

        threshold = (
            self.short_query_threshold
            if self._is_short_query(cleaned_input)
            else self.similarity_threshold
        )

        valid_results = [
            (item, score) for item, score in top_results if score >= threshold
        ]

        if not valid_results:
            _, top1_score = top_results[0]

            return {
                "user_input": user_input,
                "predicted_intent": predicted_intent,
                "intent_confidence": (
                    None if intent_confidence is None else round(intent_confidence, 4)
                ),
                "matched_question": None,
                "similarity_score": round(top1_score, 4),
                "answer": (
                    "I found a related topic, but I need a little more detail "
                    "to give a useful suggestion. "
                    "Please describe your question a bit more clearly."
                ),
            }

        best_item, best_score = max(valid_results, key=lambda x: x[1])

        if self.use_llm:
            final_answer = self._rewrite_with_llm(
                user_input=cleaned_input,
                top_results=valid_results,
                intent=predicted_intent,
            )
        else:
            final_answer = best_item["answer"]

        return {
            "user_input": user_input,
            "predicted_intent": predicted_intent,
            "intent_confidence": (
                None if intent_confidence is None else round(intent_confidence, 4)
            ),
            "matched_question": best_item["question"],
            "similarity_score": round(best_score, 4),
            "answer": final_answer,
        }


def main() -> None:
    chatbot = HealthyKidsChatbot(
        faq_file=DEFAULT_FAQ_PATH,
        use_llm=True,
        top_k=3,
    )

    print("Healthy Kids Chatbot is running.")
    print(f"LLM mode: {'ON  (Claude API)' if chatbot.use_llm else 'OFF (FAQ only)'}")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Chatbot: Goodbye!")
            break

        result = chatbot.get_response(user_input)

        print(f"Predicted Intent  : {result['predicted_intent']}")
        print(f"Intent Confidence : {result['intent_confidence']}")
        print(f"Matched Question  : {result['matched_question']}")
        print(f"Similarity Score  : {result['similarity_score']}")
        print(f"Chatbot           : {result['answer']}\n")


if __name__ == "__main__":
    main()