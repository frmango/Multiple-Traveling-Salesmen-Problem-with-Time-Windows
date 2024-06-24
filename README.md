# Multiple-Traveling-Salesmen-Problem-with-Time-Windows
## Problem Statement
In the environment of retail, optimizing transportation logistics emerges as a strategy for enhancing efficiency and reducing costs.   
The transportation problem focuses on minimizing costs and itinerary time for two distinct groups involved in showroom appointments: buyers and salespeople.     

<span style="color:lightyellow;">Buyers</span> from prominent retail companies navigate through the city to attend 6-8 meetings daily across various locations during the fashion week season. Their primary objectives are to:
1. streamline their routes effectively;
2. adjust in real-time to traffic; 
3. strategically cluster meetings within proximate areas to maximize productivity.  

<span style="color:lightyellow;">Salespeople</span> representing elite brands must:
1. efficiently calculate travel times
2. adapt to unforeseen schedule changes due to external events e.g. cancellations
3. organize their meetings to optimize their daily schedule, which translates into reducing operational costs.   

By addressing these tailored needs through refined transportation strategies, companies can significantly bolster profitability and operational efficacy.

## Algorithm Rationale
The rationale behind the development of the algorithm begins with the reducibility theorem and the foundational concept of the Traveling Salesman Problem (TSP), where the objective is to find the shortest possible route that visits a set of locations exactly once and returns to the origin point. Extending this problem to accommodate scenarios where there are multiple buyers, each responsible for covering distinct sets of showrooms without overlap with their colleagues, the problem evolves into the Multiple Traveling Salesmen Problem (mTSP). This adaptation distributes the workload among several agents, thereby complicating the route optimization process due to the introduction of parallel operational constraints.  

Further complexity is introduced with the integration of specific time windows for each showroom, turning the problem into the Multiple Traveling Salesmen Problem with Time Windows (mTSPTW). Each showroom, treated as a node in the problem, has an associated single time window characterized by a predefined opening and closing time. The algorithm must, therefore, not only determine the optimal route for each buyer to minimize travel time and distance but also synchronize these routes with the operational schedules of the showrooms. This synchronization ensures that each buyer arrives at each showroom within the permissible time window, making the problem both a routing and a scheduling challenge. The inclusion of time windows adds a layer of temporal constraints that requires the algorithm to balance between spatial efficiency and time-specific feasibility, thus significantly enhancing the complexity and practical relevance of the solution.

## Before executing 
It is essential to ensure that the number of buyers $m$ is accurately defined to match the real-world scenario you are simulating. Additionally, careful attention must be given to setting the large constant $M$. This value is used to linearize the time window constraints and should be large enough to effectively enforce the inequalities but not so large as to cause numerical instability or excessive computation times.

Setting $M$ incorrectly can lead to several issues. If $M$ is set too low, the model may not adequately enforce the triangle inequality constraints, leading to illogical solutions where the time required to travel between two locations is underestimated. Conversely, if $M$ is too high, it might lead to numerical challenges that can hamper the solver's ability to find an optimal solution, as the large coefficients can dominate the formulation, skewing the optimization process.

Therefore, determining a suitable value for $M$ should be based on the magnitude of travel times in your problem context to balance constraint enforcement with computational efficiency. 
