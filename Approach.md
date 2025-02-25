📝 **The Challenge**

---
Designing and implementing a solution to extract addresses from PDF documents. The solution:

- Identifies and extracts physical addresses
- Records the page number of each address
- Handle various document formats and layouts
- Associates extracted addresses with relevant entities
---

I used a **RAG-based approach** to address the problem, implementing an efficient chunking mechanism to segment the documents. For each chunk, I extracted and stored the **page number** in the metadata for better retrieval. To enhance retrieval accuracy, I **augmented the query** with **keywords** (extracted using **RAKE**) and **cities** (identified through **LocationTagger**).

---

### ❌ **Methods Attempted but Ineffective:**

- Initially, I experimented with multiple **NER models** to extract location-related entities. However, these models produced numerous **false positives and negatives**, affecting accuracy.
- I then attempted to use **NER results as metadata** for ChromaDB chunks to filter results during retrieval. Unfortunately, due to the **inaccurate NER outputs**, the retrieved chunks were **irrelevant**.
- Lastly, I tried **augmenting ChromaDB queries with NER results**, but the retrieval **accuracy remained low** due to persistent noise in the entity recognition.

---

### **Final Approach – RAG with Augmented Queries**

- **Key Techniques:**
    - **Location extraction** and **keyword extraction** were combined to improve retrieval accuracy, ensuring the **scalability** of LLM usage.

---

### **Breaking Down the Problem**

I divided the problem into the following **phases**:

1. **Reading the PDF**
2. **Chunking the PDF**
3. **Storing the Chunks**
4. **Querying the Vector DB**
5. **Generating Answers via LLM**

---

### **Phase 1: Reading the PDF**

**Tools Explored:**

- `PyPDF2`
- `PyPDFLoader (Langchain)`
- `PyMuPDF4LLM`
- `Docling`

**Final Choice:** **Docling -**  I found it provides a more **accurate Markdown representation**, which significantly helped with better document chunking.

---

### **Phase 2: Extracting Key Information**

### **Techniques Used:**

- **Keyword Extraction:**
    - Tried: `RAKE`, `YAKE`, `TF-IDF`
    - **Final Choice:** **RAKE** — I found that tf-idf and YAKE didn’t give accurate results on the documents. tf-idf focuses too much on specific words while RAKE focuses more on longer phrases — this helped with retreival.
    - I used RAKE on the entire document which gave me a list of important keywords. I used these keywords while querying the database to get a better match of chunks.
- **Named Entity Recognition (NER):**
    - Tried various models from **Hugging Face 🤗**
    - **Final Choice:** **SpaCy** — best performance for **GPE/LOC** extraction — other models like bert-addresses, bert-base-NER etc were unable to detect addresses in the documents.
    - I used NER for every chunk before storing it into the DB. I attempted to use it to store a list of important location-related entities as metadata for the chunk, however the results of the NER were not as good. Therefore, I simply created a boolean variable in the metadata of each chunk indicating the presence of a location-related entity.
- **Location Extraction:**
    - **Final Choice:** **LocationTagger** — outperformed NER - used it for augmenting vector DB queries.
    - Similar to RAKE, i used cities detected by LocationTagger to augment the query used to get matching chunks from ChromaDB. This helped get all address-related chunks.

---

### **Phase 3: Vector DB & Chunking Strategy**

### **Database: ChromaDB**

- I used ChromaDB for the assignment, since it’s free and langchain supports it well. Also, I have some experience working with it.
- **I** stored all the documents in a single chromaDB collection**:**
    - Reduced overhead of multiple collection queries.
    - Leverages **metadata filtering** to retrieve chunks belonging to a **specific document**.

### **Metadata Structure**

Each chunk is stored with the following metadata:

```json
{
  "doc_name": "",       // Document name
  "pages": [],          // Pages where the chunk appears
  "chunk_id": "",       // Unique identifier for each chunk
  "location": true/false // Flag indicating presence of location entities
}
```

---

### **Chunking Strategy: Optimized for Scalability**

### **Step-by-Step Breakdown**

### **1. Extract Markdown Headings for Logical Segmentation**

- Legal documents are inherently structured. By splitting text at **Markdown headings** (`#`etc.), I tried to ensure:
    - **Chunks represent coherent sections** (clauses, articles, sub-sections).
    - Reduces chances of splitting mid-context, which can affect downstream information retrieval.

### **2. Dynamic Chunk Merging Based on Token Limit**

- **Not a fixed-size chunking approach -** My approach merges consecutive headings/sections as much as possible without exceeding the token limit.
- **Why this is effective:**
    - **Maximizes context per chunk** without exceeding the model’s input limit.
    - **Improved retrieval performance:** Larger, context-rich chunks rank higher during semantic search.

### **3. Token-Based Splitting with Overlap for Extra-Long Sections**

- If a merged section **exceeds the token threshold (300 tokens)**:
    - It’s **split** using a **token-based splitter**.
    - **Overlap** of 10% between adjacent chunks ensures no context breaks mid-thought or mid-sentence.

### **4. Mapping Chunks to Pages**

- Each chunk is **mapped to its originating page(s)** in the document.
- When users ask for specific information, results come with **page references**.

### 5. **Storing Optimized Chunks in ChromaDB**

- Each final chunk is embedded using **all-mpnet-base-v2** for semantic similarity search.
- Stored along with its **metadata** in a single ChromaDB collection.

This chunking approach **balances scalability, context preservation, and retrieval precision**

---

### **Phase 4: Querying the Vector DB**

### **Query Augmentation:**

Simple queries to the DB did not result in retrieval of relevant chunks. Hence, I decided to augment the query by adding some document specific words to it. This would help retreive entity or location specific chunks.

- Used **LocationTagger’s** `place_entity` extraction. — since the query now contains potential cities from the document itself, ChromaDB returns relevant chunks
- Added **RAKE** keywords + domain-specific terms (e.g., “address,” “location”). — RAKE keywords consist of names of the companies/partners involved in the agreement. This results is entity-related chunks to be prioritised. The assumption here is that in such legal documents, it is unnatural for addresses to be mentioned without reference to the associated entity itself.

---

### **Phase 5: LLM Integration**

- Retrieved **top 10 closest chunks** from **ChromaDB**.
- Prompted LLM to extract **all physical addresses** along with their **page numbers** from the retreived chunks.

---