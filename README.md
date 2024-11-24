## Problem Statement
The aim of this project is to map words in a sentence to their appropriate contextual categories to facilitate their conversion into sign language for the deaf. Each word must be classified into one of a predefined set of categories (e.g., Finance, Legal, Numbers, Locations, etc.) based on its usage in context. Accurate classification is crucial to ensure the correct interpretation and conveyance of meaning in sign language.
________________________________________
## Idea
1.	Initial Plan with API
Initially, we used an API (powered by GPT-4) to classify words into categories based on context. While the API showed promise in understanding sentences, its responses were inconsistent and often mapped words to general or irrelevant categories, reducing the accuracy of the classification.
2.	Integration of BERT
To improve classification, we incorporated BERT (Bidirectional Encoder Representations from Transformers). BERT is a pretrained language model designed to generate contextual word embeddings by analyzing the entire sentence context in both directions (left-to-right and right-to-left). These embeddings are particularly useful for context-aware tasks.
Using BERT, we aimed to classify each word into one of our predefined categories. However, BERT’s pretrained model was not specifically designed for our custom categories. Moreover, it exhibited limitations:
o	Repetition Issue: In sentences where the same word appeared multiple times, BERT often assigned a category based on its first occurrence, ignoring subsequent contextual variations.
3.	Combining API and BERT
To overcome the limitations of both methods, we integrated BERT and the API into a unified workflow:
o	BERT’s Role: It generates contextual embeddings for words in the sentence. These embeddings represent the contextual meaning of each word.
o	API’s Role: The API utilizes these embeddings, along with BERT’s classification, as weighted inputs to determine the most contextually accurate category for each word. The final classification is constrained to our predefined categories to ensure relevance.
________________________________________
## Implementation
1.	Predefined Categories:
We defined 20 specific categories such as Finance, Legal, Numbers, Food, Nature, etc., to guide the classification process.
2.	Dummy Dataset:
We created a dummy dataset representing words and their contextual meanings to simulate training for BERT. While this dataset allowed us to explore the training process, due to time and resource constraints, we did not train BERT.
3.	Limitations of Pretrained BERT:
The pretrained BERT model supports only general contextual classification or up to 4 default categories. For our custom categories, training was necessary. However, due to the lack of sufficient labeled data and time, we focused on showing how training could be implemented, leaving actual training for future work.
4.	API and BERT Integration:
o	BERT: Generates embeddings for words.
o	API: Combines BERT-generated embeddings with sentence context to refine the classification.
o	Logic: A weighted approach gives 70% weight to BERT’s output and 30% to the API’s context analysis. This ensures the output is precise and fits into one of the predefined categories.
________________________________________
## Outcome
The integration of BERT and the API resulted in more accurate and precise word classifications. By combining contextual embeddings and external API-based context analysis, our system successfully addresses the challenge of mapping words to their appropriate categories, paving the way for effective translation into sign language for the deaf.
The project also demonstrates how BERT models can be retrained with a custom dataset for more tailored classifications in future iterations.