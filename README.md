# Kenny's Meta Strats
The idea is to use the Riot API plus some complicated math to come up with off-meta League of Legends builds.

## Objective Creativity
How can a machine be creative? We have a couple ways to characterize computational creativity (source: [Wikipedia](https://en.wikipedia.org/wiki/Computational_creativity))

1. The answer is novel and useful (either for the individual or for society)
2. The answer demands that we reject ideas we had previously accepted
3. The answer results from intense motivation and persistence
3. The answer comes from clarifying a problem that was originally vague

I propose addressing criteria 1 & 2 by seeking to maximize the objectives: utility, newness, unpopularity.

## The Process
We initialize a recommendation by looking at what you play, and what others play. We look at all-time history, as well as recent history. Suppose you play an abnormal amount of Singed. The machine is more likely to give you a Singed recommendation. Suppose that although Singed is your main, you've been spamming Ezreal in recent games. The machine spots the trend, and will try to give you something more up to speed with your current playing trends.

# TODO