# User Story Scheduler  
  
### Instructions  
- The assignment is developed in groups of minimum 2 and maximum 3 students.  
- Use a repository on GitHub or similar to store the files for your assignment.  
- You must upload the repository compressed in zip as well as the URL of the repository.  
- It is recommended to elaborate the documentary part using a GitHub repository and markdown files.  
  
### Table of contents  
1. Description of the problem to be solved  
2. Motivation to solve the problem  
3. Approach and examples of the search space
4. Solution space approach and examples  
5. Representation implementation using a programming language  

### Programmers
- Francesco Bassino u201816669
- Cesar Mosqueira u201910750
- Renzo Mondragón u201415624


## 1. Description of the problem to solve
Nowadays, the Agile methodology is one of the most used by several companies in different sectors.  
The main advantages of Agile are:  
**1. Improves quality:** Minimizes errors in deliverables and improves customer experience and functionality.  
**2. Increased engagement:** Improves employee satisfaction and generates team awareness.  
**3. Speed:** Shorten production cycles and minimize reaction and decision making times.  
**4. Increased productivity:** By allocating resources better and more dynamically, production improves according to the company's priorities.  

#### User Story Definition  
  
To define _User Story Mapping_ in English, we must first start from the notion of the _user story_. This refers to the user's narrative or expectations of the product and the clear representation of them, based on information such as:  
  
- Identification 
- prioritization
- estimation of the volume of work required 
- demonstration
- complementary observations
  
#### _User Story Mapping_: objective  
  
In this sense and in order to carry out this representation, we speak of _story mapping_ or user story mapping. From this, the expertise of the Product Owner and the information he has collected from his customers, is organized and presented in a clearer way. For example:  

"As a [type of user], I would like to have [this functionality] with which I can benefit [in this way]."

![image](https://user-images.githubusercontent.com/54272736/194406376-46012a63-b69a-47b3-9ac3-c33bdfebfe29.png)

There are times when you have a lot of user stories that need to be done in a period of time. You also have a limited amount of developers who can do the task and many have priority other the other ones (for example time).

The Scrum Muster (or Product Owner) may assign the tasks in the order they believe is the best (according to the client or de General Manager) but it is not necesarly the best way and the most efficient way posible to do it


## 2. Motivation to solve the problem  
We are just about to finish college and already having experience doing various jobs with my colleagues (university jobs and with clients), to organize the execution of these projects, plan strategies and, above all, see the tasks we have to do and see their priorities is a complicated task when the client wants to see progress over the weeks. 

Having a tool that allows us to see which is the best way to organize the user stories in an efficient way, would help us to be able to organize ourselves more clearly throughout the project and finish the deadlines before the date or at least on time.  Also, to explain the client how are we going to setup the priorities so he can clearly understand the prosses and view all the project in the big picture.


## 3. Approach and examples of the search space
The search space for this problem would be the ways that the user stories can be aranged. Since this is a combinatorial problem, there are exponential answers for this problem. The approach we're taking to optimize the iteration through some of them to get the best solution in the search space is a genetic algorithms. This will allow us to randomly select `N` solutions or so called `genomes` and store them in an array (`population`). The idea is to improve this population by using the algorithm which will be further detailed in apendix 3.

## 4. Solution space approach and examples
The way we use to get to the optimal solution, is by crossovering the `population`. Which we achieve by selecting the top 5 `genomes`. We can evaluate which gemomes are the best by a `fitness function` which in this case will be the `makespan` function, that returns the total delay that the order of the tasks will produce. Clearly what we're trying to do is minimze this delay. After we get the best genomes we 'reproduce' them through a simple `crossover` function.

![image](https://user-images.githubusercontent.com/48858334/194410271-ae6a9559-ec9f-4c03-a362-42bc139f425f.png)

The parent represent the order of in which the tasks would be executed and the offspring would be the children genome. A slice of its data is the same as its parent and the rest of it is in this case shuffled. Then there is a small chance that a `mutation` step will ocurr which consists on shuffling the children genome. This guarantees the population to evolve while goingh through more solutions in the search space. 

By the end of this process we will get a `fitted` population, but the best solution will not necessarily be among the genomes in the final population. So, through the evolution we keep track of the best genome that gives us the best result, and that is the solution that we'll take as our final answer as we see in the [script](https://github.com/Cesarmosqueira/schedule-user-stories/blob/master/main.py).


