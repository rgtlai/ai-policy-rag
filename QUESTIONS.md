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

## 2. How did you choose your stack, and why did you select each tool the way you did?
That is a good question. There are a  number of choices for I choose Langgraph with Langchain as the overall architecture for the two agents. For the vectorstore I choose QDrant as it is an efficient, fast vectorstore that we will store the documents that have been chunked.

[Langgraph](./src/agents/output.jpeg)



## 3. What conclusions can you draw about performance and effectiveness of your pipeline with this information? We tested the performance 

Below is the table results:


## 4. How did you choose the embedding model for this application? 


The model was uploaded to https://huggingface.co/rgtlai/ai-policy-ft. The notebook that shows the training can be seen at src/sdg/Fine_Tuned.ipynb and src/sdg/Fine_Tuned2.ipynb. 

I choose the 

## 5. Test the fine-tuned embedding model using the RAGAS frameworks to quantify any improvements.  Provide results in a table. Test the two chunking strategies using the RAGAS frameworks to quantify any improvements. Provide results in a table. Which one is the best to test with internal stakeholders next week, and why

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


