# ETS & MRV Maritime – Voyage Data Fields Overview

This document summarizes, in simple terms, the types of data fields that shipping companies report for EU ETS and MRV Maritime, and distinguishes between fields that are legally mandatory and fields that are optional or supporting.

The focus is on **voyage-level** and **annual** emissions reporting for ships in scope of MRV Maritime and EU ETS. It is written as a practical working note to support internal compliance and AI experiments, not as a legal interpretation.

## Mandatory Voyage Reporting Fields (ETS/MRV)

Mandatory fields are those that must be present in emissions reporting for ships in scope. If they are missing or incomplete, the report is likely not compliant and cannot be verified as satisfactory.

Typical mandatory data elements include:

- **Ship identifiers**
  - Ship name
  - IMO ship identification number
  - Shipping company name
  - Company IMO unique company and registered owner identification number

- **Voyage information**
  - Departure port
  - Departure date and time
  - Arrival port
  - Arrival date and time
  - Whether the voyage is in ETS scope (e.g. between EU ports or to/from EU ports)
  - Distance travelled for the voyage, using the defined methodology

- **Fuel and energy information**
  - Fuel type(s) used (e.g. HFO, MDO, MGO, LNG, biofuels)
  - Amount of each fuel type consumed for the voyage
  - Monitoring method applied (e.g. Methods A–D in the MRV Maritime Regulation, such as bunker delivery notes or flow meters)
  - Emission factors used for each fuel type, following the relevant rules

- **Emissions data**
  - CO₂-equivalent emissions for the voyage
  - Aggregated annual emissions per ship
  - Any additional gases covered by the scope where relevant

- **Monitoring and reporting context**
  - Reference to the approved monitoring plan (MP)
  - Information on any data gaps and the methodology used to close them
  - Indication that data completeness and accuracy principles have been applied

These fields support the verifier in checking completeness, accuracy and reliability of the reported data and are fundamental for ETS and MRV compliance.

## Optional or Additional Voyage Fields

Optional or additional fields are not strictly required by the core MRV Maritime and ETS rules, but are often recommended in guidance or useful for internal management, efficiency analysis, or other regulations.

Examples of optional or supporting fields include:

- **Operational details**
  - Speed profiles
  - Weather or route conditions
  - Details of operational efficiency projects (e.g. hull cleaning, propeller upgrades)

- **Commercial and cargo information beyond minimum requirements**
  - Detailed cargo categories beyond what is required for transport work
  - Additional passenger breakdowns or service categories

- **Advanced fuel and sustainability information**
  - Internal references for sustainability certificates of alternative fuels
  - Additional notes on renewable content, RFNBOs, RCFs, or SLCFs beyond what is required to zero-rate emission factors

- **Internal KPIs and benchmarks**
  - Company-specific efficiency metrics
  - Internal ratings or risk indicators that are not mandated by MRV or ETS

These fields can help companies optimize operations, support other reporting frameworks, and provide richer context, but omission of these additional fields does not automatically mean non-compliance, as long as mandatory data are complete and correct.

## Difference Between Mandatory and Optional Fields

In practice, the difference between mandatory and optional fields can be summarized as:

- **Mandatory fields**
  - Required for legal compliance with MRV Maritime and EU ETS.
  - Needed for the verifier to reach a reasonable level of assurance that the emissions report is free from material misstatements.
  - Directly linked to core principles such as completeness, accuracy, and reliability.
  - Missing or incorrect mandatory fields can lead to non-conformities and a “not verified” opinion.

- **Optional or additional fields**
  - Useful for better understanding, management and optimization, but not strictly required for verification of the emissions report under MRV/ETS.
  - More likely to be relevant to recommendations for improvement or internal KPIs rather than core compliance.
  - Their absence usually does not, on its own, prevent verification, provided that all mandatory fields are correctly reported.

When designing data schemas or AI systems around ETS/MRV reporting, mandatory fields should be treated as **hard requirements** for compliance and verification, while optional fields can be considered **enhancements** that improve insight and robustness but may be implemented progressively over time.