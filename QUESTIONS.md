## Questions

## 1. Describe the default chunking strategy that you will use.

Chunking enables better handling of large documents, ensures context is maintained, and optimizes the retrieval and generation capabilities of language models. It's a foundational technique to manage complexity and ensure that NLP applications can process and interact with large volumes of text effectively.

For first pass I decided to use the RecursiveCharacterTextSplitter with a chunk size of 1200 and an chunk overlap of 100. This size strikes a balance between capturing substantial information and not losing too much context when breaking sections. By using this range, we can ensure that sections like headings, definitions, and lists stay together. Add overlap of about 100 to 200 characters between chunks. This helps preserve context when the text gets split mid-sentence or mid-thought, ensuring smooth transitions. The NIST and Blueprint documents likely contain detailed, interconnected ideas. A larger chunk size (1000-1500 characters) ensures that related information stays together, minimizing the risk of losing important context. Overlap ensures no loss of context across adjacent chunks, which is crucial for coherent question-answering tasks in downstream NLP applications like Retrieval-Augmented Generation (RAG).

```
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        length_function=tiktoken_len,
    )
```

The second proposed is to use a chunk size of 500. This is a smaller chunk size that can allow more precision and has lesser chance of retrieving irrelevant information compared to a larger chunk size. A 1200 chunk size however can retrieve overall or surrounding context which can be beneficial for understanding complex topics or maintaining coherence in longer passages.

```
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=tiktoken_len,
    )
```



## 2. How did you choose your stack, and why did you select each tool the way you did?

Great question. When selecting our stack, we evaluated several options, ultimately choosing a combination of LangGraph and LangChain as the core architecture for our two-agent system.

For the vector store, we opted for Qdrant due to its efficiency and speed in handling vector-based storage. This is crucial for managing and retrieving chunked document data. On the front end, we utilized Chainlit to provide an interactive UI for users to engage with the application. The entire system is deployed on Hugging Face, which simplifies deployment and scalability. Also we first used the "text-embedding-3-small" embedding model by Open AI for the intial setup for this stack.

LangChain was essential in allowing us to build chains of actions, such as retrieval, prompt enhancement, and generating responses using a Large Language Model (LLM). In our case, we’re using GPT-4o, which is a top-tier LLM for most use cases.

![Langgraph](./src/agents/output.jpeg)

The diagram above illustrates our two-agent architecture. By using LangGraph, we designed the system with a graph-like flow, where each node represents an agent. In a typical Retrieval-Augmented Generation (RAG) setup, a user’s query triggers data retrieval from the vector database based on vector embedding similarity. However, since our application is built as a chatbot (via Chainlit), users may follow up with additional questions that relate to the already retrieved context. It would be inefficient to retrieve the same context repeatedly for each follow-up. Moreover, users might input statements that aren't queries at all.

To address these cases, we designed a chat agent with tool calling that determines when a new retrieval is needed. It only triggers retrieval when a fresh query is received that can't be answered with the current context. The "rag agent" then generates the response and performs any necessary retrieval.

We also implemented streaming through LangGraph/LangChain's astream_events, enabling the application to provide faster response times.

## 3. What conclusions can you draw about performance and effectiveness of your pipeline with this information? 

Below are the evaluation metrics for the pipeline using the RAGAS framework for OpenAI Embeddings "text-embedding-3-small" with the above chunking strategy of 1200 chunk size and 100 chunk overlap.

### Evaluation Metrics

| Metric              | Score  |
|---------------------|--------|
| Faithfulness        | 0.82581|
| Answer Relevancy    | 0.81263|
| Context Recall      | 0.95666|
| Context Precision   | 0.90000|
| Answer Correctness  | 0.77387|

### Interpretation of Results

Context Understanding:

Context Recall (0.95666) and Context Precision (0.9000) are both very high, indicating that the model is excellent at identifying and retrieving relevant context. This suggests the pipeline is highly effective in understanding and capturing the appropriate context for given queries or tasks.


Faithfulness (0.82581):

This relatively high score suggests that the model's outputs are generally consistent with the input information. The pipeline is producing results that align well with the provided context or source material.


Answer Relevancy (0.81263):

The strong score here indicates that the answers or outputs generated are highly relevant to the input queries or tasks. This suggests good performance in producing on-topic and pertinent responses.


Answer Correctness (0.77387):

While still good, this is the lowest score among the metrics. It suggests that while the answers are relevant and faithful to the context, there might be some room for improvement in terms of factual accuracy or precision of the generated responses.

### Conclusions and Recommendations

Overall conclusions:

- Strong contextual understanding: The pipeline excels at identifying and using relevant context, which is crucial for many NLP tasks.
- High relevance and faithfulness: The system produces outputs that are both relevant to the input and faithful to the source material, indicating good overall performance.
Potential for improvement in accuracy: While the answer correctness is good, it's the lowest score, suggesting this could be an area for focused improvement in future iterations.
- Balanced performance: The pipeline shows well-rounded performance across different aspects, with no significant weak points.
- Effective for many applications: Given these metrics, the pipeline would likely be effective for tasks requiring strong context understanding and relevant output generation, such as question-answering systems, summarization, or information retrieval.
- Possible trade-offs: The high context recall and precision, combined with slightly lower answer correctness, might indicate that the model is very good at finding relevant information but might occasionally struggle with synthesizing it into perfectly accurate responses.


## 4. How did you choose the embedding model for this application? 

The model was uploaded to https://huggingface.co/rgtlai/ai-policy-ft. The notebook that shows the training can be seen at src/sdg/Fine_Tuned.ipynb and src/sdg/Fine_Tuned2.ipynb. 

I choose the Snowflake/snowflake-arctic-embed-m embedding model because it is lightweight as it has embedding dimension of 768 and 110 million parameters. It should perform well when it it is fine tuned. The results of the RAGAS framework on this model can be seen in src/sdg/Fine_Tuned.ipynb and src/sdg/Fine_Tuned2.ipynb.


## 5. Test the fine-tuned embedding model using the RAGAS frameworks to quantify any improvements.  Provide results in a table. Test the two chunking strategies using the RAGAS frameworks to quantify any improvements. Provide results in a table. Which one is the best to test with internal stakeholders next week, and why

Below are the evaluation metrics for the pipeline using the RAGAS framework for OpenAI Embeddings "fine-tuned" with the above chunking strategy of 1200 chunk size and 100 chunk overlap.

| Metric              | Score  |
|---------------------|--------|
| Faithfulness        | 0.8961 |
| Answer Relevancy    | 0.9228 |
| Context Recall      | 0.9666 |
| Context Precision   | 0.8986 |
| Answer Correctness  | 0.6249 |

Evaluation and Comparison:

Improvements:

Faithfulness increased by about 7%, indicating better alignment with input information.
Answer Relevancy saw a significant improvement of about 11%, suggesting more on-topic responses.
Context Recall slightly improved, maintaining its already high performance.


Slight Decrease:
Context Precision decreased marginally (about 0.14%), which is negligible given the improvement in other areas.


Significant Decline:
Answer Correctness dropped by about 14.9%, which is a notable decrease.

Analysis:
- Enhanced Relevance and Faithfulness:
The fine-tuned model shows significant improvements in producing relevant and faithful responses. This suggests that the model has become better at understanding and adhering to the context of queries.
- Maintained Strong Context Understanding:
The already strong Context Recall has slightly improved, while Context Precision remained virtually unchanged. This indicates that the model's ability to identify and use relevant context has been maintained through fine-tuning.
- Trade-off with Answer Correctness:
The substantial decrease in Answer Correctness is concerning. It suggests that while the model has become better at providing relevant and faithful responses, it may be struggling with factual accuracy.
- Potential Overfitting:
The improvement in relevancy and faithfulness coupled with the decrease in correctness might indicate some degree of overfitting to the fine-tuning dataset. The model may be prioritizing matching patterns in the training data over generating factually correct responses.

In conclusion, while the fine-tuned model shows promising improvements in several areas, the significant drop in answer correctness is a critical issue that needs to be addressed. The next steps should focus on maintaining the improved relevancy and faithfulness while boosting factual accuracy.

Possible work can be done to improve the answer correctness by increasing the size of the fine tuning dataset and retraining the model.

We also looked at different chunking strategies using chunk size of 500 and chunk overlap of 100. Here are the evaluation metrics:

| Metric              | Score  |
|---------------------|--------|
| Faithfulness        | 0.8186 |
| Answer Relevancy    | 0.8556 |
| Context Recall      | 0.9062 |
| Context Precision   | 0.8875 |
| Answer Correctness  | 0.7433 |

Evaluation and Comparison:

Faithfulness:

Setup 2 performs best, followed by Setup 1, then Setup 3.
The fine-tuned model shows a significant improvement in faithfulness.


Answer Relevancy:

Setup 2 leads by a considerable margin, with Setup 3 slightly outperforming Setup 1.
The fine-tuned model demonstrates superior relevancy in responses.


Context Recall:

Setup 2 slightly edges out Setup 1, while Setup 3 lags behind.
Larger chunk size (1200) seems to benefit context recall.


Context Precision:

All setups perform similarly, with Setup 1 having a slight edge.
Differences are minimal, suggesting consistent performance across setups.


Answer Correctness:

Setup 1 performs best, followed closely by Setup 3, with Setup 2 significantly behind.
The fine-tuned model (Setup 2) shows a notable drop in correctness.


Analysis:

Setup 1 (OpenEmbeddings, 1200 chunk size) shows balanced performance across all metrics.
Setup 2 (Fine-tuned model) excels in faithfulness, relevancy, and recall but struggles with correctness.
Setup 3 (OpenEmbeddings, 500 chunk size) shows improvements in relevancy compared to Setup 1 but slight decreases in other areas.

Final Recommendation:
Among the three setups, I would recommend Setup 1: OpenEmbeddings model with a chunk size of 1200 and overlap of 100. Here's why:

- Balanced Performance: It demonstrates the most balanced performance across all metrics, without any significant weaknesses.
- Superior Answer Correctness: It maintains the highest score in answer correctness, which is crucial for providing accurate information to users.
- Strong Context Handling: It shows excellent context recall and precision, indicating effective use of contextual information.
- Reliability: While it doesn't have the highest scores in faithfulness and relevancy, the differences are not drastic, and it compensates with better correctness.
- Avoiding Overfitting: Unlike Setup 2 (fine-tuned model), it doesn't show signs of potential overfitting, maintaining a good balance between relevancy and correctness.

While Setup 2 shows promising results in some areas, the significant drop in answer correctness is a major concern. Setup 3, with its smaller chunk size, doesn't offer substantial improvements over Setup 1 to justify the change.
Setup 1 provides the most reliable and balanced performance, making it the best choice for general use. However, if the use case prioritizes relevancy and faithfulness over strict factual correctness, Setup 2 might be worth considering, with additional measures to improve its accuracy.

## 6. What is the story that you will give to the CEO to tell the whole company at the launch next month? 

## AI Initiative: Empowering Ethical AI Understanding Across the Enterprise

### Executive Summary

Our AI initiative has successfully developed an innovative tool to address the growing need for AI education and ethical guidance within our organization. This chatbot leverages cutting-edge RAG (Retrieval-Augmented Generation) technology to provide our employees with accurate, context-aware information on AI ethics, policies, and industry developments.

### Key Achievements

1. **Data-Driven Insights**: Incorporated authoritative sources like the "Blueprint for an AI Bill of Rights" and the NIST AI Risk Management Framework.
2. **Advanced Technology Stack**: Utilized state-of-the-art open-source tools and models to create a robust, scalable solution.
3. **Performance Optimization**: Implemented fine-tuned embedding models and optimized data chunking strategies to enhance accuracy and relevance.
4. **Rigorous Evaluation**: Employed the RAGAS framework to quantify and improve the system's performance across key metrics.

### Impact and Benefits

- **Informed Workforce**: Empowers employees with up-to-date knowledge on AI ethics and policies.
- **Risk Mitigation**: Promotes responsible AI development and use across the organization.
- **Innovation Catalyst**: Positions our company at the forefront of ethical AI adoption and implementation.
- **Scalable Solution**: Built to evolve with emerging AI technologies and regulations.

### Next Steps

1. **User Testing**: Engaging 50+ internal stakeholders for feedback and refinement.
2. **Continuous Improvement**: Regular updates with latest AI policy information, including recent White House briefings.
3. **Expansion**: Potential to extend the tool's capabilities to address broader AI-related queries and challenges.

This initiative demonstrates our commitment to responsible AI innovation and positions us as industry leaders in ethical AI adoption.


There appears to be important information not included in our build, for instance, the 270-day update on the 2023 executive order on Safe, Secure, and Trustworthy AI.  How might you incorporate relevant white-house briefing information into future versions? 

## Strategy for Incorporating New Governmental AI Information

### 1. Establish a Dedicated Update Team

- Form a cross-functional team responsible for monitoring, evaluating, and incorporating new AI policy information.
- Include members from legal, AI ethics, data science, and engineering departments.
- Assign clear roles and responsibilities for content curation, technical implementation, and quality assurance.

### 2. Implement an AI-Powered Content Monitoring System

- Develop or adopt an AI-based system to continuously scan official government websites, including:
  - WhiteHouse.gov
  - NIST.gov
  - AI.gov
- Configure the system to identify and flag new publications related to AI policy, ethics, and regulations.
- Set up automated alerts for the update team when new relevant content is detected.

### 3. Establish a Structured Review Process

1. **Initial Screening**:
   - Automatically categorize new content based on relevance and priority.
   - Have team members perform a quick review to confirm relevance and importance.

2. **In-depth Analysis**:
   - Assign team members to thoroughly review flagged documents.
   - Identify key points, new guidelines, or policy changes.
   - Create summaries and extract relevant quotes.

3. **Integration Planning**:
   - Determine how new information fits into the existing knowledge base.
   - Identify any conflicts with current content and plan for resolution.
   - Decide on the appropriate level of detail to include.

4. **Technical Implementation**:
   - Update the RAG system's document corpus with new information.
   - Adjust embeddings and fine-tune models if necessary.
   - Update metadata and tagging for improved retrieval.

5. **Quality Assurance**:
   - Conduct thorough testing to ensure new information is correctly integrated.
   - Verify that the system provides accurate and up-to-date responses.
   - Check for any unintended effects on existing functionalities.

### 4. Develop a Versioning and Changelog System

- Implement a versioning system for the knowledge base to track changes over time.
- Maintain a detailed changelog documenting all updates, including:
  - Date of update
  - Source of new information
  - Summary of changes
  - Impact on existing content

### 5. Create a User Communication Plan

- Develop a strategy to inform users about significant updates to the system.
- Consider implementing an in-app notification system for major policy changes.
- Provide a way for users to access both current and historical information.

### 6. Establish Partnerships and Expert Consultations

- Build relationships with AI policy experts in academia and industry.
- Consider partnering with legal firms specializing in AI and technology policy.
- Regularly consult with these experts to ensure proper interpretation and implementation of new policies.

### 7. Implement Feedback Loops

- Create mechanisms for users to provide feedback on the relevance and accuracy of AI policy information.
- Regularly review user feedback to identify areas for improvement or gaps in coverage.

### 8. Conduct Regular System Audits

- Schedule quarterly audits of the entire knowledge base to ensure consistency and relevance.
- Use these audits to identify outdated information that needs to be updated or removed.

### 9. Develop a Rapid Response Protocol

- Create a process for quickly incorporating critical updates (e.g., executive orders or urgent policy changes).
- Define criteria for triggering the rapid response protocol.
- Establish a streamlined approval process for emergency updates.

### 10. Continuous Improvement of Update Process

- Regularly review and refine the update process itself.
- Stay informed about advancements in natural language processing and information retrieval to improve the system's capabilities.


