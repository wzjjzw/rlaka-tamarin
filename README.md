# RLAKA: Tamarin Formal Verification
This repository contains the complete Tamarin model for the RLAKA protocol,
a lightweight PUF-based authentication and key agreement protocol for 
resource-constrained smart home environments.
## Contents
- `rlaka.spthy` - Complete Tamarin model (13 security properties verified)
## Requirements
- Tamarin 1.12.0
- Maude 3.5.1
## Quick Start
```bash
tamarin-prover rlaka.spthy --prove --bound=9 --derivcheck-timeout=0
