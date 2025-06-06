## Classification

* Linear regression is not a good algorithm for classification problems.
* decision boundary
* logistic regression

### Logistic Regression

* sigmoid function/logistic function

$$
z=\overrightarrow{w}\cdot\overrightarrow{x}+b\\
g(z)=\frac{1}{1+e^{-z}}n
$$

### Decision Boundary

$$
z=\overrightarrow{w}\cdot\overrightarrow{x}+b=0
$$

### Cost Function

* The squared error cost function is not suitable for logistic regression.

  * It's a non-convex function.
    * If you try to use gradient descent, there are lots of local minimum that you can get stuck in.

* the loss of logistic regression: 
  $$
  L(f_{\overrightarrow{w},b}(\overrightarrow{x}^{(i)}),y^{(i)})=
  \begin{cases}
  -log(f_{\overrightarrow{w},b}(\overrightarrow{x}^{(i)})) & \text{if $y^{(i)}$=1}\\
  -log(1-f_{\overrightarrow{w},b}(\overrightarrow{x}^{(i)})) & \text{if $y^{(i)}$=0}\\
  \end{cases}
  $$
  
* 

* simplified cost function
  * 
