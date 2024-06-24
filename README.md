# Multiple-Traveling-Salesmen-Problem-with-Time-Windows
## Problem Statement
In the dynamic environment of fashion retail, optimizing transportation logistics emerges as a strategy for enhancing efficiency and reducing costs.   
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

## Construction Hypothesis 
The introduction of the following set of hypotheses is strategically aligned with the goal of optimizing the transportation logistics in the context of fashion retail showroom visits, where efficiency and cost reduction are paramount. 

1. A list of brands' showroom addresses is provided, from which the travel costs i.e. average travel time can be retrieved
2. Being employees paid by hour, the unit cost of travelling i.e. distance would coincide with the unit cost of waiting, hence this reduces to the Makespan Problem with Time Window. Therefore, the ultimate objective would be just to minimize the tour duration. 
3. Buyers depart from the same starting point as their colleagues', which is the retail company they work for i.e. depot.
4. The TSPTW at hand is stated to be symmetric, setting $t_{ij} = t_{ji}$. Hence, arcs in the complete graph [Subsection *Index Sets* of *Notations*] will be undirected.
5. Brands' showrooms are considered to be non-stop i.e. an only time window will be associated to each node. 
6. Time to visit a brand showroom is measured based a worst-case scenario fashion, in order to get covered as many scenarios as possible.

## Notations
### 1. Index Sets
Let $m$ be the number of buyers within the same retail company, $n$ the number of brands’ showrooms and $G = \left ( V, A \right )$ a complete graph, such that:
- $V = \left \{ 0, 1, .., n \right \}$ is the set of the nodes i.e. brands’ showrooms;
- Node 0 is the Depot;
- $A = \left \{ \left ( i, j \right )| i\neq j, j\in V \right \}$ is the set of undirected arcs [$4^{th}$ hypothesys in Section *'Construction Hypothesis'*]. 

### 2. Parameters
- $t_{ij}$ is the travel time from the $i^{th}$ showroom to the $j^{th}$ [$4^{th}$ hypothesys in Section *'Construction Hypothesis'*];
- $d_{i}$ is the meeting duration at the $i^{th}$ showroom [$6^{th}$ hypothesys in Section *'Construction Hypothesis'*];
- $a_{i}$ is the earliest possible visit to the $i^{th}$ showroom i.e. opening hour during its working dates;
- $b_{i}$ is the latest possible visit to the $i^{th}$ showroom i.e. closing hour subtracted by its meetiong duration, during working dates.

Therefore, $\left [a_{i}, b_{i} \right]$ consists in the time window related to node $i$ [$5^{th}$ hypothesys in Section *Construction Hypothesis*].

### 3. Decision Variables
- $t_{ik}$ is the meeting time the $k^{th}$ salesperson shows up at the $i^{th}$ showroom; 
- $x_{ijk} \in \left \{ 0, 1 \right \}$ is the auxiliarity binary value. It is equals to 1 if and only if salesman $k$ travels from showroom of brand $i$ to $j$'s.

## Formulation - Integer Linear Programming [ILP]
[<span style="color:orange;">Objective</span>] Find a set of ($n$) routes that services all at minimum times i.e. time to get from  the $i^{th}$ showroom to the $j^{th}$ plus the meeting time at the $j^{th}$.   

N.B. This minimization by time will contribute to maximize the number of meetings scheduled per day.
$$ min \left (\sum_{k = 1}^{m}\sum_{i = 0}^{n}\sum_{j = 0, j\neq i}^{n}x_{ijk}\cdot t_{ij} + \sum_{k = 1}^{m}\sum_{i = 1}^{n} x_{i0k}\cdot d_{i} \right )$$  

[<span style="color:lightgreen;">Constraint 1</span>] Time window limitations
1. Triangle inequality depot w.r.t. depot
$$ \left\{\begin{matrix}
t_{ik} - t_{0} \geqslant  t_{0i}\\ 
t_{(n + 1)k} - t_{ik} \geqslant  t_{i0}
\end{matrix}\right. $$

2. (Lineralized) Triangle inequality between two consequently placed showrooms (within same salesperson's route)  
    
    Where $M > 0$ and a sufficiently large number and $y_{ij}s$ are binary variables for all arcs of A
$$ \left\{\begin{matrix}
t_{ik} - t_{jk} \geqslant t_{ij} - My_{ij}\\ 
t_{jk} - t_{ik} \geqslant t_{ij} - M\left ( 1 - y_{ij}\right )
\end{matrix}\right. $$

3. Meeting time compatibility w.r.t. opening hour
$$ \left\{\begin{matrix}
t_{ik} \geqslant a_{i}\\ 
t_{ik} + d_{i} \leqslant b_{i}\\ 
t_{ik} \geqslant 0
\end{matrix}\right. $$

[<span style="color:lightgreen;">Constraint 2</span> - BONUS not covered in the task] All buyers' routes start and end at their retail company
$$ \left\{\begin{matrix}
\sum_{j \in V: (1,j) \in A}{x}_{1j} = m & depot\_depart\\ 
\sum_{j \in V: (j,1) \in A}{x}_{j1} = m & depot\_return
\end{matrix}\right. $$    

[<span style="color:lightgreen;">Constraint 3</span>] Each brand showroom must be visited exactly once by only one buyer from each retail company
$$ \left\{\begin{matrix}
\sum_{i}^{}\sum_{k}^{}x_{ijk} = 1 & \forall j \neq depot & arriving\_buyer\\ 
\sum_{j}^{}\sum_{k}^{}x_{ijk} = 1 & \forall i \neq depot & leaving\_buyer\\ 
\sum_{i}^{}\sum_{k}^{}x_{ihk} - \sum_{j}^{}\sum_{k}^{}x_{hjk} = 0 & 
\end{matrix}\right. $$   


N.B. Last equation in the system checks whether the arriving buyier is consistent i.e. equals to the leaving one. It assures that the showroom has been visited by only one buyer from the retail company.

[<span style="color:lightgreen;">Constraint 4</span>] Subtour elimination

Being $\left | S \right | - 1 $ the number of hacks:
$$ \begin{matrix}
\sum_{ijk}^{}x_{ijk} \leqslant  \left | S \right | - 1  & \forall S\subseteq P\left ( N \right ), & depot\notin S
\end{matrix} $$

N.B. In ILP the number of subtour elimination constraints grows exponentially.

[<span style="color:lightgreen;">Constraint 5</span>]  
$$ x_{ijk}\in \left \{ 0,1 \right \} $$  

Before executing this script for the multiple Travelling Salesmen Problem with Time Windows (mTSPTW), it's essential to ensure that the number of buyers $m$ is accurately defined to match the real-world scenario you are simulating. Additionally, careful attention must be given to setting the large constant $M$. This value is used to linearize the time window constraints and should be large enough to effectively enforce the inequalities but not so large as to cause numerical instability or excessive computation times.

Setting $M$ incorrectly can lead to several issues. If $M$ is set too low, the model may not adequately enforce the triangle inequality constraints, leading to illogical solutions where the time required to travel between two locations is underestimated. Conversely, if $M$ is too high, it might lead to numerical challenges that can hamper the solver's ability to find an optimal solution, as the large coefficients can dominate the formulation, skewing the optimization process.

Therefore, determining a suitable value for $M$ should be based on the magnitude of travel times in your problem context to balance constraint enforcement with computational efficiency. 
