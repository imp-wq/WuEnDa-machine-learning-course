* vscode cannot render `<img>` tags in ipynb files: open the folder that .ipynb files in.

## Multiple Features

multiple features - multiple variables

* Notations:

  * $x_j$: j-th feature
  * $n$: number of features
  * $\overrightarrow{x}^{(i)}$: features of i-th training example, the arrow is an optional identifier, to remind us that this is a vector.
  * $x_j^{(i)}$: value of feature j in the i-th training example

  ![](D:\machine learning\WuEnDa_course\images\multiple-features-notations.jpg)

* Parameters of the model:
  $$
  f_{w,b}=w_1x_1+w_2x_2+\dots+w_nx_n=b\\
  \overrightarrow{w}=[w_1\,w_2\,w_3\dots w_n]\\
  \overrightarrow{x}=[x_1\,x_2\,x_3\dots x_n]\\
  $$

  * To be more succinctly: 
    $$
    f_{\overrightarrow{w},b}(\overrightarrow{x})=\overrightarrow{w}\cdot\overrightarrow{x}+b
    $$

  * w: a vector

  * b: a number

### Vectorization

* advantages:
  * it makes codes shorter
  * it results in your code running much faster:
    * behind the scenes, the numpy `dot` function is able to use parallel hardware in  your computer.

## Numpy

* vector slicing: `[start: stop: step]`

## Feature Scaling

### Mean Normalization

* $\mu_1$: the average of x1
* 2000: maximum
* 300: minimum

$$
x_1=\frac{x_1-\mu_1}{2000-300}
$$

### Z-score normalization

* $\sigma_1$: the standard deviation of x1

$$
x_1=\frac{x_1-\mu_1}{\sigma_1}
$$

## How to choose alpha

### Learning Curve

* horizontal axis: iteration of gradient descent

  * each iteration: a simultaneously update of w and b

* vertical axis: the value of cost function J

  <img src=".\images\learning-curve.png" style="zoom:50%;" />

### Automatic convergence test

1. Let $\epsilon$ be $10^{-3}$.
2. If $J(\overrightarrow{w}, b)$ decreases by $\leq\epsilon$ in one iteration, declare convergence(found parameters $\overrightarrow{w},b$ to get close to global minimum.

## Choosing Learning Rate

* With a small enough alpha, $J(\overrightarrow{w},b)$ should decrease on every iteration.
* Roughly trying out gradient descents with each value of alpha being roughly 3 times bigger than the previous value.
* Try a range of values, until I found the value that's too small, and then also make sure I found a value that is too large. And I'll slowly try to pick the largest possible learning rate or something slightly smaller than the largest reasonable value that I found.

![](.\images\choosing-the-learning-rate.jpg)
