# Practice Questions — Domain 2b — Model Context Protocol (part of Domain 2, 18%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **7 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 6. In MCP, who decides when a TOOL is invoked?
- A) The user
- B) The application
- C) The model
- D) The server admin

### 7. In MCP, a RESOURCE is identified by a:
- A) UUID
- B) URI
- C) Filename
- D) JSON schema

### 25. The MCP primitive controlled by the USER (slash-command style) is:
- A) Tool
- B) Resource
- C) Prompt
- D) Capability

### 26. Two valid MCP transports are:
- A) stdio and HTTP+SSE / Streamable HTTP
- B) UDP and gRPC
- C) WebSocket and FTP
- D) AMQP and stdio

### 33. Which is NOT an MCP capability the server might announce in `initialize`?
- A) tools
- B) resources
- C) sampling
- D) async-await

### 34. In MCP, "sampling" refers to:
- A) Random temperature sampling
- B) The server asking the client's model to perform an LLM call
- C) Sampling a vector from an embedding
- D) Dataset sampling for evaluation

### 56. In the MCP-to-Claude bridge, MCP tool definitions map to Anthropic's tool schema by copying:
- A) `inputSchema` → `input_schema` + `name` + `description`
- B) `inputSchema` → `output_schema`
- C) `description` → `name`
- D) `name` → `id`


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 6 | C | Phase 6 |
| 7 | B | Phase 6 |
| 25 | C | Phase 6 |
| 26 | A | Phase 6 |
| 33 | D | Phase 6 |
| 34 | B | Phase 6 |
| 56 | A | Phase 6 |
