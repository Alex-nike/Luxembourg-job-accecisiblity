Problem Statement:

With the population of Luxembourg City rising and the number of cross-border communters coming in by car, there is a lot of traffic in the city and importanly near business districts. 
The commute time is a large factor in choosing a job, esepcially in traffic heavy condtions, thefore the use of P+R stops can reduce traffic.
Therefore, finding the places which have the longest commute time, by bus, is imperative to undertanding where to put future P+R stops.

Analytical question:
Starting from a P+R stop, how long does it take someone to get from there to one of the business districts, using the AVL network, including the tram?

Method Overview:
To answer this question, we will assume that the average person commutes 30-45 minutes, across the border, to one of the major P+R stops that the city provides. The P+R stops used wiht have P+R in the name and placed digitally. 
We assume that once the individual reaches the P+R stops, they only walk or use the Bus and Tram  Network to get to their destination. The first stop in the given Luxembourg city quater will be used in this analysis.
This question concerns cross-border commuters.

In terms of quantifiable data, network analysis will be used to emasure the average travel time from the P+R stop to the first stop they reach within the quater. This includes walking and bus transfers.
To do this, freqency weighted bus netwokr data is used. A static traffic netowrk at peak hours as well as a traffic level to average speed table will be used to find travel time.

Expected output:
There will be two maps which first locate the P+R stops and then the business distrcits. From here, there will be tables detailing the average travel time for each buisness district as well as an isochrone map for each P+R stop.
THis Isochrome will range from 15,20,30, and 45 minutes

Limitations:
We assume the P+R stop is right next to the bus station. We must also assume that the bus speed scales with traffic. The average traffic will be taken and a estimated average spped table will be used to map traffic to avergae speed.
We assume commuters come from the west or south since the majority of P+R stops are around that area of the city. We disregard normal parking lots. There is bias with the first stop method as well.
We can use the isochrone map to get a better estimate but we can't get too precise.

A good result will allows us to see which business districts are currently inaccessible using the P+R stops. I will compare the results with the NPM 2035 which is a plan from the goverment regarding mobility.
