# Differential Privacy Framework for Movie Recommendation System

Applying *differential privacy* to movie recommendation system to guarantee the privacy of individual user ratings.

**Implemented By:**

* @mertkosan
* @mbenlioglu

## About

Consider a trusted 3rd party that holds a statistical database of sensitive and private information (e.g. movie ratings, medical records, e-mail patterns) that would like to
provide global, statistical information about the data for helpful applications and researches. 

Such information carries a danger of revealing information about the individuals.

    + Usage of anonym identities for information might be a method of preserving real identities but deanonymization techniques using two or more separately innocuous databases  
    can reveal the true identities of data providers.
 
Differential privacy aims to provide means to maximize the accuracy of these statistical queries while minimizing the chances of identifying its records. It introduces noise
to real data so that, adding or removing one user to database does not make noticeable difference in the data, thus preventing to identify his/her private information. It is
a probabilistic concept, therefore, any differentially private mechanism is necessarily randomized with Laplace mechanism, exponential mechanism etc.


**More Formally:**
___
Let ε be a positive real number and A be a randomized algorithm that takes a dataset as input (representing the actions of the trusted party holding the data). The algorithm A
is ε-differentially private if for all datasets 𝐷_1 and 𝐷_2 that differ on a single element (i.e., the data of one person), and all subsets S of image of A.

![ε-differential privacy formula](/docs/formula.png)

where the probability is taken over the randomness used by the algorithm.

## Movie Recommendation

In the scope of this project a [movie ratings dataset](https://grouplens.org/datasets/movielens/) has been considered, and by using the ratings of the users, most similar movies to user’s ratings is determined and
a suitable recommendation is done from the ones among them.

To process this dataset, a graph database has been used ([Neo4j](https://neo4j.com/)) with nodes to represent users and movies, and edges between them to represent the rating the a user gives to
a movie as well as the calculated similarity score between two movies.

![Graph Database Snapshot](/docs/sampleGraphDb.png)

Here is a snapshot from shrunk version of the database to give insight about the representation of the data. Blue nodes are anonymized users, green nodes are movies and the
edges are rating relations between users and movies.


## Experimental Test Results

To test the accuracy of our algorithms, we perepared some test queries and retrived the experimental reults to compare and measure the error of the algortihm, from which we have
determined privacy/utility ratio to decide whether the error is within an acceptable range.

In the below table the experimental results of the query _"What is the number of ratings given to a movie? (movie name as parameter)"_ is shown. The Algorithm is run twice and
both results are included to the table. Notice that the difference in the results are coming from the randomness of the algorithm.

| Movie ID      | Actual Rating Count | Noisy Rating Count (exp-1) | Noisy Rating Count (exp-2) |
| ------------- | ------------------- | ---------------------------| -------------------------- |
| ```1```       | ```412```           | ```420,956086753```        | ```390,802680394```        |
| ```10```      | ```216```           | ```219,268858516```        | ```212,135271164```        |
| ```32```      | ```3295```          | ```3312,91503397```        | ```3296,44044631```        |
| ```34```      | ```399```           | ```413,114967105```        | ```392,58561983```         |
| ```47```      | ```480```           | ```472,192080468```        | ```476,43260495```         |

For more information: [Final Report of Project](/docs/finalReport.pdf), [Presentation](/docs/presentation.pdf)