# covid-networkx

https://pybluepanda.github.io/covid-networkx/

## NetworkX COVID SEAIR simulation model

- S (Susceptible): Healthy, but can become exposed.  
- E (Exposed/Latent): Infected but not yet contagious (incubation period).  
  - Latent Phase: Nodes enter an E state (exposed but not infectious).  
- A (Asymptomatic): Infectious but without symptoms (~30% cases).  
  - Asymptomatic Spread: 30% of cases stay A (asymptomatic but contagious).
- I (Symptomatic Infected): Infectious & symptomatic.  
  - Weighted Infection Risk: More infected neighbors → higher transmission risk. 
- R (Recovered): Immune after recovery.  
  - Recovery: Infected individuals move to R (Recovered) after 7 days.
