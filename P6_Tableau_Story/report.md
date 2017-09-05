# Tableau Story Project
## 1. Introduction

In this project, we will choose [baseball](https://s3.amazonaws.com/udacity-hosted-downloads/ud507/baseball_data.csv) to explore and visualize. In this dataset, we have 1157 observations and 6 variables including their names, handedness height (in inches), weight (in pounds), batting average and home run in total. I will not focus on the variable name since it is more like a primary key containing no duplicate value.

## 2. Summary

In this project, I would like to mainly focus on variable `Height` including the interaction and correlation with other variables. I will include the general distribution of this variable first, then I will try to visualize if players with different heights tend to have different `Home Run` or `Batting Average`. The handedness preference of players will also be discussed.

## 3. Design

First, we would like to use histogram to present the general distribution of variable `Height`. Additionally, I would also like to use stacked plot here so that we are able to notice the distribution of `Handedness` within different height bins.

Second, I would like to build the scatter plot of average `Batting Average` vs average `Home Run`. I will use different colors to represent frequency of `Height`. The lighter color indicates small frequency while darker color indicates larger frequency. A filter of `Handedness` is also added here to see if players with different handedness preference may lead to different results or not.

Third, I will create an animation, the x-axis of which goes from the shortest `Height` to the tallest. The y-axes represent both `Batting Average` and `Home Run`, but separately. I would like to use histogram again. This will give us clearer understanding of the changing of these two measures as height goes taller. Only right-handed players are included.

The initial plot can be viewed by clicking [here](https://public.tableau.com/profile/wenke#!/vizhome/Book1_22831/Story1).

## 4. Feedback
The following two feedbacks are from one of my friends after my first version of visualization.
- 100% stacked plot may also be included because stacked plot only may be misleading because of different bar lengths.
- Redundant encoding can be considered in the scatter plot, which can help emphasize different frequencies.

The feedback here is from a friend after he viewed the new plots that had been modified based on the first two feedbacks.
- It seems that the animation is fading gradually, which definitely misleads viewers if different colors have particular meanings here.

## 5. Update

First, I chose to follow the suggestion of redundant encoding. In my scatter plot of average `Batting Average` vs average `Home Run`, I also used different marker size to represent different height frequencies. The bigger the marker is, the larger frequency it represents. Additionally, I also performed redundant encoding to my animation. Besides the heights of different bins, I also added color to represent the corresponding y-values. The darker color indicates higher corresponding y-values.

However, my second viewer gave me a negative feedback on my animation with redundant encoding. In order not to create any misunderstanding, I set the animation not to fade as time goes by.

For the first feedback, I decided not to include 100% stacked plot. The histogram of `Height` tells us that the frequency of bins at two sides are extremely lower than those bins in the middle. Some of the two-side bins may only have one or two players. The distribution of `handedness` within those bins may be different dramatically. We can choose to subset range of axes or add new filters instead.

- The final plot can be viewed by clicking [here](https://public.tableau.com/profile/wenke#!/vizhome/Book3_5900/Story2)
## Resources

1. Animations On Tableau Public, Tableau Community, https://community.tableau.com/thread/243115
