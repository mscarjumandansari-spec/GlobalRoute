#### 🌐 GlobalRoute : Cross-Border Multi-Modal & Tariff Optimization System

**Quantitative Decision-Support Platform for Geopolitical Corridor Routing, EU CBAM Carbon Valuation & Working Capital Efficiency.** 

[](YOUR_VIDEO_LINK_HERE)
[](docs/GlobalRoute_WhitePaper.pdf) 

#### Executive Overview

Traditional supply chain optimizers minimize base freight rates—ignoring up to **70% of true landed costs** during geopolitical shocks. **GlobalRoute v3.0** models China–Europe export corridors across four simultaneous dimensions: 

1. **True Landed Cost Engine:** Integrates base freight, bilateral customs tariffs, **EU CBAM Scope 3 carbon pricing**, and **working capital inventory lockup**.
2. **360° Interactive Corridor Globe:** Visualizes multi-modal trade routes (Direct Sea, China-Europe BRI Rail, Dubai Free-Zone Sea+Air, Direct Air) and dynamic maritime chokepoint detours (Red Sea / Cape of Good Hope).
3. **Belt & Road (BRI) Break-Even Sensitivity:** Identifies the exact tariff inflection points where overland CR Express and bonded hubs outperform disrupted ocean shipping.
4. **Enterprise CSV Ingestion:** Allows procurement teams to upload custom carrier rate cards and export auditable boardroom reports.

 

#### Mathematical Formulation

True Landed Cost (

Ctotalcap C sub total end-sub
𝐶total
⁠) is evaluated across freight (F), cargo value (

Vcargocap V sub cargo end-sub
𝑉cargo
⁠), effective tariff (τ), Scope 3 carbon emissions (E), EU CBAM carbon price (

PCBAMcap P sub CBAM end-sub
𝑃CBAM
⁠), and cost of capital (

rcapr sub cap end-sub
𝑟cap
⁠): 

Ctotal=(Funit⋅Q)+(Vcargo⋅τ100)+(Eunit⋅Q1000⋅PCBAM)+(Vcargo⋅rcap⋅T365)cap C sub total end-sub equals open paren cap F sub unit end-sub center dot cap Q close paren plus open paren cap V sub cargo end-sub center dot the fraction with numerator tau and denominator 100 end-fraction close paren plus open paren the fraction with numerator cap E sub unit end-sub center dot cap Q and denominator 1000 end-fraction center dot cap P sub CBAM end-sub close paren plus open paren cap V sub cargo end-sub center dot r sub cap end-sub center dot the fraction with numerator cap T and denominator 365 end-fraction close paren
𝐶total=(𝐹unit⋅𝑄)+𝑉cargo⋅𝜏100+𝐸unit⋅𝑄1000⋅𝑃CBAM+𝑉cargo⋅𝑟cap⋅𝑇365
 

Metrics are normalized via **Dimensionless Max-Normalization** onto a 
[

0

,

1

]
⁠ penalty scale before applying executive priority weights. 

 

#### Quick Start

bash

git clone https://github.com/YOUR_USERNAME/GlobalRoute.git
cd GlobalRoute
pip install streamlit pandas numpy plotly
python -m streamlit run app.py

Use code with caution.

Copy code text to clipboard.