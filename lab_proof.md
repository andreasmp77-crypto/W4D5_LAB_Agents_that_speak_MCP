# W4D5_LAB_LAB_Agents_that_speak_MCP_fluently
- Week 4 / Day 5
- Student: Andreas Papachristophorou
- Course: AI Consulting & Integration 2026-07
- Date: 2026-07-31

---

**To run the code type in your teminal.** `pyhton main.py`

**Sample Outputs saved in:** `output.pd`

---

## 1. Code / Workflow

**Files that make up the lab system**

- **ets_fuel_mcp_server.py:**
    A local MCP filesystem server that exposes only the lab_docs/ets_fueleu folder as tools. It defines three MCP tools:
    - *list_ets_documents()* – lists all ETS-related documents in the folder.
    - *read_ets_document(path)* – reads the full text of one ETS document by relative path.
    - *search_ets_documents(query, limit)* – searches across documents and returns best-matching lines with file path, line number, excerpt, and a relevance score.

- **mcp_langchain.py:** A LangChain-based agent client that:
    -Verifies and loads OPENAI_API_KEY via .env.
    -Configures MultiServerMCPClient to start ets_fuel_mcp_server.py as a stdio MCP server.
    - Calls client.get_tools() to load the ETS MCP tools into LangChain.
    - Builds an ETS voyage fields agent with create_openai_tools_agent, using those tools and a grounding-focused prompt.
    - Runs a single lab query about mandatory vs optional ETS voyage fields and prints the final answer.

- **main.py:** A simple entrypoint

### Workflow / Pipeline

```text
main.py
   ↓
mcp_langchain.py
   ↓
Load API key + create ChatOpenAI model
   ↓
Start ETS MCP server (ets_fuel_mcp_server.py)
   ↓
Load MCP tools
   ↓
Build ETS agent with grounding prompt
   ↓
Run one ETS query
   ↓
Search/read ETS documents through MCP tools
   ↓
Return final answer
```

---

## 2. Single Query

```
QUERY = Explain the difference between mandatory and optional ETS voyage fields and quote the sections that define each.
```

---

## 3. Retrieved / Tool Evidence

For the single query:

> Explain the difference between mandatory and optional ETS voyage fields and quote the sections that define each

the agent used the ETS MCP tools in the following sequence (as shown in the Tool Trace):

1. **search_ets_documents** – query: `"mandatory ETS voyage fields"`  
   - Agent log: `Invoking: search_ets_documents with {'query': 'mandatory ETS voyage fields', 'limit': 5}`  
   - Purpose: find lines in local ETS documents that talk explicitly about “mandatory ETS voyage fields”. 

2. **search_ets_documents** – query: `"optional ETS voyage fields"`  
   - Agent log: `Invoking: search_ets_documents with {'query': 'optional ETS voyage fields', 'limit': 5}`  
   - Purpose: locate text passages that describe “optional ETS voyage fields” for comparison. 

3. **read_ets_document** – path: `ETS_MRV_mandatory_vs_optional_fields.md`  
   - Agent log: `Invoking: read_ets_document with {'path': 'ETS_MRV_mandatory_vs_optional_fields.md'}`  
   - Purpose: read the full ETS note that defines mandatory vs optional voyage data fields and provides the wording the agent later quotes. 

4. **read_ets_document** – path: `ets_voyage_fields_schema_example.csv`  
   - Agent log: `Invoking: read_ets_document with {'path': 'ets_voyage_fields_schema_example.csv'}`  
   - Purpose: inspect the schema where individual voyage fields are explicitly marked as `yes` (mandatory) or `optional`, to support concrete examples. 

From these tool calls, the key pieces of evidence used by the agent are:

- **From `ETS_MRV_mandatory_vs_optional_fields.md`** (read via `read_ets_document`):  
  - A section stating that:  
    - “Mandatory fields are those that must be present in emissions reporting for ships in scope. If they are missing or incomplete, the report is likely not compliant and cannot be verified as satisfactory.”  
  - A section explaining that:  
    - “Optional or additional fields are not strictly required by the core MRV Maritime and ETS rules but are often recommended in guidance or useful for internal management.”  
  - These passages directly support the agent’s explanation of what “mandatory” and “optional” mean in ETS voyage reporting. 

- **From `ets_voyage_fields_schema_example.csv`** (read via `read_ets_document`):  
  - Rows where fields such as `ship_name` and `departure_port` are marked as `yes` (mandatory), with descriptions like “Name of the ship as recorded in the monitoring plan” and “Port where the voyage starts”.  
  - Rows where fields such as `voyage_id` and `efficiency_project_flag` are marked as optional, with descriptions like “Internal unique identifier for the voyage”.  
  - These examples are used by the agent to show concrete mandatory vs optional fields and to connect the narrative explanation back to a structured schema. 

Together, these tool outputs show that the agent’s final answer is grounded in:
- a specific ETS narrative document (`ETS_MRV_mandatory_vs_optional_fields.md`), and  
- a concrete ETS voyage fields schema (`ets_voyage_fields_schema_example.csv`),  
rather than relying only on general model knowledge.

---

## 4. Final Output (Agent Answer)

### === Final Answer ===
### Difference Between Mandatory and Optional ETS Voyage Fields

#### Mandatory Voyage Fields
Mandatory fields are those that must be included in emissions reporting for ships operating under the EU ETS and MRV rules. The absence or incompleteness of any mandatory field makes the report likely non-compliant and unable to be verified satisfactorily. 

Key elements of mandatory fields include:
- **Ship identifiers**: e.g., Ship name, IMO ship identification number, Shipping company name.
- **Voyage information**: e.g., Departure port, Departure date and time, Arrival port, and Arrival date and time.
- **Fuel and energy information**: e.g., Fuel type(s) used, Amount of each fuel Type consumed.
- **Emissions data**: e.g., CO₂-equivalent emissions for the voyage.
- **Monitoring context**: Reference to the approved monitoring plan and any data gaps.

This is detailed in the document titled **"ETS & MRV Maritime – Voyage Data Fields Overview"**, which notes:
> "Mandatory fields are those that must be present in emissions reporting for ships in scope. If they are missing or incomplete, the report is likely not compliant and cannot be verified as satisfactory."

#### Optional Voyage Fields
Optional fields, on the other hand, are not strictly required by the core MRV Maritime and ETS rules. While they may assist in internal management, operational efficiency, or other regulations, omitting them does not result in non-compliance.

Examples of optional fields include:
- Operational details (e.g., Speed profiles, Weather conditions).
- Commercial and cargo information broader than minimum requirements.
- Internal KPIs and benchmarks.

From the same document, it is emphasized:
> "Optional or additional fields are not strictly required by the core MRV Maritime and ETS rules but are often recommended in guidance or useful for internal management."

### Supporting Evidence
From **"ets_voyage_fields_schema_example.csv"**, some mandatory fields include:
- `ship_name,ship_id,yes,Name of the ship as recorded in the monitoring plan..."`
- `departure_port,voyage,yes,Port where the voyage starts..."`

An example of an optional field is:
- `voyage_id,voyage,optional,Internal unique identifier for the voyage..."`

In summary, mandatory fields are crucial for compliance and verification, while optional fields enhance reporting and operational insights but are not required for compliance.
Run completed successfully.

---

## 5. One Failure or Limitation

One limitation of this setup is that the agent can still produce a plausible-sounding answer even if the evidence is weak, incomplete, or not perfectly matched to the query. For example, if `search_ets_documents` returns only partial excerpts or misses an important section, the agent may still summarize the ETS voyage fields confidently without fully proving the distinction from the source files. 

A second limitation is that the search tool is simple and keyword-based, so it may miss relevant content if the wording in the document is different from the query. That means the agent might rely on the wrong excerpt or give an answer that is not fully supported by the documents. 

To reduce this risk, I would:
- Require the agent to quote the exact source line or excerpt before making a claim.
- Make the agent say “insufficient evidence” when the tools do not return a strong match.
- Improve the search logic or add better document structure for ETS notes.
- Introduce more tool and connection to more sources via MCPs

---