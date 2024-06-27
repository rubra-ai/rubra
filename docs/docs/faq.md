---
sidebar_position: 3
title: FAQ
---

# Frequently Asked Questions

This page will cover common questions and issues that users may encounter when using Rubra.

### FAQ

#### Who are the intended users of Rubra?
Rubra models are for anyone looking to use open source LLMs with native function calling support, which yields superior results in local LLMs when compared to prompting models to return tool calls.

---

#### Why use Rubra models over Llama, Mistral, or other popular fine tunes like Hermes Pro or Gorilla OpenFunctions?
Rubra models are capable of complex, multi-step, function calls (chain of function) and enhance popular open source instruct LLMs while retaining their original capabilities. While Hermes Pro is exceptional at chat and Gorilla OpenFunctions is good at basic function calling, Rubra models excel in both chat and complex, multi-step function calling.

---

#### Mistral-7B-Instruct-v0.3 has tool calling capability, so why use Rubra enhanced Mistral-7B-Instruct-v0.3
Rubra enhanced Mistral-7B-Instruct-v0.3 is capable of complex tool calling that original model falls short of. TODO INSERT EXAMPLE

---

#### vLLM has tool calling capability, so why use Rubra?
vLLM expects that if you pass in tools, the LLM response will make a tool call. It inhibits the user's ability to chat with the model and puts the responsibility of passing in tools to the user or whatever is orchestrating the chat. 
Using Rubra enhanced models and custom vLLM will give the LLM full discretion on when to make a tool call and when to reply with an assistant message - the same way OpenAI models work.

---

#### How were Rubra models trained?
We curated a high quality tool calling dataset consisting of over 1 million conversations and TODO n million tool calls. The dataset consists of TODO N billion tokens. We spent 1000s of A100 and H100 GPU hours training the models. The smaller models were block expanded to ensure the parent model capabilities weren't lost, while the larger models followed an iterative training technique in which guide tokens were introduced initially for fast convergence, and removed in later stages to reduce token usage. We anticipate publishing a technical report on our recipe in the future.

---

#### Why do the benchmark results differ from the ones found in parent model cards?
We use 2 popular tools to compute our benchmarks - see below. These tools are constantly improving and evolving, so the evaluation results can differ from when the parent model lab ran their benchmarks due to a variety of reasons. From what we've observed, all numbers we produce are in the same ballpark as parent models, and our numbers are consistent across all evaluated models as of June 2024. For MT-bench, the model under evaluation is judged by GPT-4, so any update by OpenAI to GPT-4 will change the results, but not by much. **We do not try to game the benchmarks with our Rubra enhanced models.**

1. [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
	- For MMLU, GPQA, GSM-8k, MATH
2. [FastChat LLM Judge](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
	- For MT-bench

---

#### How did you construct the training set for Rubra models?
We came up with a phrase named "chain of function". Chain of function is the process of calling and chaining multiple and/or consecutive function calls to achieve an end goal. This method is particularly relevant when integrating the LLM with user-defined tools, allowing for complex workflows and operations.

Here's an example: Customer Feedback Processing

**Prompt**: "Retrieve raw customer feedback using `getFeedback`, clean the data using `cleanFeedback`, analyze the cleaned data using `analyzeFeedback`, and generate a report using `generateReport`."

**Available Functions**:
- `getFeedback`: Retrieves raw customer feedback from a database.
  - **Parameters**: None.
  - **Result**: Returns a JSON array of feedback entries, each containing text and metadata.
- `cleanFeedback`: Cleans the retrieved feedback by removing spam, correcting typos, and standardizing text format.
  - **Parameters**:
    - `feedbackData`: A JSON array of raw customer feedback.
  - **Result**: Returns a JSON array of cleaned feedback entries.
- `analyzeFeedback`: Analyzes the cleaned feedback to identify key themes and sentiments.
  - **Parameters**:
    - `cleanedData`: A JSON array of cleaned feedback.
  - **Result**: Returns a summary object with counts of positive, negative, and neutral feedback, along with common themes.
- `generateReport`: Generates a detailed report based on the analysis, summarizing key insights and recommendations.
  - **Parameters**:
    - `analysisResults`: An object containing analysis results of customer feedback.
  - **Result**: Returns a formatted text report detailing customer satisfaction and areas for improvement.

**Expected Function Calls**:
1. **`getFeedback`**:
   - **Arguments**: None
   - **Result**: `[{"id": 1, "comment": "Great service!", "metadata": {"timestamp": "2023-06-01"}}, {"id": 2, "comment": "Poor experience.", "metadata": {"timestamp": "2023-06-01"}}]`
2. **`cleanFeedback`**:
   - **Arguments**: `{ "feedbackData": [{"id": 1, "comment": "Great service!", "metadata": {"timestamp": "2023-06-01"}}, {"id": 2, "comment": "Poor experience.", "metadata": {"timestamp": "2023-06-01"}}] }`
   - **Result**: `[{"id": 1, "comment": "Great service"}, {"id": 2, "comment": "Poor experience"}]`
3. **`analyzeFeedback`**:
   - **Arguments**: `{ "cleanedData": [{"id": 1, "comment": "Great service"}, {"id": 2, "comment": "Poor experience"}] }`
   - **Result**: `{ "positive": 1, "negative": 1, "themes": ["service quality"] }`
4. **`generateReport`**:
   - **Arguments**: `{ "analysisResults": { "positive": 1, "negative": 1, "themes": ["service quality"] } }`
   - **Result**: `"Customer Feedback Report: 1 positive feedback, 1 negative feedback. Key theme identified: Service Quality. Recommendations: Enhance training on customer interaction."`

**Final Answer Should**: "The answer should indicate that the final output is a detailed report titled 'Customer Feedback Report', which synthesizes all previous processing steps into actionable insights."
