## python main.py

python main.py
Starting ETS MCP lab agent...
Setup OK: OPENAI_API_KEY loaded and local ETS MCP client created.
Local source folder: C:\Users\andre\Documents\IronHack\ACFT_2026_Course\W4D5_LAB_LAB_Agents_that_speak_MCP_fluently\W4D5_LAB_Agents_that_speak_MCP\lab_docs\ets_fueleu
Loading MCP tools from the local server...
Loaded 3 MCP tools from the local ETS server
 - list_ets_documents: List all documents available in the local ETS folder....
 - read_ets_document: Read one local ETS document by relative path....
 - search_ets_documents: Search local ETS documents for a string query and return matching excerpts....

### === Query ===
Explain the difference between mandatory and optional ETS voyage fields and quote the sections that define each

Running agent on the ETS query...

### === Tool Trace ===

Step 1
Tool: search_ets_documents
File: mandatory ETS voyage fields
Agent log: Invoking: `search_ets_documents` with `{'query': 'mandatory ETS voyage fields', 'limit': 5}`

Step 2
Tool: search_ets_documents
File: optional ETS voyage fields
Agent log: Invoking: `search_ets_documents` with `{'query': 'optional ETS voyage fields', 'limit': 5}`

Step 3
Tool: read_ets_document
File: ETS_MRV_mandatory_vs_optional_fields.md
Agent log: Invoking: `read_ets_document` with `{'path': 'ETS_MRV_mandatory_vs_optional_fields.md'}`

Step 4
Tool: read_ets_document
File: ets_voyage_fields_schema_example.csv
Agent log: Invoking: `read_ets_document` with `{'path': 'ets_voyage_fields_schema_example.csv'}`

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


## python ets_fuel_mcp_server.py

ETS MCP server ready for folder: C:\Users\andre\Documents\IronHack\ACFT_2026_Course\W4D5_LAB_LAB_Agents_that_speak_MCP_fluently\W4D5_LAB_Agents_that_speak_MCP\lab_docs\ets_fueleu
Waiting for MCP client requests...

---

## python mcp_langchain.py

Setup OK: OPENAI_API_KEY loaded and local ETS MCP client created.
Local source folder: C:\Users\andre\Documents\IronHack\ACFT_2026_Course\W4D5_LAB_LAB_Agents_that_speak_MCP_fluently\W4D5_LAB_Agents_that_speak_MCP\lab_docs\ets_fueleu
Loading MCP tools from the local server...
Loaded 3 MCP tools from the local ETS server
 - list_ets_documents: List all documents available in the local ETS folder....
 - read_ets_document: Read one local ETS document by relative path....
 - search_ets_documents: Search local ETS documents for a string query and return matching excerpts....

=== Query ===
Explain the difference between mandatory and optional ETS voyage fields and quote the sections that define each

Running agent on the ETS query...

=== Agent answer ===
In the context of ETS (Emissions Trading System) and MRV (Monitoring, Reporting, and Verification) for maritime transport, fields in voyage reporting are categorized into mandatory and optional types.

### Mandatory Voyage Reporting Fields
Mandatory fields are those that must be present for compliance with emissions reporting. If any of these fields are missing or incorrect, the report cannot be verified as satisfactory. Typical mandatory data elements include:

1. **Ship Identifiers**
   - Ship name
   - IMO ship identification number
   - Shipping company name
   - Company IMO unique company and registered owner identification number

2. **Voyage Information**
   - Departure port
   - Departure date and time
   - Arrival port
   - Arrival date and time
   - Indication whether the voyage is in ETS scope (e.g., between EU ports)
   - Distance travelled for the voyage

3. **Fuel and Energy Information**
   - Fuel types and amounts consumed
   - Monitoring methods applied
   - Emission factors used

4. **Emissions Data**
   - CO₂-equivalent emissions for the voyage
   
5. **Monitoring and Reporting Context**
   - Reference to the approved monitoring plan (MP)

These fields are essential for verifiers to check the completeness, accuracy, and reliability of reported data, thereby directly linking to core compliance principles (ETS & MRV Maritime, *Mandatory Voyage Reporting Fields*).

### Optional or Additional Voyage Fields
Optional fields, while beneficial for internal management and reporting enhancements, are not legally required for compliance. Their absence won't lead to automatic non-compliance as long as mandatory data are complete. Examples of optional fields include:

- **Operational Details**
  - Speed profiles
  - Weather conditions

- **Advanced Fuel and Sustainability Information**
  - Internal references for sustainability certifications

- **Internal KPIs and Benchmarks**
  - Company-specific efficiency metrics

These optional fields can help optimize operations and provide richer context, facilitating better management and analysis (ETS & MRV Maritime, *Optional or Additional Voyage Fields*).

### Summary of Differences
In summary, mandatory fields are legally required for compliance and necessary for proper verification, while optional fields enhance reporting and analysis but are not essential. Missing mandatory fields can lead to non-compliance, whereas optional fields do not affect compliance as long as mandatory fields are correctly reported (*ETS & MRV Maritime – Voyage Data Fields Overview*). 

In addition, from the data schema example, mandatory fields are explicitly marked with "yes" (e.g., ship_name, departure_port) while optional fields are marked as such (e.g., voyage_id, efficiency_project_flag), underscoring their differing levels of necessity in reporting (from the *ets_voyage_fields_schema_example.csv* file).