# Problem Definition — Accessibility of Job Centers via P+R in Luxembourg

## 1. Problem Statement

Luxembourg City is experiencing increasing traffic congestion driven by population growth and a high volume of cross-border commuters traveling primarily by private car. This congestion is particularly pronounced in areas with high employment density, where demand for access is greatest.

Commute time is a critical determinant of job accessibility. Under peak-hour conditions, long and unreliable travel times reduce access to employment opportunities and contribute to inefficiencies in the transport system.

Park-and-Ride (P+R) infrastructure is designed to mitigate congestion by enabling commuters to switch from private vehicles to public transport at the urban periphery. However, the effectiveness of existing P+R facilities in providing efficient access to major employment centers is not well understood.

This project aims to evaluate the accessibility of high-employment-density business districts from existing P+R facilities using public transport, in order to identify spatial gaps and inform future transport planning decisions.

---

## 2. Analytical Question

How long does it take for a commuter, starting from a P+R facility, to reach high-employment-density business districts using the public transport network (bus and tram) during peak hours?

Accessibility will be measured using frequency-weighted travel times.

---

## 3. Method Overview

### 3.1 Scope and Assumptions

This analysis focuses on cross-border commuters entering Luxembourg City.

* Commuters travel by car to P+R facilities (external travel time is assumed to be 30–45 minutes but is not explicitly modeled)
* From the P+R onward, commuters rely exclusively on:

  * Bus
  * Tram
  * Walking
* Travel occurs during peak commuting hours
* The transport network is modeled as a **static network**

---

### 3.2 Network Modeling

A network-based accessibility analysis will be conducted using the AVL public transport network, including:

* Bus routes
* Tram lines
* Walking connections
* Transfer waiting times
* Service frequency (used to compute frequency-weighted travel times)

Travel times will be calculated using frequency-weighted shortest path methods.

---

### 3.3 Spatial Representation

* **P+R locations**: All major facilities, digitized as point features
* **Spatial units**: City quarters (polygon level)
* **Destination representation**: Each business district is represented by a primary public transport stop within its corresponding quarter

---

### 3.4 Business District Definition

Business districts are defined using employment data from STATEC.

The process is as follows:

* Employment density is calculated as jobs per unit area (jobs/km²)
* Spatial units are ranked by employment density
* The highest-density areas are identified
* The top three employment density clusters are selected
* Adjacent high-density units are aggregated to form continuous business district zones

This ensures a data-driven and reproducible identification of major employment centers.

---

### 3.5 Accessibility Metric

* Accessibility is measured using **frequency-weighted travel time**
* Waiting times and transfers are explicitly included
* Isochrone thresholds are defined at:

  * 15 minutes
  * 20 minutes
  * 30 minutes
  * 45 minutes

---

## 4. Expected Outputs

The analysis will produce:

* A map of P+R facilities and identified business districts
* Isochrone maps (15, 20, 30, 45 minutes) for each P+R location
* A travel time matrix between P+R facilities and business districts
* Identification of business districts with the highest average travel times (i.e., lowest accessibility)

---

## 5. Assumptions and Limitations

* P+R facilities are assumed to be directly connected to nearby public transport stops
* The transport network is modeled as static and does not account for temporal variability
* Public transport speeds are approximated using average values
* Transfer waiting times are included but simplified
* Business districts are represented by a single primary stop, introducing spatial generalization bias
* The analysis focuses on commuters entering from the west and south, reflecting the distribution of P+R infrastructure
* Standard parking options within the city are not considered

---

## 6. Success Criteria

A successful analysis will:

* Identify business districts with the highest travel times from P+R facilities
* Reveal spatial inequalities in accessibility across Luxembourg City
* Highlight gaps in the current P+R and public transport system
* Provide insights that can be compared with national mobility strategies (e.g., NPM 2035)

---

## 7. Scope

### Included

* Public transport accessibility from P+R facilities
* Peak-hour commuting conditions
* Cross-border commuter flows
* Network-based travel time analysis

### Excluded

* Job quality, salary, or employment type
* Full door-to-door commute modeling outside the P+R system
* Real-time or dynamic traffic modeling
* Behavioral decision-making beyond modal shift at P+R facilities

