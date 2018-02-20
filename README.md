# Car-pool-algorithm
This project designed a min matching algorithm to match riders requesting carpool in Manhattan in order to save total travel distance.

## Min Matching algorithm
We formed an undirected graph with nodes represent passengers and edges represent their sharing plan. Using maximum matching with minimum weight algorithm, we can find the best sharing plan with the minimum total distance.

### Distance between passengers
Based on Manhattan distance (𝑋(𝑥1, 𝑥2), 𝑌(𝑦1, 𝑦2), 𝑑(𝑋, 𝑌) = |𝑥1 − 𝑦1| + |𝑥2 − 𝑦2|), we defined the distance between each two passengers 𝑑(𝑋, 𝑌)1 in five scenarios:

<br />a. Pick up 𝑋 then pick up 𝑌 then drop off 𝑋 then drop up 𝑌: 
<br />➢ 𝑑(𝑋𝑌)=𝑑(1)=𝑑(𝑋1𝑌1)+𝑑(𝑌1𝑋2)+𝑑(𝑋2𝑌2)
<br />b. Pick up 𝑋 then pick up 𝑌 then drop off 𝑌 then drop up 𝑋:
<br />➢ 𝑑(𝑋𝑌)=𝑑(2)=𝑑(𝑋1𝑌1)+𝑑(𝑌1𝑌2)+𝑑(𝑌2𝑋2)
<br />c. Pick up 𝑌 then pick up 𝑋 then drop off 𝑋 then drop up 𝑌: 
<br />➢ 𝑑(𝑋𝑌)=𝑑(3)=𝑑(𝑌1𝑋1)+𝑑(𝑋1𝑋2)+𝑑(𝑋2𝑌2)
<br />d. Pick up 𝑌 then pick up 𝑋 then drop off 𝑌 then drop up 𝑋:
<br />➢ 𝑑(𝑋𝑌)=𝑑(4)=𝑑(𝑌1𝑋1)+𝑑(𝑋1𝑌2)+𝑑(𝑌2𝑋2) 
<br />d.𝑋 and 𝑌 travels on his/her own:
<br />➢ 𝑑(𝑋𝑌)=𝑑(5)=𝑑(𝑋1𝑋2)+𝑑(𝑌1𝑌2)

### Level of service
Passengers are not pooling with someone if the total travel distance he spends on a shared vehicle will exceed 25% more then traveling on his/her own. We call it “level of service” to guarantee the quality of vehicle sharing.


For passenger(𝑋):
<br />if 𝑑(𝑋1𝑌1)+ 𝑑(𝑌1𝑋2)>1.25𝑑(𝑌1𝑋1):
<br /> set 𝑑(1) as +∝
<br />if 𝑑(𝑋1𝑌1)+ 𝑑(𝑌1𝑌2)+ 𝑑(𝑌2𝑋2)>1.25𝑑(𝑌1𝑋1): 
<br />set 𝑑(2) as +∝
<br />if 𝑑(𝑋1𝑌2) + 𝑑(𝑌2𝑋2) > 1.25𝑑(𝑌1𝑋1):
<br />set 𝑑(4) as +∝

<br />Repeat it for all passengers and output all the distance. The weight of two passengers is defined as:
<br />𝑑(𝑋𝑌) = min{𝑑(1), 𝑑(2), 𝑑(3), 𝑑(4), 𝑑(5)}.

### Min Matching
After defining all the weight of edges, we formed a complete graph to represent passengers and their best way of pooling with each other.

As shown in the figure below, there are four passengers 𝐴, 𝐵, 𝐶 and 𝐷 with weights and way of pooling marked on edges. The maximum matching of all passengers with a minimum total weight is pair 𝐴 with 𝐷 using scenario 1 and pair 𝐵 with 𝐶 using scenario a.

![alt text](https://github.com/Melody-Meng/Car-pool-algorithm/blob/master/figure1.png)
